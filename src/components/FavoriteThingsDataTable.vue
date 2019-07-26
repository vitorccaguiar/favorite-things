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
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.metadata" label="Metadata"></v-text-field>
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
      <v-dialog v-model="categoryDialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn @click="initCategoryDialog" dark color="#0191A9" class="mb-2" v-on="on">Manage Category</v-btn>
        </template>
        <v-card>
          <div v-if="inCategoryDialogProgress">
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
            <span class="headline">Manage Category</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout column>
                <v-flex xs12 sm6 md4>
                  <v-radio-group v-model="radioGroup" row @change="getButtonMessage">
                    <v-radio
                      label="New"
                      value="1"
                    ></v-radio>
                    <v-radio
                      label="Update"
                      value="2"
                    ></v-radio>
                    <v-radio
                      label="Delete"
                      value="3"
                    ></v-radio>
                  </v-radio-group>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-select
                    v-model="category.id"
                    v-if="radioGroup > 1"
                    :items="categories"
                    item-text="name"
                    item-value="id"
                    label="Select a category">
                  </v-select>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-if="radioGroup != 3" v-model="category.name" label="Name" :rules="basicRules" autofocus></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="closeCategoryDialog">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click="categoryAction">{{radioGroupMessage}}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="metadataDialog" max-width="500px">
        <v-card>
          <div v-if="inMetadataDialogProgress">
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
                  <v-radio-group v-model="metadataRadioGroup" row @change="getButtonMessage">
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
            <v-btn color="blue darken-1" flat @click="metadataAction">{{metadataRadioGroupMessage}}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-toolbar>
    <v-data-table :headers="headers" :items="favoriteThings" class="elevation-1">
      <template v-slot:items="props">
        <td>{{ props.item.title }}</td>
        <td class="text-xs-left">{{ props.item.description }}</td>
        <td class="text-xs-left">{{ props.item.ranking }}</td>
        <td class="text-xs-left metadataButton"><v-btn @click="initMetadataDialog" dark class="mb-2" color="#0191A9">View</v-btn></td>
        <td class="text-xs-left">{{ props.item.category.name }}</td>
        <td class="text-xs-left">{{ props.item.created_date }}</td>
        <td class="text-xs-left">{{ props.item.modified_date }}</td>
        <td class="text-xs-left">{{ props.item.audit_log }}</td>
        <td class="justify-center align-center layout px-0">
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

