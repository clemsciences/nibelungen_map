<template>
  <div id="all-map">
    <BContainer>
      <BRow>
        <p class="m-3">You can select places by type with checkboxes and by chapter with a slider.</p>
      </BRow>
      <BRow>
        <BCol sm="12" md="3" class="m-3">
          <BFormSelect class="my-2" v-model="selectedMode" :options="modeOptions">
          </BFormSelect>
          <div v-if="selectedMode === 'placeType'">
            <BFormCheckboxGroup
                    id="place-types"
                    v-model="selected_places"
                    :options="options"
                    value-field="item"
                    text-field="name">
            </BFormCheckboxGroup>
          </div>
          <div v-if="selectedMode === 'chapter'">
            <label for="range-chapter">Selected chapter {{ selectedChapter }}</label>
            <BFormInput id="range-chapter" v-model.number="selectedChapter" type="range" min="1" :max="textSize"></BFormInput>
          </div>
        </BCol>
      </BRow>
      <BRow>
        <BCol class="m-3">
          <div class="mapclass">
          <div id="map-id"></div>
            </div>
        </BCol>
      </BRow>
    </BContainer>
  </div>
</template>

<script>
  import { markRaw } from 'vue';
  import L from 'leaflet';
  import axios from 'axios';

  export default {
    name: 'PlacesMap',
    data: function() {
      return {
        theMap: null,
        markers: [],
        loadedPlaces: [],
        selected_places: [],
        options: [
          {item: 'city', name: "Cities"},
          {item: "region_country", name: "Regions and countries"},
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
        // Leaflet objects must not be wrapped in Vue reactive proxies
        this.theMap = markRaw(L.map("map-id", {
          zoomControl: true,
          zoomDelta: 0.25,
          zoomSnap: 0
        }));
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
        }).catch(
            (reason => console.log(reason))
        );
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
        ).catch(
            (reason => console.log(reason))
        );
      },
      retrieveTextSize() {
        axios.get("/text/size/").then(
                (response) => {
                  if(response.data.result) {
                    this.textSize = response.data.result;
                  }
                }
        ).catch(
            (reason => console.log(reason))
        )
      },
      retrievePlacesByChapter() {
        return axios.post("/text/place-by-chapter/",
                {chapter: this.selectedChapter}).then(
                (response) => {
                  return response.data.result;
                }
        ).catch(
            (reason => console.log(reason))
        )
      },
      addPlaceMarker(place) {
        let marker = markRaw(L.marker([place.lat, place.lon]).addTo(this.theMap));
        marker.on("click", () => {
          this.retrieveOccurrences(place.placeType, place.name).then(
                  (response) => {
                    let occurrences = response || [];
                    let occurrencesText = occurrences.reduce((acc, currValue) => {
                      return acc+currValue.occurrence+": "+currValue.line.join(" ")+";";
                    }, "")
                    let content = `<div class="own-popup" style="overflow-y: auto; height: 100px;"><h4>${ place.name }</h4>${occurrencesText}</div>`;
                    L.popup()
                    .setLatLng(marker.getLatLng())
                    .setContent(content)
                    .openOn(this.theMap);
                  }
          ).catch(
              (reason => console.log(reason))
          );
        });
        this.markers.push(marker);
        return marker;
      },
      displayPlacesByPlaceType(places, selectedPlaces) {
        places.filter(place => {
          return place != null && selectedPlaces.find(selectedPlace => place.placeType === selectedPlace);
        }).forEach(place => this.addPlaceMarker(place));
      },
      displayPlacesByName(places, selectedPlaceNames) {
        places.filter(place => {
          return place != null && selectedPlaceNames.find(selectedPlace => place.name === selectedPlace);
        }).forEach(place => this.addPlaceMarker(place));
      },
      // Called from the digital edition when a place name is clicked
      focusPlace(placeName) {
        let place = this.loadedPlaces.find(loadedPlace => loadedPlace != null && loadedPlace.name === placeName);
        if(!place) {
          return false;
        }
        this.flushMap();
        let marker = this.addPlaceMarker(place);
        this.theMap.flyTo(marker.getLatLng(), Math.max(this.theMap.getZoom(), 6));
        marker.fire("click");
        return true;
      }
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
      selectedChapter: function() {
        this.flushMap();
        this.retrievePlacesByChapter().then((result => {
          if(result) {
            this.displayPlacesByName(this.loadedPlaces, result);
          }
        }));
      },
      selectedMode:function(newMode) {
        this.flushMap();
        if(newMode === "placeType") {
          this.selected_places = [];
        } else if(newMode === "chapter") {
          this.selectedChapter = 1;
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
  z-index: 800;
}
.mapclass {
  width: 100%;
  height: 550px;
}
.own-popup {
  height: 100px;
  overflow-y: scroll;
  display: inline-block;
}

#all-map {
  background-color: white;
}
</style>
