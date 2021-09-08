import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/src/stylus/app.styl";
// import "@mdi/font/css/materialdesignicons.min.css";
// import myIconSvg from '@/components/CustomIcon.vue'

Vue.use(Vuetify, {
  icons: {
    iconfont: "md",
  },
  //Replace color scheme values
  theme: {
    primary: "#9652ff",
    success: "#3cd1c2",
    info: "#ffaa2c",
    error: "#f83e70",
  },
});