export default {
  data: () => ({
    update: false,
    radioGroup: 1,
    radioGroupMessage: 'Save',
    metadataDialog: false,
    favoriteThingDialog: false,
    categoryDialog: false,
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
    favoriteThings: [],
    categories: [],
    editedIndex: -1,
    editedItem: {
      id: null,
      title: null,
      description: null,
      ranking: null,
      category: null,
      metadata: null
    },
    defaultItem: {
      title: "",
      description: "",
      ranking: 0,
      category: "",
      metadata: "",
      created_date: new Date(),
      modified_date: new Date(),
      audit_log: ""
    },
    category: {
      id: null,
      name: null
    },
    inMainProgress: false,
    inFavoriteDialogProgress: false,
    inCategoryDialogProgress: false,
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
    this.initialize();
  },

  methods: {
    initialize() {
      this.getFavoriteThings();
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
            this.setSnackbar(true, "Failed while getting the favorite things");
            console.error(error);
          })
      }
      catch(error) {
        this.setMainProgress(false, "");
        this.setSnackbar(true, "Failed while getting the favorite things");
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
              audit_log: "Loging",
            }
          })
          .then(response => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar(true, "Successfuly created the favorite thing " + response.data.title);
            this.editedItem.title = null;
            this.editedItem.description = null;
            this.editedItem.ranking = null;
            this.editedItem.category = null;
            this.editedItem.metadata = null;
            this.favoriteThingDialog = false;
            this.getFavoriteThings();
          })
          .catch(error => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar(true, "Failed while creating the favorite thing");
            console.log(error);
          });
        }
      }
      catch(error) {
        this.setFavoriteDialogProgress(false, "");
        this.setSnackbar(true, "Failed while creating the favorite thing");
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
            audit_log: "Loging"
          }
        })
        .then(response => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Successfuly updated the favorite thing " + response.data.title);
          this.favoriteThingDialog = false;
          this.update = false;
          this.editedIndex = -1;
          this.getFavoriteThings();
        })
        .catch(error => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Failed while updating the favorite thing");
          console.log(error);
        });
      }
      catch(error) {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Failed while updating the favorite thing");
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
        .then(response => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Successfuly deleted the favorite thing");
          this.editedItem.title = null;
          this.editedItem.description = null;
          this.editedItem.ranking = null;
          this.editedItem.category = null;
          this.editedItem.metadata = null;
          this.getFavoriteThings();
        })
        .catch(error => {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Failed while deleting the favorite thing");
          console.log(error);
        });
      }
      catch(error) {
          this.setFavoriteDialogProgress(false, "");
          this.setSnackbar(true, "Failed while deleting the favorite thing");
          console.log(error);
      }
    },

    getCategories() {
      try {
        this.setFavoriteDialogProgress(true, "Loading Categories...");
        axios.get('/api/category')
          .then(response => {
            this.setFavoriteDialogProgress(false, "");
            this.categories = response.data;
          })
          .catch(error => {
            this.setFavoriteDialogProgress(false, "");
            this.setSnackbar(true, "Failed while getting the categories");
            console.log(error);
          });
      }
      catch(error) {
        this.setFavoriteDialogProgress(false, "");
        this.setSnackbar(true, "Failed while getting the categories");
        console.log(error);
      }
    },

    saveCategory() {
      try {
        this.setCategoryDialogProgress(true, "Saving Category...");
        axios({
          method: 'post',
          url: '/api/category/',
          headers: {'Content-Type': 'application/json'},
          data: {
            name: this.category.name,
          }
        })
        .then(response => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Successfuly created the category " + response.data.name);
          this.category.name = null;
        })
        .catch(error => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Failed while creating the category");
          console.log(error);
        });
      }
      catch(error) {
        this.setCategoryDialogProgress(false, "");
        this.setSnackbar(true, "Failed while creating the category");
        console.log(error);
      }
    },

    updateCategory() {
      try {
        this.setCategoryDialogProgress(true, "Updating Category...");
        axios({
          method: 'put',
          url: '/api/category/' + this.category.id + '/',
          headers: {'Content-Type': 'application/json'},
          data: {
            name: this.category.name,
          }
        })
        .then(response => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Successfuly updated the category " + response.data.name);
          this.category.name = null;
        })
        .catch(error => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Failed while updating the category");
          console.log(error);
        });
      }
      catch(error) {
        this.setCategoryDialogProgress(false, "");
        this.setSnackbar(true, "Failed while updating the category");
        console.log(error);
      }
    },

    deleteCategory() {
      try {
        this.setCategoryDialogProgress(true, "Deleting Category...");
        axios({
          method: 'delete',
          url: '/api/category/' + this.category.id + '/',
          headers: {'Content-Type': 'application/json'},
        })
        .then(response => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Successfuly deleted the category");
          this.category.name = null;
        })
        .catch(error => {
          this.setCategoryDialogProgress(false, "");
          this.setSnackbar(true, "Failed while deleting the category");
          console.log(error);
        });
      }
      catch(error) {
        this.setCategoryDialogProgress(false, "");
        this.setSnackbar(true, "Failed while deleting the category");
        console.log(error);
      }
    },

    setSnackbar(status, message) {
      this.snackbar = status;
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

    setCategoryDialogProgress(status, message) {
      this.inCategoryDialogProgress = status;
      this.progressMessage = message;
    },

    editItem(item) {
      this.getCategories();
      this.editedIndex = this.favoriteThings.indexOf(item);
      this.editedItem = Object.assign({}, item);
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

    closeCategoryDialog() {
      this.categoryDialog = false;
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

    async categoryAction() {
      if (this.radioGroup == 1) {
        this.saveCategory();
      } else if(this.radioGroup == 2) {
        this.updateCategory();
      } else if(this.radioGroup == 3) {
        if (confirm("Are you sure you want to delete this category? " +
            "By deleting this category all related favorite things will be also deleted.")) {
          await this.deleteCategory();
        }
      }
      this.getCategories();
    }
  },

  async initCategoryDialog() {
    await this.getCategories();
    this.radioGroup = 1;
  },

  initMetadataDialog() {
    this.metadataDialog = true;
  }
};
</script>
<style>
  .metadataButton {
    padding: 8px;
  }
</style>