<template>
  <v-app id="app">
    <v-toolbar dark color="#0191A9">
      <v-layout align-center justify-center fill-height>
        <v-toolbar-title class="white--text">Favorite Things</v-toolbar-title>
      </v-layout>
    </v-toolbar>

    <FavoriteThingsDataTable></FavoriteThingsDataTable>

    <v-footer height="auto" color="#0191A9">
      <v-layout justify-center row fill-height>
        <v-flex py-4 text-xs-center white--text xs12>
          &copy;2019 —
          <strong>Vitor Aguiar</strong>
        </v-flex>
      </v-layout>
    </v-footer>
  </v-app>
</template>

<script>
import FavoriteThingsDataTable from "./components/FavoriteThingsDataTable.vue";
import MetadataDialog from "./components/MetadataDialog.vue";

export default {
  components: {
    FavoriteThingsDataTable,
    MetadataDialog
  }
};
</script>

<style>
</style>
