import time
import paho.mqtt.client as mqtt
import json
import SensorsRead
import pigpio
from UPS_RTC import INA219
import csv
import os
from datetime import datetime
from simple_pid import PID

#_______________________________________________________SETUP___________________________________________
### GPIO Pin Assign
gpio=pigpio.pi()
gpio.set_mode(18, pigpio.OUTPUT)

### SENSORS
ina219 = INA219(addr=0x42) ##UPS Chip, get current value to check for plug pullouts
SensorsRead.HV120_Set()    ## Sends config to HV120 Sensor

### File Paths for Data Logging
file_path= os.path.join(os.getcwd(), "Export_data") #CSV Export Paths
data_tracker= os.path.join(os.getcwd(), "Import_data")
### MQTT Setup
BROKER ='localhost' # Broker (this device) address
TOPIC="esensor" #Default Topic
CLIENT_ID="main_Loop" #Client Id

client= mqtt.Client("Sensors") 
client.connect(BROKER,1803)
client.subscribe([("is_on",0),("run_mode",0),("enclosure_target",0),("duty_cycle",1)])

### Variables
logsRecord={}  # Data for Import_data Json
duty_cycle=25  # Duty cycle
run_mode=0 #Operation mode 0=manual, 1=auto, 2=standy (2 Not yet implemented)
status=0 #0=on 1=Off
enclosureTarget=12 #Pressure Setpoint for PID control
cycle_delay=0.1  #Cycling time

### PID Setup   
pid= PID(2,1,0.2, setpoint=enclosureTarget) #Set pid values : P,I,D and Setpoint
pid.output_limits=(20,255) #Set output limits (20 to keep the motor energised 255 (max value))


### Functions
def createlog(path): #Create Log File
   global fname
   now=datetime.today()
   with open(os.path.join(data_tracker,"logs.json")) as logdata:  #load content of existing data in the data_tracker
      try:
         logsRecord= json.loads(logdata.read() )
      except:
         logsRecord=[]  #if empty create an empty array
   id=str(len(logsRecord)).zfill(2) #Get the length of the array and add 1
   print (f"Id is : {id} and logsrecord length is : {len(logsRecord)}")
   fname= id+"_"+now.strftime("%d-%m-%Y")+".csv" #Assign name sequential+ day
   with open(os.path.join(path,fname),"w") as log:
      logsheaders=["Timestamp", "Enclosure Pressure", "Hepa Blockage", "Running Mode"] #write headers
      writer=csv.writer(log, delimiter=",")
      writer.writerow(logsheaders)
   logsRecord.append({"filename":fname[:-4],"startTime":now.strftime("%H:%M"),"endTime":"in progress"}) #add to list of logs (tracking and data persistence)
   with open(os.path.join(data_tracker,"logs.json"),"w") as output:
         json.dump(logsRecord, output, indent=4) #Write to logs record

def writetolog( file_path, fname, data1, data2, data3):  #Function to write append data to log file
   with open(os.path.join(file_path,fname),"a") as logfile: 
      logwriter=csv.writer(logfile)
      now=datetime.today()
      line=[now.strftime("%H:%M:%S"),data1, data2, data3]
      logwriter.writerow(line)
   
def endlog( path, fname): #Change the status of log session, add end time to log tracking
   with open(os.path.join(path,fname),"r") as logfile:
       now=datetime.today()
       data=json.loads(logfile.read())
       id=(len(data)-1)
   with open(os.path.join(path,fname),"w") as logfile:
       data[id]["endTime"]=now.strftime("%H:%M")
       json.dump(data,logfile,indent=4)

def deletelogentry( path, fname,entryid): #Delete log entry and refresh UI (WIP)
   with open(os.path.join(path,fname),"r") as logfile:
       data=json.loads(logfile.read())
   with open(os.path.join(path,fname),"w") as logfile:
        sortedList=sorted(entryid, reverse=True)
        for e in sortedList:
            print (e)
            del data[e]
        json.dump(data,logfile,indent=4)
        msgt=json.dumps(data)
        client.publish("datalogs",msgt)

