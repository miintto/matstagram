const requestDisplayPlaces = () => {
  $.ajax({
    url: "/api/place",
    type: "GET",
    dataType: "JSON",
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: (data) => {
      const places = data["data"]
      for (let i = 0; i < places.length; i++) {
        feature = createFeature(places[i])
        markerSource.addFeature(feature);
      }
      markerLayer = new ol.layer.Vector({
        source: markerSource,
        style: markerStyle,
      });
      map.addLayer(markerLayer);
    },
    fail: (err) => {
      console.log(err);
    }
  });
};
