<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <div v-if="inProgress">
        <v-layout justify-center>
          <h3> {{ progressMessage }} </h3>
        </v-layout>
        <v-progress-linear
          color="#0191A9"
          indeterminate
          rounded
          height="6">
        </v-progress-linear>
      </div>
      <v-card-title>
        <span class="headline">Manage Metadata</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout column>
            <v-flex xs12 sm6 md4>
              <v-radio-group v-model="radioGroup" row @change="getButtonMessage">
                <v-radio
                  label="List"
                  value="1"
                ></v-radio>
                <v-radio
                  label="New"
                  value="2"
                ></v-radio>
                <v-radio
                  label="Delete"
                  value="3"
                ></v-radio>
              </v-radio-group>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" flat @click="manageActions">{{radioGroupMessage}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data: () => ({
    inProgress: false,
    progressMessage: "",
    radioGroup: 1,
    radioGroupMessage: "",
    showList: false
  }),
  props: {
    dialog: Boolean,
  },
  methods: {
    getButtonMessage() {
      if (this.radioGroup == 1) { 
        this.radioGroupMessage = 'List';
      } else if (this.radioGroup == 2) {
        this.radioGroupMessage = 'New';
      } else if (this.radioGroup == 3) {
        this.radioGroupMessage = 'Delete';
      }
    },
    close() {
      this.dialog = false;
    },
    manageActions() {
      if (this.radioGroup == 1) {
        this.showList = true;
      } else if(this.radioGroup == 2) {
        this.showList = false;
        this.updateMetadata();
      } else if(this.radioGroup == 3) {
        if (confirm("Are you sure you want to delete this metadata?")) {
          this.showList = false;
          this.deleteMetadata();
        }
      }
    },

    getMetadata() {

    },

    updateMatadata() {

    },

    deleteMetadata() {

    }
  },

  computed: {
    show: {
      get () {
        return this.dialog
      },
      set (value) {
         this.$emit('dialog', value)
      }
    }
  }
}
</script>