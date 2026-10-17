<template>
  <div id="app">
    <BContainer fluid>
      <BRow>
        <h2 class="m-3">Nibelungenlied map</h2>
      </BRow>
      <BRow>
        <BCol lg="7">
          <PlacesMap ref="map"/>
        </BCol>
        <BCol lg="5">
          <TextEdition @select-place="showPlace"/>
        </BCol>
      </BRow>
      <BRow class="mx-3">
        <p>By Clément Besnier <a href="https://www.clementbesnier.eu/">clementbesnier.eu</a> - 06/02/2021</p>
      </BRow>
    </BContainer>
  </div>
</template>

<script>
import PlacesMap from './components/PlacesMap.vue'
import TextEdition from './components/TextEdition.vue'
// import Characters from "./components/Characters";

export default {
  name: 'App',
  components: {
    PlacesMap,
    TextEdition,
    // Characters
  },
  methods: {
    showPlace(placeName) {
      this.$refs.map.focusPlace(placeName);
    }
  }
}
</script>

<style>

</style>
