<template>
  <v-container>
    <v-tabs color="dark-gray" slider-color="red" class="mx-2">
      <v-tab>Logs</v-tab>
      <v-tab>Alerts</v-tab>

      <v-spacer></v-spacer>
      <v-btn ma-0 pa-0 flat @click="printlog">
        <v-flex flat class="fill-height red--text pt-2 title"
          >Export Data</v-flex
        >
        <v-flex flat width="60px">
          <v-icon style="padding: 4px 0px 0px 10px " color="red" size="40"
            >file_download</v-icon
          >
        </v-flex>
      </v-btn>

      <v-tab-item>
        <v-container
          fluid
          style=" max-height:410px "
          mt-4
          mx-0
          pa-0
          overflow-y-hidden
          scroll-y
        >
          <v-data-table
            v-model="logsSelected"
            :headers="logsHeaders"
            :items="logs"
          
            item-key="filename"
            class="elevation-1"
            hide-actions
          >
            <template v-slot:headers="logsprops">
              <tr>
                <th>
                  <v-checkbox
                    color="red"
                    :input-value="logsprops.all"
                    :indeterminate="logsprops.indeterminate"
                    hide-details
                    @click.stop="toggleLogs"
                  ></v-checkbox>
                </th>
                <th
                  class="text-xs-left red--text ma-0"
                  v-for="header in logsprops.headers"
                  :key="header.text"
                >
                  {{ header.text }}
                </th>
              </tr>
            </template>
            <template v-slot:items="logsprops">
              <tr>
                <td>
                  <v-checkbox
                    color="red"
                    :active="logsprops.selected"
                    v-model="logsSelected"
                    @click="logsprops.item.selected = !logsprops.item.selected"
                    :input-value="logsprops.item.selected"
                    primary
                    hide-details
                  ></v-checkbox>
                </td>
                <td class="text-xs-centre">{{ logsprops.item.filename }}</td>
                <td class="text-xs-centre">{{ logsprops.item.startTime }}</td>
                <td class="text-xs-centre">{{ logsprops.item.endTime }}</td>
                <td class="text-xs-centre">
                  <v-icon
                    color="red darken-2"
                    @click="deleteLog(logsprops.item)"
                    >clear</v-icon
                  >
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-container>
      </v-tab-item>

      <v-tab-item>
        <v-container
          fluid
          style=" max-height:393px "
          mt-4
          pt-0
          pb-0
          overflow-y-hidden
          scroll-y
        >
          <v-data-table
            v-model="alertsSelected"
            :headers="alertsHeaders"
            :items="alerts"
            :select-all=red
            item-key="timestamp"
            class="elevation-1"
            hide-actions
          >
            <template v-slot:headers="props">
              <tr>
                <th>
                  <v-checkbox
                    :input-value="props.selected"
                    :indeterminate="props.indeterminate"
                    primary
                    hide-details
                    @click.stop="toggleAlerts"
                    color="red"
                  ></v-checkbox>
                </th>
                <th
                  class="text-xs-left red--text ma-0"
                  v-for="header in props.headers"
                  :key="header.text"
                >
                  {{ header.text }}
                </th>
              </tr>
            </template>
            <template v-slot:items="props">
              <tr>
                <td
                  :active="props.selected"
                  @click="props.selected = !props.selected"
                >
                  <v-checkbox
                    :input-value="props.selected"
                    primary
                    hide-details
                    color="red"
                  ></v-checkbox>
                </td>
                <td class="text-xs-centre">{{ props.item.timestamp }}</td>
                <td class="text-xs-centre">{{ props.item.code }}</td>
                <td class="text-xs-centre">{{ props.item.desc }}</td>
                <td class="text-xs-centre">
                  <v-icon color="red darken-2" @click="deleteAlert(props.item)"
                    >clear</v-icon
                  >
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-container>
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>


