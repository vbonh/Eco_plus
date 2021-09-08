<template>
  <nav>
    <v-toolbar flat app class="elevation-2">
      <v-toolbar-title right class="text-uppercase blue-grey--text">
        <span class="font-weight-light headline">NPU10000</span>
        <span class="headline font-weight-medium">
          ECO
          <sup>+</sup>
        </span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        class="text-uppercase blue-grey--text title font-weight-light"
        font-weight-medium
        flat
        left
        mr-2
        pa-0
        style="width: 180px "
        @click="doPublish"
      >
        <v-spacer></v-spacer>
        {{ status ? 'Start Unit' : 'Stop Unit' }}
        <v-icon
          class="mr-3 ml-1 pl-0"
          large
          right
          :color="status ? 'red' : 'green'"
        >power_settings_new</v-icon>
        <!-- <v-icon right></v-icon> -->
      </v-btn>
    </v-toolbar>
  </nav>
</template> 

<script>
import mqtt from "mqtt";``

export default {
  name: "Navbar",
  components: {},
  data: () => ({
    status: true,
    connection: {
      host: "localhost",
      port: 9001,
      endpoint: "/mqtt",
      clean: true, 
      connectTimeout: 4000, 
      reconnectPeriod: 4000, 
      clientId: "Navbartt",
      username: "",
      password: ""
    },
    // subscription: {
    //   topic: "esensor",
    //   qos: 0
    // },
    powerstatus: {
      topic: "is_on",
      qos: 0,
      payload: "1"
    },
    sensordata: {},
    // sensorVal: 0,
    qosList: [
      { label: 0, value: 0 },
      { label: 1, value: 1 },
      { label: 2, value: 2 }
    ],
    client: {
      connected: false
    },
    subscribeSuccess: false,
    switch1: true,
    speed: 30,
    interval: null,
    dialog: false
  }),

  computed: {},

  created: function() {
    this.createConnection();
  },
  beforeDestroy() {

 
    this.destroyConnection()
  },
  mounted() {},

  methods: {
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
      this.client.on("error", error => {
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
                  // eslint-disable-next-line
          console.log("NavBar Connected and subscribed", error);
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
      this.client.unsubscribe(topic, error => {
        if (error) {
          // eslint-disable-next-line
          console.log("Unsubscribe error", error);
        }
      });
    },
    // doPublish() {
    //   const { topic, qos, payload } = this.publish;
    //   this.client.publish(topic, payload, qos, error => {
    //     if (error) {
    //       // eslint-disable-next-line
    //       console.log("Publish error", error);
    //     }
    //   });
    // },    
    doPublish: function() {
      const { topic, qos, payload } = this.powerstatus;
      this.client.publish(topic, payload, qos, error => {
          this.status= !this.status; 
          // eslint-disable-next-line
          console.log("Power Clicked")
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
            connected: false
          };
          // eslint-disable-next-line
          console.log("Successfully disconnected!");
        } catch (error) {
          // eslint-disable-next-line
          console.log("Disconnect failed", error.toString());
        }
      }
    }
  }
};
</script>

<style>
</style>