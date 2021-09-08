import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";
import router from "./router";
import VueSvgGauge from "vue-svg-gauge";
import VueEllipseProgress from "vue-ellipse-progress";
Vue.use(VueEllipseProgress);
Vue.config.productionTip = false;
Vue.use(VueSvgGauge);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
