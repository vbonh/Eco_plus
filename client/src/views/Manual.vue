<template>
  <v-container grid-list-md mt-2 pa-0 style="height:520px" overflow-hidden>
    <v-layout row wrap>
      <v-flex white elevation-1 md12 mx-4 mt-3 pb-3 style="height:50px">
        <v-card-title dark color="primary">
          <div>
            <h3 class="red--text title">Manual Mode</h3>
          </div>
        </v-card-title>
      </v-flex>
      <v-layout row wrap mx-4 mb-4 pa-0>
        <v-flex elevation-1 mx-n2 white md4 pt-3 style="height:300px">
          <v-layout justify-center mt-4>
            <vue-ellipse-progress
              class="v-label headline"
              v-bind:progress="sensordata.airflow_disp"
              :thickness="16"
              :color="airColored"
              :angle="0"
              line="butt"
              :half="true"
              :size="240"
              lineMode="out -4"
              emptyColor="#B0BEC5"
              v-bind:legend-value="sensordata.airflow_prog"
            >
              <span slot="legend-value" class="v-label headline"
                >/{{ gauges[0].rangeHigh }}</span
              >
              <p slot="legend-caption" class="title mt-2 ma-0">
                {{ gauges[0].name }}
              </p>
              <span
                slot="legend-caption"
                style="font-size:13pt"
                class="mt-0 pa-0 theme--light"
                v-html="gauges[0].unit"
                >{{ gauges[0].unit }}</span
              >
            </vue-ellipse-progress>
          </v-layout>
        </v-flex>

        <v-flex elevation-1 mx-n2 white md4 pt-3 style="height:300px">
          <v-layout justify-center mt-4>
            <vue-ellipse-progress
              class="v-label headline"
              v-bind:progress="sensordata.enclosure_disp"
              :thickness="16"
              :color="encColored"
              :angle="0"
              line="butt"
              :half="true"
              :size="240"
              lineMode="out -4"
              emptyColor="#B0BEC5"
              v-bind:legend-value="sensordata.enclosure_prog"
            >
              <span slot="legend-value" class="v-label headline"
                >/{{ gauges[1].rangeHigh }}</span
              >
              <p slot="legend-caption" class="title mt-2 ma-0">
                {{ gauges[1].name }}
              </p>
              <span
                slot="legend-caption"
                style="font-size:13pt"
                class="mt-0 pa-0 theme--light"
                v-html="gauges[1].unit"
                >{{ gauges[1].unit }}</span
              >
            </vue-ellipse-progress>
          </v-layout>
        </v-flex>

        <v-flex elevation-1 mx-n2 white md4 pt-3 style="height:300px">
          <v-layout justify-center mt-4>
            <vue-ellipse-progress
              class="v-label headline"
              :progress="sensordata.block_disp"
              :thickness="16"
              :color="presColored"
              :angle="0"
              line="butt"
              :half="true"
              :size="240"
              lineMode="out -4"
              emptyColor="#B0BEC5"
              v-bind:legend-value="sensordata.block_prog"
            >
              <span slot="legend-value" class="v-label headline"
                >/{{ gauges[2].rangeHigh }}</span
              >
              <p slot="legend-caption" class="title mt-2 ma-0">
                {{ gauges[2].name }}
              </p>
              <span
                slot="legend-caption"
                style="font-size:13pt"
                class="mt-0 pa-0 theme--light"
                v-html="gauges[2].unit"
                >{{ gauges[2].unit }}</span
              >
            </vue-ellipse-progress>
          </v-layout>
        </v-flex>
      </v-layout>

      <v-flex elevation-2 white md12 pa-0 mb-1 mx-4 style="height:110px">
        <v-layout row wrap>
          <v-flex md6 offset-md3 mt-3 white>
            <h3 class="red--text title pl-3">Fan Speed: {{ duty_cycle }}%</h3>
            <v-card color="white" flat>
              <v-slider
                v-model="duty_cycle"
                @change="updateDC"
                :disabled="switch1"
                color="red"
                step="5"
                label="100"
                inverse-label
                class="px-3"
              >
                <template v-slot:prepend>
                  <div class="v-label theme--light pt-1">0</div>
                </template>
              </v-slider>
            </v-card>
          </v-flex>
          <v-flex md1 mt-1 pa-0 fill-height>
            <v-card white flat>
              <v-icon v-if="switch1 === true" color="red" class="pt-2" large
                >lock</v-icon
              >
              <v-icon v-else color="gray" class="pt-2" large>lock_open</v-icon>
              <v-switch color="red" class="pt-0" v-model="switch1"></v-switch>
            </v-card>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import mqtt from "mqtt";