def on_message_status(mosq, obj, msg): #Update the running status of the unit, on/off. Change variable in main loop
    global run_mode 
    global status 
    if status==0 and run_mode==0:
        status=1
        createlog(file_path)
        print(f"Manual Mode Started with duty_cycle of:{duty_cycle}")
    elif status==0 and run_mode==1:
        status=1
        createlog(file_path)
        print(f"Auto Mode Started")
    elif status==1:
        status=0
        endlog(data_tracker,"logs.json")
        print ("Turning off manual mode from on/off button")

def on_message_EP(mosq, obj, msg): #Update Pressure Target in Auto Mode
    global enclosureTarget
    enclosureTarget=float(msg.payload.decode("utf-8"))
    pid.setpoint=enclosureTarget
    print(f"Pressure Target Changed to :{enclosureTarget}")

def on_message_DC(mosq, obj, msg): #Update duty cycle when updated for manual mode
    global duty_cycle
    global run_mode
    print("Duty Cycle Updating in Py")
    duty_cycle=float(msg.payload.decode("utf-8"))
    duty_cycle=duty_cycle*2.55 
    print(f"Duty Cycle Changed to :{duty_cycle}")

def is_powered(): #Check current flow direction to detect if the unit has been unplugged
    return ((ina219.getCurrent_mA())/1000)

def runshutdown(): #Not yet implemented : Trigger soft shutdown when power off is detected.
    print("starting shutdown now")

def get_SDP6_Data():  #Get sensor data and update UI
        global sdpr #SDP reading
        global hv120r #hv120r reading
        global run_mode #Run Mode for data logging
        global duty_cycle #Duty cycle for test monitoring (to remove)
        sdpr = round(SensorsRead.read_SDP(),1) 
        calcEncProg= round( (sdpr/24)*100,1)
        hv120r= round(SensorsRead.read_NPU(),1)
        Hepa_Block= round(hv120r/10,1)
        calcHEPA_Block= round(hv120r/10,1) 
        calcAirflow=round((-0.0161*hv120r**2+29.634*hv120r+97.052),1) 
        airflow= round( calcAirflow/1000,1) 
        runString= "Manual" if run_mode==1 else "Auto"
        msgt=json.dumps({ "airflow_prog": airflow, "airflow_disp":airflow, "enclosure_prog":calcEncProg, "enclosure_disp":sdpr if sdpr>=0 else 0 , "block_prog":calcHEPA_Block, "block_disp":Hepa_Block }) #UI Data : Display values and progress bar value could be computed in js.
        client.publish(TOPIC,msgt) #publish data to UI
        writetolog(file_path,fname,calcEncProg,Hepa_Block,runString) #Log record

def on_message_run_mode(mosq, obj, msg): #Update run_mode upon change page in UI
    global run_mode
    run_mode=int(msg.payload.decode("utf-8"))

### Set-up Mqtt callbacks
client.message_callback_add("is_on", on_message_status) 
client.message_callback_add("run_mode", on_message_run_mode) 
client.message_callback_add("enclosure_target", on_message_EP) 
client.message_callback_add("duty_cycle", on_message_DC) 
client.loop_start() #start listening for incoming data
def main():
    reset_flag=True
    while True:
        if is_powered()<=-0.3: 
            runshutdown()
        if status==0: #Unit is off, check if gauges have been reset or else pause and check if status has changed
            if reset_flag==True: #
                time.sleep(cycle_delay)
            elif reset_flag==False:
                global duty_cycle
                gpio.set_PWM_dutycycle(18,0) 
                msgt=json.dumps({ "airflow_prog":0, "airflow_disp":0, "enclosure_prog":0, "enclosure_disp":0 , "block_prog":0, "block_disp":0 })
                client.publish(TOPIC,msgt)
                reset_flag=True
        elif status==1: #unit is on
            reset_flag=False
            if run_mode==0: #and in Manual mode
                get_SDP6_Data()
                gpio.set_PWM_dutycycle(18,duty_cycle) 
                time.sleep(cycle_delay)
            elif run_mode==1: #and in Auto mode
                get_SDP6_Data()
                duty_cycle=pid(round(SensorsRead.read_SDP(),1))  
                gpio.set_PWM_dutycycle(18,duty_cycle)                                             
                time.sleep(cycle_delay)
main()


