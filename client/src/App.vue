<template>
  <v-app class="grey lighten-4 test">
    <Navbar />
    <Drawer />

    <v-content no-gutter>
      <v-slide-x-reverse-transition mode="out-in">
        <router-view></router-view>
      </v-slide-x-reverse-transition>
    </v-content>
  </v-app>
</template>

<script>
import Navbar from "@/components/Navbar";
import Drawer from "@/components/Drawer";

export default {
  components: {
    Navbar,
    Drawer,
  },
  data() {
    return {};
  },

  beforeCreate() {},
  mounted() {},
  methods: {},
};
</script>
<style>
.test {
  overflow-x: hidden;
  overflow-y: hidden;
}
</style>