export default {
  name: "manual",
  components: {},
  data: () => ({
    connection: {
      host: "localhost",
      port: 9001,
      endpoint: "/mqtt",
      clean: true,
      connectTimeout: 4000,
      reconnectPeriod: 4000,
      clientId: "Manuage",
      username: "",
      password: "",
    },
    subscription: {
      topic: "esensor",
      qos: 0,
    },
    publish_run: {
      topic: "run_mode",
      qos: 1,
      payload: "0",
    },
    publish_status: {
      topic: "is_on",
      qos: 1,
      payload: '{ "msg": 0 }',
    },
    publish_DC: {
      topic: "duty_cycle",
      qos: 1,
      payload: "25",
    },
    sensordata: {
      airflow_prog: 0,
      airflow_disp: 0,
      enclosure_prog: 0,
      enclosure_disp: 0,
      block_prog: 0,
      block_disp: 0,
    },

    qosList: [
      { label: 0, value: 0 },
      { label: 1, value: 1 },
      { label: 2, value: 2 },
    ],
    client: {
      connected: false,
    },
    subscribeSuccess: false,
    switch1: true,
    duty_cycle: 25,
    interval: null,
    dialog: false,
    gauges: [
      {
        name: "Airflow",
        progress: 0,
        show: 2.6,
        unit: "(000's M<sup>3</sup>/Hr)",
        color: "green",
        rangeHigh: 10,
      },
      {
        name: "Enclosure Pressure",
        progress: 0,
        show: 8.9,
        unit: "(Pa)",
        color: "orange",
        rangeHigh: 24,
      },
      {
        name: "HEPA Blockage",
        progress: 80,
        show: 80,
        unit: "(Percent)",
        color: "red",
        rangeHigh: 100,
      },
    ],
  }),

  computed: {
    presColored() {
      if (this.sensordata.block_disp > 70) return "red"; //1000Pa max
      if (this.sensordata.block_disp > 60) return "#e06c00";
      if (this.sensordata.block_disp < 60) return "green";
      return "red";
    },
    encColored() {
      if (this.sensordata.enclosure_disp > 25) return "red"; //1000Pa max
      if (this.sensordata.enclosure_disp > 20) return "#e06c00";
      if (this.sensordata.enclosure_disp < 20) return "green";
      return "red";
    },
    airColored() {
      if (this.sensordata.airflow_disp > 95) return "red"; //1000Pa max
      if (this.sensordata.airflow_disp > 90) return "#e06c00";
      if (this.sensordata.airflow_disp < 90) return "green";
      return "red";
    },

    animationDuration() {
      return `${this.duty_cycle}s`;
    },
  },
  created: function() {
    this.createConnection();
    this.doSubscribe();

    // this.doPublish();
  },
  beforeDestroy() {
    this.doUnSubscribe();
    this.destroyConnection();

    // this.doPublish();
    // eslint-disable-next-line
    // console.log("Page Change");
  },
  mounted() {
    this.doPublish();
    this.doPublishDC();
  },

  methods: {
    updateDC: function(value) {
      // eslint-disable-next-line
      console.log("Slider DC Changed");
      this.publish_DC.payload = value.toString();
      this.doPublishDC();
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
      this.client.on("connect", () => {
        // eslint-disable-next-line
        console.log("Connection succeeded!");
      });
      this.client.on("error", (error) => {
        // eslint-disable-next-line
        console.log("Connection failed", error);
      });
      this.client.on("message", (topic, message) => {
        this.sensordata = JSON.parse(message);
        // eslint-disable-next-line
        console.log(`Received message ${this.sensordata} from topic ${topic}`);
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
    doPageAck() {
      const { topic, qos, payload } = this.publish;
      this.client.publish(topic, payload, qos, (error) => {
        if (error) {
          // eslint-disable-next-line
          console.log("Publish error", error);
        }
      });
    },
    doPublishDC() {
      const { topic, qos, payload } = this.publish_DC;
      this.client.publish(topic, payload, qos, (error) => {
        // eslint-disable-next-line
        console.log("Duty Cycle updated"), payload;
        if (error) {
          // eslint-disable-next-line
          console.log("Publish error", error);
        }
      });
    },

    destroyConnection() {
      if (this.client.connected) {
        try {
          this.client.end();
          this.client = {
            connected: false,
          };
          // eslint-disable-next-line
          console.log("Successfully disconnected!");
        } catch (error) {
          // eslint-disable-next-line
          console.log("Disconnect failed", error.toString());
        }
      }
    },

    decrement() {
      this.duty_cycle--;
    },
    increment() {
      this.duty_cycle++;
    },
  },
};
</script>
