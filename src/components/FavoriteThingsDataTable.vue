<template>
  <v-container>
    <div v-if="inMainProgress">
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
    <v-toolbar flat color="white">
      <v-spacer></v-spacer>
      <v-dialog v-model="favoriteThingDialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn @click="getCategories" dark color="#0191A9" class="mb-2" v-on="on">New Favorite Thing</v-btn>
        </template>
        <v-card>
          <div v-if="inFavoriteDialogProgress">
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
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout column>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.title" label="Title" :rules="basicRules" autofocus></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-textarea
                    v-model="editedItem.description"
                    auto-grow
                    counter
                    label="Description">
                  </v-textarea>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.ranking" label="Ranking" :rules="basicRules"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-select
                    v-model="editedItem.category"
                    :items="categories"
                    item-text="name"
                    item-value="id"
                    label="Category"
                    :rules="basicRules">
                  </v-select>
                </v-flex>
                <v-flex style="margin-top: 30px" xs12 sm6 md4 v-if="update === false">
                  <span class="headline">Metadata</span>
                  <v-text-field
                    v-model="editedItem.metadata.key"
                    label="Name"
                    :rules="basicRules"
                    autofocus
                  ></v-text-field>
                  <v-select
                    v-model="editedItem.metadata.type"
                    :items="metadataTypes"
                    label="Type"
                    :rules="basicRules"
                    @change="editedItem.metadata.value = null"
                  ></v-select>
                  <v-text-field
                    v-if="editedItem.metadata.type !== 'Date'"
                    v-model="editedItem.metadata.value"
                    label="Value"
                    :rules="basicRules"
                  ></v-text-field>
                  <v-menu
                    ref="menu"
                    v-model="menu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    :return-value.sync="editedItem.metadata.value"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                  >
                    <template v-if="editedItem.metadata.type === 'Date'" v-slot:activator="{ on }">
                      <v-text-field
                        v-model="editedItem.metadata.value"
                        label="Value"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="editedItem.metadata.value" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu.save(editedItem.metadata.value)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click="saveFavoriteThing">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <CategoryDialog @setSnackbar="setSnackbar" @getFavoriteThings="getFavoriteThings"/>
    </v-toolbar>
    <v-data-table :headers="headers" :items="favoriteThings" class="elevation-1">
      <template v-slot:items="props">
        <td>{{ props.item.title }}</td>
        <td class="text-xs-left">{{ props.item.description }}</td>
        <td class="text-xs-left">{{ props.item.ranking }}</td>
        <td class="text-xs-left metadataButton"> <MetadataDialog :favoriteThing="props.item"/> </td>
        <td class="text-xs-left">{{ props.item.category.name }}</td>
        <td class="text-xs-left">{{ props.item.created_date }}</td>
        <td class="text-xs-left">{{ props.item.modified_date }}</td>
        <td class="text-xs-left">Logging</td>
        <td class="align-center layout" style="height: 66px;">
          <v-icon small class="mr-2" @click="editItem(props.item)">edit</v-icon>
          <v-icon small @click="deleteItem(props.item)">delete</v-icon>
        </td>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
    <v-snackbar
      v-model="snackbar"
      top
    >
      {{ snackbarResult }}
      <v-btn
        color="#0191A9"
        text
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';
import MetadataDialog from "./MetadataDialog.vue";
import CategoryDialog from "./CategoryDialog.vue";

