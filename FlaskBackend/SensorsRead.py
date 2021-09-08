
import time
import pigpio

pi = pigpio.pi()

#Sensor Addresses
SDP_addr = 0x40
HV120_addr= 0x28

# i2c bus
bus = 1

#Sensor Commanbds
rdEnc = 0xF1 #Read Command for SDP610
rdNPU = 0xE5 #Read Command for HV120
hv120_config= 0xd5 #Setup for HV120
hv120_convert=0.0421899



def HV120_Set(): 
	handle = pi.i2c_open(bus, HV120_addr) # open i2c bus
	pi.i2c_write_byte(handle, hv120_config) #Send config to sensor
	pi.i2c_close(handle) # close i2c bus
	# print("Sensor Config Sent")
	time.sleep(0.2) # reset takes 15ms so let's give it some time

def read_SDP():
	handle = pi.i2c_open(bus, SDP_addr) # open i2c bus
	pi.i2c_write_byte(handle, rdEnc) # send read command
	(count, byteArray) = pi.i2c_read_device(handle, 2) 
	t1 = byteArray[0] # most significant byte msb
	t2 = byteArray[1] # least significant byte lsb
	SDP_reading = int.from_bytes(byteArray, byteorder='big', signed=True) # combine both bytes 
	SDP_Pressure = ((SDP_reading / 240)) # formula from datasheet
	return SDP_Pressure

def read_NPU():
	handle = pi.i2c_open(bus, HV120_addr) # open i2c bus
	(count, byteArray) = pi.i2c_read_device(handle, 2) # retrieve data
	pi.i2c_close(handle) 
	h1 = byteArray[0] # most significant byte msb
	h2 = byteArray[1] # least significant byte lsb
	HV120_reading= int.from_bytes(byteArray, byteorder='big', signed=True)
	HV120_Pressure = HV120_reading*hv120_convert
	return HV120_Pressure

