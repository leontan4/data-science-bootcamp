// Creating map object
var myMap = L.map("map", {
    center: [40.7, -73.95],
    zoom: 6
  });
  
  // Adding tile layer to the map
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
  }).addTo(myMap);
  
  // Store API query variables
  var baseURL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson";
  
  // Assemble API query URL
  var url = baseURL

  // Grab the data with d3
  d3.json(url, function(error, data) {
    
    var all_data = data.features;

    var coord= [];
    var magnitude = [];

    for (var i = 0; i < all_data.length; i++) {

      // Set the data location property to a variable
      var location = all_data[i].geometry;
      var mag = all_data[i].properties;

      var color = "";
        if (mag.mag > 5) {
          color = "	#ff0000";
        }
        else if (mag.mag > 4) {
          color = "#ff4000";
        }
        else if (mag.mag > 3) {
          color = "#ff8000";
        }

        else if (mag.mag > 2) {
          color = "#ffbf00";
        }

        else if (mag.mag > 1) {
          color = "#ffff00";
        }

        else {
          color = "#bfff00";
        }
      // Check for location property
      var circle = L.circle([location.coordinates[1], location.coordinates[0]], {
          fillOpacity: 1,
          color: color,
          fillColor:color,
          radius: (mag.mag)*5000 }).addTo(myMap);
    
        // Add a new marker to the cluster group and bind a pop-up
        coord.push([location.coordinates[1], location.coordinates[0]]);
        magnitude.push(all_data[i].properties.mag);
      
    }
  });