<script>
import mqtt from "mqtt";
export default {
  data() {
    return {
      connection: {
        host: "localhost",
        port: 9001,
        endpoint: "/mqtt",
        clean: true,
        connectTimeout: 4000,
        reconnectPeriod: 4000,
        clientId: "Logs_Page",
        username: "",
        password: "",
      },
      subscription: {
        topic: "datalogs",
        qos: 1,
      },
      publish_dellogs: {
        topic: "dellogs",
        qos: 1,
        payload: "",
      },
      publish_getlogs: {
        topic: "getlogs",
        qos: 1,
        payload: "",
      },

      isDeleted: [],
      logsSelected: [],
      alertsSelected: [],
      checkbox: [],
      logsHeaders: [
        {
          text: "File Name",
          align: "left",
          sortable: false,
          value: "filename",
        },
        { text: "Start Time", value: "startTime", sortable: false },
        { text: "End Time", value: "endTime", sortable: false },
        { text: "", value: "delete", sortable: false },
      ],
      logs: [],
      alertsHeaders: [
        {
          text: "Date/Time",
          value: "timestamp",
        },
        { text: "Alert Code", value: "code" },
        { text: "Description", value: "desc" },
      ],
    };
  },
  created: function() {
    this.createConnection();
    this.doSubscribe();
    this.doPublish_getlogs();
  },

  methods: {
    toggleLogs() {
      if (this.logsSelected.length) this.logsSelected = [];
      else this.logsSelected = this.logs.slice();
    },
    toggleAlerts() {
      if (this.alertsSelected.length) this.alertsSelected = [];
      else this.alertsSelected = this.alerts.slice();
    },
    changeSort(column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending;
      } else {
        this.pagination.sortBy = column;
        this.pagination.descending = false;
      }
    },

    deleteAlert(item) {
      const index = this.alerts.indexOf(item);
      this.alerts.splice(index, 1);
    },
    printlog() {
      // eslint-disable-next-line
      console.log(this.logsSelected);
    },
  
  createConnection() {
    const { host, port, endpoint, ...options } = this.connection;
    const connectUrl = `ws://${host}:${port}${endpoint}`;
    try {
      this.client = mqtt.connect(connectUrl, options);
    } catch (error) {
      // eslint-disable-next-line
      console.log("mqtt.connect error", error);
    }
    this.client.on("message", (topic, message) => {
      this.logs = JSON.parse(message);
      // eslint-disable-next-line
      console.log(`Received message ${this.logs} from topic ${topic}`);
    });
  },
  doSubscribe() {
    const { topic, qos } = this.subscription;
    this.client.subscribe(topic, { qos }, (error, res) => {
      if (error) {
        // eslint-disable-next-line
        console.log("Subscribe to topics error", error);
        return;
      }
      this.subscribeSuccess = true;
      // eslint-disable-next-line
      console.log("Subscribe to topics res", res);
    });
  },
  doUnSubscribe() {
    const { topic } = this.subscription;
    this.client.unsubscribe(topic, (error) => {
      // eslint-disable-next-line
      console.log("Unsubscribed");
      if (error) {
        // eslint-disable-next-line
        console.log("Unsubscribe error", error);
      }
    });
  },
  doPublish() {
    const { topic, qos, payload } = this.publish_run;
    this.client.publish(topic, payload, qos, (error) => {
      // eslint-disable-next-line
      console.log("Publishing something in manual");
      if (error) {
        // eslint-disable-next-line
        console.log("Publish error", error);
      }
    });
  },
    doPublish_getlogs() {
    const { topic, qos, payload } = this.publish_getlogs;
    this.client.publish(topic, payload, qos, (error) => {
      // eslint-disable-next-line
      console.log("Log getter");
      if (error) {
        // eslint-disable-next-line
        console.log("Publish error", error);
      }
    });
  },
  doPublish_dellogs() {
     
      const { topic, qos, payload } = this.publish_dellogs;
      // eslint-disable-next-line
      console.log("Trying to log delete with payload", payload);
      this.client.publish(topic, payload, qos, (error) => {
              // eslint-disable-next-line
        console.log("Publishing log delete with payload", payload);
        if (error) {
          // eslint-disable-next-line
          console.log("delog Publish error", error);
        }
      });
    },
        deleteLog(item) {
           // eslint-disable-next-line
      console.log("clicked delete ");     
      const index = this.logs.indexOf(item);
      this.publish_dellogs.payload=index.toString();
       // eslint-disable-next-line
      console.log(this.publish_dellogs.payload);
      this.logs.splice(index, 1);
      this.doPublish_dellogs()
     
    },
},
};

</script>
