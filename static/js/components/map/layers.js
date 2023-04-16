const map = new ol.Map({
  target: "map",
  layers: [
    new ol.layer.Tile({
      name: "Map",
      source: new ol.source.XYZ({
          projection : 'EPSG:3857',
          url : 'http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}'
      }),
//      source: new ol.source.XYZ({
//        url: "http://xdworld.vworld.kr:8080/2d/Base/202002/{z}/{x}/{y}.png"
//      }),
    })
  ],
  controls: [],
  view: new ol.View({
    center: ol.proj.fromLonLat([141.352, 43.06]),
    zoom: 15,
  }),
});

var markerStyle = new ol.style.Style({
  image: new ol.style.Icon({
    opacity: 1,
    scale: .7,
    src: "/static/img/icon-restaurant.png"
  }),
  zindex: 10,
});

const createFeature = (place) => {
  var feature = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([place.lng, place.lat])),
    place_name: place.place_name,
    description: place.description,
    image_url: place.image_url,
    tags: place.tags,
  });
  return feature
};

map.on("click", (e) => {
  var feature = map.forEachFeatureAtPixel(e.pixel, (f) => { return f; });
  if (feature) {
    $("#place-info").show();
    $("#filter").hide();
    if (feature.get("image_url") !== null) {
      $("#place-info-image").attr("src", feature.get("image_url"));
    } else {
      $("#place-info-image").attr("src", "static/img/place-blank.jpg");
    }
    $("#place-title").html(`<p>` + feature.get("place_name") + `</p>`);
    $("#place-description").html(`<p>` + feature.get("description") + `</p>`);
    const tags = concatTag(feature.get("tags"))
    $("#place-tags").html(tags);
  };
});
