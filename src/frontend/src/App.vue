<template>
  <div id="app">
    <Map/>
    <Characters/>
  </div>
</template>

<script>
import Map from './components/Map.vue'
import Characters from "./components/Characters";

export default {
  name: 'App',
  components: {
    Map,
    Characters
  }
}
</script>

<style>

</style>
