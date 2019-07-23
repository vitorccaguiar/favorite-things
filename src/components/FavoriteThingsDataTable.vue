<template>
  <v-container>
    <v-toolbar flat color="white">
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn dark color="#0191A9" class="mb-2" v-on="on">New Favorite Thing</v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.title" label="Title"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.description" label="Description"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.ranking" label="Ranking"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.category" label="Category"></v-text-field>
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
  </v-container>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  data: () => ({
    dialog: false,
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
    editedIndex: -1,
    editedItem: {
      title: "",
      description: "",
      ranking: 0,
      category: "",
      metadata: ""
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
    }
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
      const axiosInstance = axios.create({
        baseURL: '/api',
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        validateStatus: function(status) {
          return true;
        }
      })
      axiosInstance.get('/favoritething')
        .then(response => {
          console.log(response);
          this.favoriteThings = response.data;
        })
        .catch(e => {
          console.error(e);
        })
    },

    editItem(item) {
      this.editedIndex = this.favoriteThings.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.favoriteThings.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.favoriteThings.splice(index, 1);
    },

    close() {
      this.dialog = false;
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
    }
  }
};
</script>


    
