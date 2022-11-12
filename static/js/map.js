const map = new ol.Map({
  target: "map",
  layers: [
    new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: "http://xdworld.vworld.kr:8080/2d/Base/202002/{z}/{x}/{y}.png"
      })
    })
  ],
  controls: [],
  view: new ol.View({
    center: ol.proj.fromLonLat([126.95, 37.55]),
    zoom: 13,
  }),
})

var markerSource = new ol.source.Vector();
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
    tags: place.tags,
  });
  return feature
}

map.on("click", (e) => {
  var feature = map.forEachFeatureAtPixel(e.pixel, (feature) => { return feature; });
  if (feature) {
    $("#place-info").show();
    $("#place-title").html(`<p>` + feature.get("place_name") + `</p>`);
    $("#place-description").html(`<p>` + feature.get("description") + `</p>`);
    let tags = ""
    feature.get("tags").forEach((e) => {
      tags = tags + `<p>#` + e.tag_name + `</p>`;
    });
    $("#place-tags").html(tags);
  }
});

$(".place-info-component").click((e) => {
  $(".place-info").hide();
})

$("#button-logout").click((e) => {
  window.location.replace("/");
})
