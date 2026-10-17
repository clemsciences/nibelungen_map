import { createApp } from 'vue'
import { createBootstrap } from 'bootstrap-vue-next'
import axios from 'axios'
import L from 'leaflet'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

import App from './App.vue'

// Leaflet guesses its marker image paths from its CSS, which breaks once bundled
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow
})

axios.defaults.baseURL = import.meta.env.VITE_SITE_API_URL

createApp(App).use(createBootstrap()).mount('#app')
