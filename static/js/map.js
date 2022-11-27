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
  if ($("#filter-tag-list").find(".tag-label-section").length == 0) {
    requestTagList();
  };
  $("#place-info").hide();
  $("#filter").show();
});

const deactivateTag = (target) => {
  target.removeClass("filter-tag-active");
  target.addClass("filter-tag-inactive");
};

const activateTag = (target) => {
  target.removeClass("filter-tag-inactive");
  target.addClass("filter-tag-active");
};

const choiceFilterTag = (e) => {
  const target = $(e.currentTarget);
  if (target.hasClass("filter-tag-active")) {
    deactivateTag(target);
    if ($(".filter-tag-active").length === 0) {
      activateTag($("#filter-tag-all"));
    };
  } else {
    if (target.index(0) === 0) {
      deactivateTag($(".filter-tag-normal"));
    } else {
      deactivateTag($("#filter-tag-all"));
    };
    activateTag(target);
  };
};

$("#button-apply-filter").click((e) => {
  let tagList = [];
  $(".filter-tag-active").each((idx, tag) => {
    tagList.push($(tag).find(".filter-tag-id").text());
  });
  map.getLayers().getArray()
    .filter(layer => layer.get("name") === "Marker")
    .forEach(layer => map.removeLayer(layer));
  displayPlaces({tags: tagList.join(",")});
  $("#filter").hide();
});

$("#button-cancel-filter").click((e) => { $("#filter").hide(); });

$("#button-logout").click((e) => { window.location.replace("/"); });

const displayMyPlace = (tags) => {
  requestPlaceList(
    queryParams = tags,
    successFunc = (data) => {
      const places = data["data"];
      let placeComponent = "";
      for (let i = 0; i < places.length; i++) {
        const tags = concatTag(places[i].tags);
        placeComponent = placeComponent + `
        <div class="place-info-component">
          <div class="place-info-section image-section">
            <img src="/static/img/place-blank.jpg" width="120">
          </div>
          <div class="place-info-section">
            <div class="place-title">
              <p>` + places[i].place_name + `</p>
            </div>
            <div class="place-description">
              <p>` + places[i].description + `</p>
            </div>
            <div class="place-tags">` + tags + `</div>
          </div>
        </div>`
      }
      $("#my-place-content").html(placeComponent);
    }
  )
}

$("#button-my-place").click((e) => {
  $("#filter").hide();
  $("#place-info").hide();
  $("#my-place").show();
  if ($("#my-place-content:has(div)").length === 0) {
    displayMyPlace({});
  }
});

$("#button-profile").click((e) => {
  $("#profile").show();
  $("#my-place").css("position", "fixed");
  if ($("#profile-user-name:has(p)").length === 0) {
    requestUserProfile();
  }
});

$("#button-register-place").click((e) => {
  $("#my-place").hide();
});

$("#button-close-profile").click((e) => {
  $("#my-place").css("position", "");
  $("#profile").hide();
});

$("#button-close-my-place").click((e) => { $("#my-place").hide(); });
