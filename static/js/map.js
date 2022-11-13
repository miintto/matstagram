const map = new ol.Map({
  target: "map",
  layers: [
    new ol.layer.Tile({
      name: 'Map',
      source: new ol.source.XYZ({
        url: "http://xdworld.vworld.kr:8080/2d/Base/202002/{z}/{x}/{y}.png"
      }),
    })
  ],
  controls: [],
  view: new ol.View({
    center: ol.proj.fromLonLat([126.98, 37.55]),
    zoom: 13,
  }),
})

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
    $("#filter").hide();
    $("#place-title").html(`<p>` + feature.get("place_name") + `</p>`);
    $("#place-description").html(`<p>` + feature.get("description") + `</p>`);
    let tags = "";
    feature.get("tags").forEach((e) => {
      tags = tags + `<p>#` + e.tag_name + `</p>`;
    });
    $("#place-tags").html(tags);
  }
});

$(".place-info-component").click((e) => {
  $("#place-info").hide();
})

$("#button-filter").click((e) => {
  if ($(".filter-tag-list").find(".filter-tag-section").length == 0) {
    requestTagList();
  }
  $("#place-info").hide();
  $("#filter").show();
})

const deactivateTag = (target) => {
  target.removeClass("filter-tag-active");
  target.addClass("filter-tag-inactive");
}

const activateTag = (target) => {
  target.removeClass("filter-tag-inactive");
  target.addClass("filter-tag-active");
}

const choiceFilterTag = (e) => {
  const target = $(e.currentTarget);
  if (target.hasClass("filter-tag-active")) {
    deactivateTag(target);
  } else {
    if (target.index(0) === 0) {
      deactivateTag($(".filter-tag-normal"))
    } else {
      deactivateTag($("#filter-tag-all"));
    }
    activateTag(target);
  }
}

$("#button-apply-filter").click((e) => {
  let tagList = [];
  $(".filter-tag-active").each((idx, tag) => {
    tagList.push($(tag).find(".filter-tag-id").text());
  });
  map.getLayers().getArray()
    .filter(layer => layer.get("name") === "Marker")
    .forEach(layer => map.removeLayer(layer));
  requestDisplayPlaces({tags: tagList.join(",")});
  $("#filter").hide();
})

$("#button-cancel-filter").click((e) => {
  $("#filter").hide();
})

$("#button-logout").click((e) => {
  window.location.replace("/");
})
