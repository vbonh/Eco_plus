<template>
  <v-container grid-list-md mt-2 pa-0 style="height:520px" overflow-hidden>
    <v-layout row wrap>
      <v-flex md6 ma-3>
        <v-card>
          <v-card-title class="pb-0 pl-3 ma-0 title red--text darken-2">
            Date:
          </v-card-title>
          <v-flex pt-0 pr-4 pl-3 mt--3>
            <v-dialog
              ref="dialog1"
              v-model="modal"
              :return-value.sync="date"
              full-width
              persistent
              lazy
              width="460px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="date"
                  prepend-icon="calendar_today"
                  readonly
                  v-on="on"
                  color="red darken-2"
                ></v-text-field>
              </template>

              <v-date-picker v-model="date" landscape color="red darken-2">
                <v-btn flat color="red darken-2" @click="modal = false"
                  >Cancel</v-btn
                >
                <v-btn
                  flat
                  color="red darken-2"
                  @click="$refs.dialog1.save(date)"
                  >OK</v-btn
                >
              </v-date-picker>
            </v-dialog>
          </v-flex>
          <v-card-title class="pb-0 pl-3 ma-0 title red--text darken-2">
            Time:
          </v-card-title>
          <v-flex pt-0 pr-4 pl-3 mt--3>
            <v-dialog
              ref="dialog"
              v-model="modal2"
              :return-value.sync="time"
              persistent
              lazy
              full-width
              width="460px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-if="modal2"
                v-model="time"
                format="24hr"
                landscape
                full-width
                color="red darken-2"
              >
                <v-spacer></v-spacer>
                <v-btn flat color="red darken-2" @click="modal2 = false"
                  >Cancel</v-btn
                >
                <v-btn
                  flat
                  color="red darken-2"
                  @click="$refs.dialog.save(time)"
                  >OK</v-btn
                >
              </v-time-picker>
            </v-dialog>
          </v-flex>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
export default {
  data: () => ({
    date: new Date().toISOString().substr(0, 10),
    menu: false,
    modal: false,
    e7: null,
    time: new Date().toLocaleTimeString().substring(0, 5),
    modal2: false,
  }),
};
</script>
