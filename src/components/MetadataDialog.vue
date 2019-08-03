<template>
  <v-dialog v-model="dialog" max-width="500px">
    <template v-slot:activator="{ on }">
      <v-btn @click="getMetadata" dark color="#0191A9" class="mb-2" v-on="on">View</v-btn>
    </template>
    <v-card>
      <div v-if="inProgress">
        <v-layout justify-center>
          <h3>{{ progressMessage }}</h3>
        </v-layout>
        <v-progress-linear color="#0191A9" indeterminate rounded height="6"></v-progress-linear>
      </div>
      <v-card-title>
        <span class="headline">Manage Metadata</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout column>
            <v-flex xs12 sm6 md4>
              <v-radio-group v-model="radioGroup" row @change="getButtonMessage">
                <v-radio name="options" label="List" :value="1"></v-radio>
                <v-radio name="options" label="New" :value="2"></v-radio>
                <v-radio name="options" label="Delete" :value="3"></v-radio>
              </v-radio-group>
            </v-flex>
            <v-flex xs12 sm6 md4 v-if="radioGroup == 1">
              <v-simple-table>
                <thead>
                  <tr>
                    <th class="text-left">Name</th>
                    <th class="text-left">Type</th>
                    <th class="text-left">Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="metadata in metadataArray" :key="metadata">
                    <td>{{ metadata.name }}</td>
                    <td>{{ metadata.type }}</td>
                    <td>{{ metadata.value }}</td>
                  </tr>
                </tbody>
              </v-simple-table>
            </v-flex>
            <v-flex xs12 sm6 md4 v-if="radioGroup == 2">
              <v-text-field
                v-model="metadata.name"
                label="Name"
                :rules="basicRules"
                autofocus
              ></v-text-field>
              <v-select
                v-model="metadata.type"
                :items="metadataTypes"
                label="Type"
                :rules="basicRules"
              ></v-select>
              <v-text-field
                v-model="metadata.value"
                label="Value"
                :rules="basicRules"
              ></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 md4 v-if="radioGroup == 3">
              <v-select
                v-model="metadata.id"
                :items="metadataArray"
                item-text="name"
                item-value="id"
                label="Select a metadata"
              ></v-select>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" v-if="radioGroup != 1" flat @click="manageActions">{{radioGroupMessage}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import axios from 'axios';

export default {
  data: () => ({
    dialog: false,
    inProgress: false,
    progressMessage: "",
    radioGroup: 1,
    radioGroupMessage: "",
    metadataArray: [],
    metadata: {
      id: null,
      name: null,
      type: null,
      value: null,
    },
    metadataTypes: ["Text", "Number", "Date"],
    basicRules: [v => !!v || "Required field"]
  }),

  props: ['favoriteThing'],

  methods: {
    getButtonMessage() {
      if (this.radioGroup == 2) {
        this.radioGroupMessage = "New";
      } else if (this.radioGroup == 3) {
        this.radioGroupMessage = "Delete";
      }
    },

    close() {
      this.dialog = false;
    },

    manageActions() {
      if (this.radioGroup == 2) {
        this.saveMetadata();
      } else if (this.radioGroup == 3) {
        if (confirm("Are you sure you want to delete this metadata?")) {
          this.deleteMetadata();
        }
      }
      this.getMetadata();
    },

    getMetadata() {
      try {
        this.setDialogProgress(true, "Loading Metadata...");
        axios
          .get("/api/metadata")
          .then(response => {
            console.log(response.data);
            this.setDialogProgress(false, "");
            this.metadataArray = response.data;
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while getting the metadata");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while getting the metadata");
        console.log(error);
      }
    },

    saveMetadata() {
      try {
        this.setDialogProgress(true, "Saving Metadata...");
        axios({
          method: "post",
          url: "/api/metadata/",
          headers: { "Content-Type": "application/json" },
          data: {
            key: this.metadata.name,
            type: this.metadata.type,
            value: this.metadata.value,
            favorite_thing: this.favoriteThing.id,
          }
        })
          .then(response => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Successfuly created the metadata " + response.data.key);
            this.cleanFields();
            this.radioGroup = 1;
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while creating the metadata");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while creating the metadata");
        console.log(error);
      }
    },

    deleteMetadata() {
      try {
        this.setDialogProgress(true, "Deleting Metadata...");
        axios({
          method: "delete",
          url: "/api/metadata/" + this.metadata.id + "/",
          headers: { "Content-Type": "application/json" }
        })
          .then(() => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Successfuly deleted the metadata");
            this.cleanFields();
            this.radioGroup = 1;
            this.getCategories();
            this.$emit('getFavoriteThings');
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while deleting the category");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while deleting the category");
        console.log(error);
      }
    },

    cleanFields() {
      this.metadata.id = null;
      this.metadata.name = null;
      this.metadata.type = null;
      this.metadata.value = null;
    },

    setDialogProgress(status, message) {
      this.inProgress = status;
      this.progressMessage = message;
    },
  }
};
</script>