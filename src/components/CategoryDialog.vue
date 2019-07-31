<template>
  <v-dialog v-model="dialog" max-width="500px">
    <template v-slot:activator="{ on }">
      <v-btn @click="getCategories" dark color="#0191A9" class="mb-2" v-on="on">Manage Category</v-btn>
    </template>
    <v-card>
      <div v-if="inProgress">
        <v-layout justify-center>
          <h3>{{ progressMessage }}</h3>
        </v-layout>
        <v-progress-linear color="#0191A9" indeterminate rounded height="6"></v-progress-linear>
      </div>
      <v-card-title>
        <span class="headline">Manage Category</span>
      </v-card-title>
      <v-card-text>
        <v-container grid-list-md>
          <v-layout column>
            <v-flex xs12 sm6 md4>
              <v-radio-group v-model="radioGroup" row @change="getButtonMessage">
                <v-radio name="options" label="New" value="1"></v-radio>
                <v-radio name="options" label="Update" value="2"></v-radio>
                <v-radio name="options" label="Delete" value="3"></v-radio>
              </v-radio-group>
            </v-flex>
            <v-flex xs12 sm6 md4>
              <v-select
                v-model="category.id"
                v-if="radioGroup > 1"
                :items="categories"
                item-text="name"
                item-value="id"
                label="Select a category"
              ></v-select>
            </v-flex>
            <v-flex xs12 sm6 md4>
              <v-text-field
                v-if="radioGroup != 3"
                v-model="category.name"
                label="Name"
                :rules="basicRules"
                autofocus
              ></v-text-field>
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
import axios from 'axios';

export default {
  data: () => ({
    dialog: false,
    inProgress: false,
    progressMessage: "",
    radioGroup: 1,
    radioGroupMessage: "New",
    categories: [],
    category: {
      id: null,
      name: null
    },
    basicRules: [
      v => !!v || 'Required field',
    ]
  }),

  methods: {
    getCategories() {
      try {
        this.setDialogProgress(true, "Loading Categories...");
        axios
          .get("/api/category")
          .then(response => {
            this.setDialogProgress(false, "");
            this.categories = response.data;
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while getting the categories");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while getting the categories");
        console.log(error);
      }
    },

    saveCategory() {
      try {
        this.setDialogProgress(true, "Saving Category...");
        axios({
          method: "post",
          url: "/api/category/",
          headers: { "Content-Type": "application/json" },
          data: {
            name: this.category.name
          }
        })
          .then(response => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Successfuly created the category " + response.data.name);
            this.category.name = null;
            this.category.id = null;
            this.radioGroup = 1;
            this.getCategories();
            this.$emit('getFavoriteThings');
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while creating the category");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while creating the category");
        console.log(error);
      }
    },

    updateCategory() {
      try {
        this.setDialogProgress(true, "Updating Category...");
        axios({
          method: "put",
          url: "/api/category/" + this.category.id + "/",
          headers: { "Content-Type": "application/json" },
          data: {
            name: this.category.name
          }
        })
          .then(response => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Successfuly updated the category " + response.data.name);
            this.category.name = null;
            this.category.id = null;
            this.radioGroup = 1;
            this.getCategories();
            this.$emit('getFavoriteThings');
          })
          .catch(error => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Failed while updating the category");
            console.log(error);
          });
      } catch (error) {
        this.setDialogProgress(false, "");
        this.$emit('setSnackbar', "Failed while updating the category");
        console.log(error);
      }
    },

    deleteCategory() {
      try {
        this.setDialogProgress(true, "Deleting Category...");
        axios({
          method: "delete",
          url: "/api/category/" + this.category.id + "/",
          headers: { "Content-Type": "application/json" }
        })
          .then(() => {
            this.setDialogProgress(false, "");
            this.$emit('setSnackbar', "Successfuly deleted the category");
            this.category.id = null;
            this.category.name = null;
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

    manageActions() {
      if (this.radioGroup == 1) {
        this.saveCategory();
      } else if(this.radioGroup == 2) {
        this.updateCategory();
      } else if(this.radioGroup == 3) {
        if (confirm("Are you sure you want to delete this category? " +
            "By deleting this category all related favorite things will be also deleted.")) {
          this.deleteCategory();
        }
      }
    },

    setDialogProgress(status, message) {
      this.inProgress = status;
      this.progressMessage = message;
    },

    getButtonMessage() {
      if (this.radioGroup == 1) { 
        this.radioGroupMessage = 'Save';
      } else if (this.radioGroup == 2) {
        this.radioGroupMessage = 'Update';
      } else if (this.radioGroup == 3) {
        this.radioGroupMessage = 'Delete';
      }
    },

    close() {
      this.dialog = false;
    },
  }
};
</script>