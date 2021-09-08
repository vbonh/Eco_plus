<template>
  <v-container>
    <v-tabs color="dark-gray" slider-color="red" class="mx-2">
      <v-tab>Logs</v-tab>
      <v-tab>Alerts</v-tab>
      <v-spacer></v-spacer>
      <v-btn ma-0 pa-0 flat>
        <v-card flat class="fill-height blue-grey--text pt-1 title"
          >Export Data</v-card
        >
        <v-card flat width="60px">
          <v-icon style="padding: 4px 0px 0px 10px " color="red" size="40"
            >file_download</v-icon
          >
        </v-card>
      </v-btn>
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
            v-model="logsSelected"
            :headers="logsHeaders"
            :items="logs"
            select-all
            item-key="filename"
            class="elevation-1"
            hide-actions
          >
            <template v-slot:headers="logsProps">
              <tr>
                <th>
                  <v-checkbox
                    color="red"
                    :input-value="logsProps.all"
                    :indeterminate="logsProps.indeterminate"
                    hide-details
                    @click.stop="toggleLogs"
                  ></v-checkbox>
                </th>
                <th
                  class="text-xs-left red--text ma-0"
                  v-for="header in logsProps.headers"
                  :key="header.text"
                >
                  {{ header.text }}
                </th>
              </tr>
            </template>
            <template v-slot:items="logsProps">
              <tr
                :active="logsProps.selected"
                @click="logsProps.selected = !logsProps.selected"
              >
                <td>
                  <v-checkbox
                    :input-value="logsProps.selected"
                    hide-details
                    color="red"
                  ></v-checkbox>
                </td>
                <td class="text-xs-centre">{{ logsProps.item.filename }}</td>
                <td class="text-xs-centre">{{ logsProps.item.startTime }}</td>
                <td class="text-xs-centre">{{ logsProps.item.endTime }}</td>
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
            select-all
            item-key="timestamp"
            class="elevation-1"
            hide-actions
          >
            <template v-slot:headers="props">
              <tr>
                <th>
                  <v-checkbox
                    :input-value="props.all"
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
              <tr
                :active="props.selected"
                @click="props.selected = !props.selected"
              >
                <td>
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
  data: () => ({
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
    publish_logupdates: {
      topic: "logupdates",
      qos: 1,
      payload: "0",
    },
    logsSelected: [],
    logsHeaders: [
      {
        text: "Filename",
        value: "filename",
      },
      { text: "Start Time", value: "startT" },
      { text: "End Time", value: "endT" },
    ],
    logs: [
      {
        filename: "01--14-05-2021",
        startTime: "14:50",
        endTime: "In Progress",
      },
      {
        filename: "03--13-05-2021",
        startTime: "16:50",
        endTime: "18:53",
      },
      {
        filename: "02--13-05-2021",
        startTime: "14:50",
        endTime: "18:53",
      },
      {
        filename: "01--13-05-2021",
        startTime: "12:50",
        endTime: "18:53",
      },
      {
        filename: "04--12-05-2021",
        startTime: "17:50",
        endTime: "18:53",
      },
      {
        filename: "03--12-05-2021",
        startTime: "12:50",
        endTime: "18:53",
      },
      {
        filename: "02--12-05-2021",
        startTime: "14:50",
        endTime: "18:53",
      },
      {
        filename: "01--12-05-2021",
        startTime: "14:50",
        endTime: "18:53",
      },
      {
        filename: "01-01-05-2021",
        startTime: "11:50",
        endTime: "18:53",
      },
      {
        filename: "01-07-05-2021",
        startTime: "11:50",
        endTime: "18:53",
      },
    ],
    alertsSelected: [],
    alertsHeaders: [
      {
        text: "Date/Time",
        value: "timestamp",
      },
      { text: "Alert Code", value: "code" },
      { text: "Description", value: "desc" },
    ],
    alerts: [
      {
        timestamp: " 01-05-2021/15:46",
        code: "MLP01",
        desc: "Pressure drop detected",
      },
      {
        timestamp: " 01-10-2021/15:45",
        code: "AHP01",
        desc: "Pressure above target",
      },
      {
        timestamp: " 01-12-2021/15:46",
        code: "PS01",
        desc: "Particles detected at exhaust",
      },
      {
        timestamp: " 01-12-2020/15:46",
        code: "FB01",
        desc: "HEPA filter blockage above limit",
      },
      {
        timestamp: " 01-05-2020/15:46",
        code: "ALP01",
        desc: "Pressure below target",
      },
      {
        timestamp: " 01-06-2020/15:46",
        code: "LP01",
        desc: "Pressure drop detected",
      },
      {
        timestamp: " 01-03-2021/15:46",
        code: "FB01",
        desc: "HEPA filter blockage above limit",
      },
    ],
  }),

  methods: {
    toggleAlerts() {
      if (this.alertsSelected.length) this.alertsSelected = [];
      else this.alertsSelected = this.alerts.slice();
    },
    toggleLogs() {
      if (this.logsSelected.length) this.logsSelected = [];
      else this.logsSelected = this.logs.slice();
    },
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
};
</script>

<style>
.project.complete {
  border-left: 4px solid #3cd1c2;
}
.project.ongoing {
  border-left: 4px solid orange;
}
.project.overdue {
  border-left: 4px solid tomato;
}
</style>
