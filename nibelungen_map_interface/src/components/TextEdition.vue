<template>
  <div id="text-edition">
    <div class="d-flex align-items-center my-2">
      <label for="edition-chapter" class="me-2 mb-0">Chapter</label>
      <BFormSelect id="edition-chapter" v-model="selectedChapter" :options="chapterOptions" size="sm"></BFormSelect>
    </div>
    <p class="small text-muted">
      Click on a <span class="place located">place name</span> to display it on the map.
      <span class="place">Underlined names</span> could not be located.
    </p>
    <div class="edition-text">
      <p v-if="loading" class="text-muted">Loading…</p>
      <div v-for="line in lines" :key="line.line" class="edition-line">
        <span class="line-number">{{ line.line }}</span>
        <span v-for="(halfLine, halfLineIndex) in line.halfLines" :key="halfLineIndex" class="half-line">
          <template v-for="(token, tokenIndex) in halfLine" :key="tokenIndex">
            <span v-if="token.place"
                  :class="['place', {located: token.place.located, selected: token.place.name === selectedPlace}]"
                  :title="token.place.name"
                  @click="selectPlace(token.place)">{{ token.token }}</span>
            <span v-else>{{ token.token }}</span>
            {{ " " }}
          </template>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'TextEdition',
    emits: ["select-place"],
    data: function() {
      return {
        selectedChapter: 1,
        textSize: 0,
        lines: [],
        loading: false,
        selectedPlace: null
      }
    },
    computed: {
      chapterOptions() {
        return Array.from({length: this.textSize}, (_, i) => ({value: i + 1, text: `Chapter ${i + 1}`}));
      }
    },
    mounted() {
      this.retrieveTextSize();
      this.retrieveChapter();
    },
    methods: {
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
      retrieveChapter() {
        this.loading = true;
        axios.post("/text/chapter/", {chapter: this.selectedChapter}).then(
                (response) => {
                  if(!response.data.error && response.data.result) {
                    this.lines = response.data.result;
                  }
                }
        ).catch(
            (reason => console.log(reason))
        ).finally(() => {
          this.loading = false;
        });
      },
      selectPlace(place) {
        if(place.located) {
          this.selectedPlace = place.name;
          this.$emit("select-place", place.name);
        }
      }
    },
    watch: {
      selectedChapter: function() {
        this.retrieveChapter();
      }
    }
  }
</script>

<style scoped>
.edition-text {
  height: 550px;
  overflow-y: auto;
  font-family: Georgia, serif;
}
.edition-line {
  display: flex;
  line-height: 1.6;
}
.line-number {
  flex: 0 0 3em;
  color: #999;
  font-size: 0.8em;
  text-align: right;
  padding-right: 1em;
  padding-top: 0.2em;
}
.half-line {
  flex: 1 1 50%;
}
.place {
  text-decoration: underline dotted;
}
.place.located {
  color: #2a7a52;
  font-weight: bold;
  text-decoration: none;
  cursor: pointer;
}
.place.located:hover, .place.selected {
  background-color: #d8f0e2;
}
</style>
