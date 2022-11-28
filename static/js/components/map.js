const map = new ol.Map({
  target: "map",
  layers: [
    new ol.layer.Tile({
      name: "Map",
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
    tags: place.tags,
  });
  return feature
};

const displayPlaces = (tags) => {
  requestPlaceList(
    queryParams = tags,
    successFunc = (data) => {
      const places = data["data"]
      var markerSource = new ol.source.Vector();
      for (let i = 0; i < places.length; i++) {
        feature = createFeature(places[i])
        markerSource.addFeature(feature);
      }
      markerLayer = new ol.layer.Vector({
        name: "Marker",
        source: markerSource,
        style: markerStyle,
      });
      map.addLayer(markerLayer);
    }
  )
}

const concatTag = (tagArray) => {
    let tags = "";
    tagArray.forEach((e) => {
      tags = tags + `<p>#` + e.tag_name + `</p>`;
    });
    return tags
}

map.on("click", (e) => {
  var feature = map.forEachFeatureAtPixel(e.pixel, (f) => { return f; });
  if (feature) {
    $("#place-info").show();
    $("#filter").hide();
    $("#place-title").html(`<p>` + feature.get("place_name") + `</p>`);
    $("#place-description").html(`<p>` + feature.get("description") + `</p>`);
    const tags = concatTag(feature.get("tags"))
    $("#place-tags").html(tags);
  };
});

$(".place-info-component").click((e) => { $("#place-info").hide(); });

$("#button-filter").click((e) => {
  if ($("#filter-tag-list").find(".tag-label-section").length === 0) {
    requestTagList(
      successFunc = (data) => {
        let tags = `
        <div id="filter-tag-all" class="tag-label-section filter-tag-active" onclick="choiceFilterTag(event)">
          <p>전체 선택</p>
        </div>`;
        data["data"].forEach((data) => {
          tags = tags + `
          <div class="tag-label-section filter-tag-inactive filter-tag-normal" onclick="choiceFilterTag(event)">
            <div class="filter-tag-id">` + data.id + `</div>
            <p>#` + data.tag_name + `</p>
          </div>`;
        });
        $("#filter-tag-list").html(tags);
      }
    );
  };
  $("#place-info").hide();
  $("#filter").show();
});

$("#button-my-place").click((e) => {
  $("#filter").hide();
  $("#place-info").hide();
  $("#my-place").show();
  if ($("#my-place-content:has(div)").length === 0) {
    displayMyPlace({});
  }
});

$("#button-logout").click((e) => { window.location.replace("/"); });
