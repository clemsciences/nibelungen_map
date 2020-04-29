


var myMap = L.map("map-id").setView([51.6, 6.2], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution: "openstreetmap contributors"})
    .addTo(myMap);