export default {
  components: {
    MetadataDialog,
    CategoryDialog
  },

  data: () => ({
    menu: false,
    update: false,
    favoriteThingDialog: false,
    snackbar: false,
    headers: [
      {
        text: "Title",
        align: "left",
        sortable: true,
        value: "title"
      },
      { text: "Description", value: "description" },
      { text: "Ranking", value: "ranking" },
      { text: "Metadata", value: "metadata" },
      { text: "Category", value: "category" },
      { text: "Created Date", value: "created_date" },
      { text: "Modified Date", value: "modified_date" },
      { text: "Audit Log", value: "audit_log" },
      { text: "Actions", value: "name" }
    ],
    categories: [],
    favoriteThings: [],
    metadataTypes: ["Text", "Number", "Date"],
    editedIndex: -1,
    editedItem: {
      id: null,
      title: null,
      description: null,
      ranking: null,
      category: null,
      metadata: {
        key: '',
        type: '',
        value: ''
      }
    },
    defaultItem: {
      title: "",
      description: "",
      ranking: 0,
      category: "",
      metadata: {
        key: '',
        type: '',
        value: ''
      },
      created_date: new Date(),
      modified_date: new Date(),
      audit_log: ""
    },
    inMainProgress: false,
    inFavoriteDialogProgress: false,
    progressMessage: "",
    snackbarResult: "",
    basicRules: [
      v => !!v || 'Required field',
    ]
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Favorite Thing" : "Edit Favorite Thing";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.getFavoriteThings();
  },

  methods: {
    getCategories() {
      try {
        this.setFavoriteDialogProgress(true, "Loading Categories...");
        axios
          .get("/api/category")
          .then(response => {
            this.setFavoriteDialogProgress(false, "");
            this.categories = response.data;
          })
          .catch(error => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar("Failed while getting the categories");
            console.log(error);
          });
      } catch (error) {
        this.setFavoriteDialogProgress(false, "");
        this.setSnackbar("Failed while getting the categories");
        console.log(error);
      }
    },

    getFavoriteThings() {
      try {
        this.setMainProgress(true, "Loading Favorite Things...");
        axios.get('/api/favoritething')
          .then(response => {
            this.favoriteThings = response.data;
            this.setMainProgress(false, "");
          })
          .catch(error => {
            this.setMainProgress(false, "");
            this.setSnackbar("Failed while getting the favorite things");
            console.error(error);
          })
      }
      catch(error) {
        this.setMainProgress(false, "");
        this.setSnackbar("Failed while getting the favorite things");
        console.log(error);
      }
    },

    saveFavoriteThing() {
      try {
        if (this.update) {
          this.updateFavoriteThing();
        } else {
          this.setFavoriteDialogProgress(true, "Saving Favorite Thing...");
          axios({
            method: 'post',
            url: '/api/favoritething/',
            headers: {'Content-Type': 'application/json'},
            data: {
              title: this.editedItem.title,
              description: this.editedItem.description,
              ranking: this.editedItem.ranking,
              category_id: this.editedItem.category,
            }
          })
          .then(response => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar("Successfuly created the favorite thing " + response.data.title);
            this.saveMetadata(response.data.id);
            this.cleanFields();
            this.favoriteThingDialog = false;
            this.getFavoriteThings();
          })
          .catch(error => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar("Failed while creating the favorite thing");
            console.log(error);
          });
        }
      }
      catch(error) {
        this.setFavoriteDialogProgress(false, "");
        this.setSnackbar("Failed while creating the favorite thing");
        console.log(error);
      }
    },

    updateFavoriteThing() {
      try {
        this.setFavoriteDialogProgress(true, "Updating Favorite Thing...");
        axios({
          method: 'put',
          url: '/api/favoritething/' + this.editedItem.id + '/',
          headers: {'Content-Type': 'application/json'},
          data: {
            title: this.editedItem.title,
            description: this.editedItem.description,
            ranking: this.editedItem.ranking,
            category_id: this.editedItem.category.id,
          }
        })
        .then(response => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Successfuly updated the favorite thing " + response.data.title);
          this.cleanFields();
          this.favoriteThingDialog = false;
          this.update = false;
          this.editedIndex = -1;
          this.getFavoriteThings();
        })
        .catch(error => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Failed while updating the favorite thing");
          console.log(error);
        });
      }
      catch(error) {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Failed while updating the favorite thing");
          console.log(error);
      }
    },

    deleteFavoriteThing(favoriteThingId) {
      try {
        this.setFavoriteDialogProgress(true, "Deleting Favorite Thing...");
        axios({
          method: 'delete',
          url: '/api/favoritething/' + favoriteThingId + '/',
          headers: {'Content-Type': 'application/json'},
        })
        .then(() => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Successfuly deleted the favorite thing");
          this.cleanFields();
          this.getFavoriteThings();
        })
        .catch(error => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Failed while deleting the favorite thing");
          console.log(error);
        });
      }
      catch(error) {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar("Failed while deleting the favorite thing");
          console.log(error);
      }
    },

    setSnackbar(message) {
      this.snackbar = true;
      this.snackbarResult = message;
    },

    setMainProgress(status, message) {
      this.inMainProgress = status;
      this.progressMessage = message;
    },

    setFavoriteDialogProgress(status, message) {
      this.inFavoriteDialogProgress = status;
      this.progressMessage = message;
    },

    editItem(item) {
      this.getCategories();
      this.editedIndex = this.favoriteThings.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.metadata = {
        key: '',
        type: '',
        value: ''
      }
      this.favoriteThingDialog = true;
      this.update = true;
      this.editedItem.id = item.id;
    },

    deleteItem(item) {
      if (confirm("Are you sure you want to delete this favorite thing?")) {
        this.deleteFavoriteThing(item.id);
      }
    },

    close() {
      this.favoriteThingDialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.favoriteThings[this.editedIndex], this.editedItem);
      } else {
        this.favoriteThings.push(this.editedItem);
      }
      this.close();
    },

    cleanFields() {
      this.editedItem.title = null;
      this.editedItem.description = null;
      this.editedItem.ranking = null;
      this.editedItem.category = null;
    },

    saveMetadata(id) {
      try {
        if (this.editedItem.metadata &&
            this.editedItem.metadata.key &&
            this.editedItem.metadata.type &&
            this.editedItem.metadata.value) {
          this.setFavoriteDialogProgress(true, "Saving Metadata...");
          axios({
            method: "post",
            url: "/api/metadata/",
            headers: { "Content-Type": "application/json" },
            data: {
              key: this.editedItem.metadata.key,
              type: this.editedItem.metadata.type,
              value: this.editedItem.metadata.value,
              favorite_thing: id,
            }
          })
            .then(response => {
              this.editItem.metadata = {
                key: '',
                type: '',
                value: ''
              }
              this.setFavoriteDialogProgress(false, "");
            })
            .catch(error => {
              this.setFavoriteDialogProgress(false, "");
              this.setSnackbar("Failed while creating the metadata");
              console.log(error);
            });
        }
      } catch (error) {
        this.setFavoriteDialogProgress(false, "");
        this.setSnackbar("Failed while creating the metadata");
        console.log(error);
      }
    },
  },
};
</script>
<style>
  .metadataButton {
    padding: 8px !important;
  }
</style>