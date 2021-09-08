<template>
  <div>
    <v-navigation-drawer clipped app v-model="drawer" permanent width="150">
      <v-container fill-height pa-0>
        <v-list>
          <v-list-tile
            router
            :to="links[0].route"
            active-class="blue-grey lighten-5 red--text"
            class="blue-grey--text darken-2"
          >
            <v-list-tile-action>
              <v-avatar style="margin-left:1px" color="red" size="34">
                <span class="white--text medium title">M</span>
              </v-avatar>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ links[0].text }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile
            router
            :to="links[3].route"
            active-class="blue-grey lighten-5 red--text"
            class="blue-grey--text darken-2"
          >
            <v-list-tile-action>
              <v-avatar style="margin-left:1px" color="red" size="34">
                <span class="white--text medium title">A</span>
              </v-avatar>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ links[3].text }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile
            router
            :to="links[4].route"
            active-class="blue-grey lighten-5 red--text"
            class="blue-grey--text darken-2"
          >
            <v-list-tile-action>
              <v-avatar style="margin-left:1px" color="red" size="34">
                <span class="white--text medium title">S</span>
              </v-avatar>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ links[4].text }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile
            v-for="index in 2"
            :key="links[index].text"
            router
            :to="links[index].route"
            active-class="blue-grey lighten-5 red--text"
            class="blue-grey--text text--darken-2"
          >
            <v-list-tile-action>
              <v-icon large color="red darken-1">{{
                links[index].icon
              }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ links[index].text }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-container>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      links: [
        { icon: "smart_toy", text: "Manual", route: "/" },
        { icon: "settings", text: "Settings", route: "/settings" },
        { icon: "article", text: "Logs", route: "/logsbkp" },
        { icon: "hdr_auto", text: "Auto", route: "/auto" },
        { icon: "email", text: "Standby", route: "/standby" },

        // { icon: "email", text: "Blob", route: "/logsbkp" }
      ],
    };
  },
};
</script>

<style></style>
