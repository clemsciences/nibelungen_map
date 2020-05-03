<template>
  <div class="mapclass">
    <div id="map-id"></div>
  </div>
</template>

<script>
  import 'leaflet/dist/leaflet.css';
  import L from 'leaflet';
  import axios from 'axios';
  axios.defaults.baseURL = "http://localhost:5000";

  export default {
    name: 'Map',
    data: function() {
      return {
        theMap: null,
        markers: [],
        places: []
      }
    },
    mounted() {
      this.setMap();
      this.retrieveData();

      this.theMap.invalidateSize();
    },

    methods: {
      setMap() {
        this.theMap = L.map("map-id", {
          zoomControl: true,
          zoomDelta: 0.25,
          zoomSnap: 0
        });
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'})
        .addTo(this.theMap);
        this.theMap.setView([50, 6], 4);

      },
      retrieveData() {
        axios.get('/places').then(
            (response) => {
                this.places = response.data;
        });
      },
    },
    watch: {
      places: function(newValue) {
        if(newValue) {
          newValue.forEach((value) => {
            console.log(value)
            if(value) {
              let marker = L.marker([value.lat, value.lon]).addTo(this.theMap);
              marker.bindPopup(value.name);
            }
          });
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: #42b983;
}
#map-id {
  width: 100%;
  height: calc(100%);
}
.mapclass {
  width: 800px;
  height: 600px;
}
</style>
