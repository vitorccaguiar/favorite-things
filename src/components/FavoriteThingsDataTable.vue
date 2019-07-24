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
            <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="categoryDialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn dark color="#0191A9" class="mb-2" v-on="on">New Category</v-btn>
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
            <span class="headline">New Category</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout column>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="category.name" label="Name" :rules="basicRules" autofocus></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="closeCategoryDialog">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click="saveCategory">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-toolbar>
    <v-data-table :headers="headers" :items="favoriteThings" class="elevation-1">
      <template v-slot:items="props">
        <td>{{ props.item.title }}</td>
        <td class="text-xs-left">{{ props.item.description }}</td>
        <td class="text-xs-left">{{ props.item.ranking }}</td>
        <td class="text-xs-left">{{ props.item.metadata }}</td>
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
      this.setMainProgress(true, "Loading Favorite Things...");
      axios.get('/api/favoritething')
        .then(response => {
          this.favoriteThings = response.data;
          this.setMainProgress(false, "");
        })
        .catch(error => {
          console.error(error);
          this.setMainProgress(false, "");
        })
    },

    getCategories() {
      this.setFavoriteDialogProgress(true, "Loading Categories...");
      axios.get('/api/category')
        .then(response => {
          this.setFavoriteDialogProgress(false, "");
          this.categories = response.data;
        })
        .catch(error => {
          console.log(error);
          this.setFavoriteDialogProgress(false, "");
        });
    },

    saveCategory() {
      console.log("Category Name: " + this.category.name);
      this.setCategoryDialogProgress(true, "Saving Category...");
      axios({
        method: 'post',
        url: '/api/category',
        headers: {'Content-Type': 'application/json'},
        data: {
          name: this.category.name,
        }
      })
      .then(response => {
        this.setCategoryDialogProgress(false, "");
        this.setSnackbar(true, "Successfuly created the category " + response.data.name);
        console.log(response);
      })
      .catch(error => {
        this.setCategoryDialogProgress(false, "");
        this.setSnackbar(true, "Failed while creating the category");
        console.log(error);
      });
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
      this.editedIndex = this.favoriteThings.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.favoriteThingDialog = true;
    },

    deleteItem(item) {
      const index = this.favoriteThings.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.favoriteThings.splice(index, 1);
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
    }
  }
};
</script>


    