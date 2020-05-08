<template>
  <div>
    <b-container>
      <b-row >
        <b-col cols="9">
          <div class="mapclass">
          <div id="map-id"></div>
            </div>
        </b-col>

        <b-col cols="3">
          <b-form-select v-model="selectedMode" :options="modeOptions">
          </b-form-select>
          <div v-if="selectedMode === 'placeType'">
            <b-form-checkbox-group
                    v-model="selected_places"
                    :options="options"
                    value-field="item"
                    text-field="name">
            </b-form-checkbox-group>
          </div>
          <div v-if="selectedMode === 'chapter'">
            <label for="range-chapter">Selected chapter {{ selectedChapter }}</label>
            <b-form-input id="range-chapter" v-model="selectedChapter" type="range" min="1" :max="textSize"></b-form-input>
          </div>
        </b-col>
      </b-row>
    </b-container>
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
        loadedPlaces: [],
        selected_places: [],
        options: [
          {item: 'city', name: "Cities"},
          {item: "region_country", name: "Regions and countries"},
          {item: "people", name: "Peoples"},
          {item: "river", name: "Rivers"}
        ],
        selectedChapter: 1,
        textSize: 0,
        selectedMode: "placeType",
        modeOptions: [
          {value: "placeType", text: "By place type"},
          {value: "chapter", text: "By chapter"}
        ]
      }
    },
    mounted() {
      this.setMap();
      this.retrieveData();
      this.retrieveTextSize();

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
      flushMap() {
        console.log(this.markers.length);
        this.markers.forEach(marker => {
          marker.removeFrom(this.theMap);
        });
        this.markers = [];
      },
      retrieveData() {
        axios.get('/places/').then(
            (response) => {
              if(response.data.result) {
                this.loadedPlaces = response.data.result;
              }
        });
      },
      retrieveOccurrences(placeType, placeName) {
        console.log(placeName);
        console.log(placeType);
        return axios.post("/get-occurrences/",
                {placeType, placeName}).then(
                (response) => {
                  if(!response.data.error && response.data.result) {
                    return response.data.result;
                  }
                }
        );
      },
      retrieveTextSize() {
        axios.get("/text/size/").then(
                (response) => {
                  if(response.data.result) {
                    this.textSize = response.data.result;
                  }
                }
        )
      },
      retrievePlacesByChapter() {
        return axios.post("/text/place-by-chapter/",
                {chapter: this.selectedChapter}).then(
                (response) => {
                  return response.data.result;
                }
        )
      },
      displayPlacesByPlaceType(places, selectedPlaces) {
        // console.log(selectedPlaces)
        places.filter(place => {
          return place != null && selectedPlaces.find(selectedPlace => place.placeType === selectedPlace);
        }).forEach((value) => {
          // console.log(value)
          if(value) {
            let marker = L.marker([value.lat, value.lon]).addTo(this.theMap);
            marker.on("click", () => {
              this.retrieveOccurrences(value.placeType, value.name).then(
                      (response) => {
                        let occurrences = response;
                        console.log(occurrences);
                        let occurrencesText = occurrences.reduce((acc, currValue) => {
                          return acc+currValue.occurrence+": "+currValue.line.join(" ")+";";
                        }, "")
                        let content = `<div class="own-popup" style="overflow-y: auto; height: 100px;"><h4>${ value.name }</h4>${occurrencesText}</div>`;
                        L.popup()
                        .setLatLng(marker.getLatLng())
                        .setContent(content)
                        .openOn(this.theMap);
                      }
              );
            });
            this.markers.push(marker);
          }
        });
      },
      // displayPlacesByChapter(chapter) {
      //   // console.log(selectedPlaces)
      //   places.filter(place => {
      //     return place != null && selectedPlaces.find(selectedPlace => place.placeType === selectedPlace);
      //   }).forEach((value) => {
      //     // console.log(value)
      //     if(value) {
      //       let marker = L.marker([value.lat, value.lon]).addTo(this.theMap);
      //       marker.on("click", () => {
      //         this.retrieveOccurrences(value.placeType, value.name).then(
      //                 (response) => {
      //                   let occurrences = response;
      //                   console.log(occurrences);
      //                   let occurrencesText = occurrences.reduce((acc, currValue) => {
      //                     return acc+currValue.occurrence+": "+currValue.line.join(" ")+";";
      //                   }, "")
      //                   let content = `<div class="own-popup" style="overflow-y: auto; height: 100px;"><h4>${ value.name }</h4>${occurrencesText}</div>`;
      //                   L.popup()
      //                   .setLatLng(marker.getLatLng())
      //                   .setContent(content)
      //                   .openOn(this.theMap);
      //                 }
      //         );
      //       });
      //       this.markers.push(marker);
      //     }
      //   });
      // }
    },
    watch: {
      places: function(newValue) {
        if(newValue) {
          this.flushMap();
          this.displayPlacesByPlaceType(newValue);
        }
      },
      selected_places: function(newValue) {
        this.flushMap();
        this.displayPlacesByPlaceType(this.loadedPlaces, newValue);
      },
      selectedChapter: function(newValue) {
        this.flushMap();

        this.displayPlacesByChapter(this.loadedPlaces, newValue);
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
  height: 550px;
}
.own-popup {
  height: 100px;
  overflow-y: scroll;
  display: inline-block;
}
</style>
