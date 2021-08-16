<template>
  <div id="app">
    <b-container>
      <b-row>
        <h2 class="m-3">Nibelungenlied map</h2>
      </b-row>
      <b-row>
        <Map/>
      </b-row>
      <b-row class="mx-3">
        <p>By Clément Besnier <a href="https://www.clementbesnier.eu/">clementbesnier.eu</a> - 06/02/2021</p>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Map from './components/Map.vue'
// import Characters from "./components/Characters";

export default {
  name: 'App',
  components: {
    Map,
    // Characters
  }
}
</script>

<style>

</style>
