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

const onClickMyPlace = () => {
  $("#filter").hide();
  $("#place-info").hide();
  $("#my-place").show();
  if ($("#my-place-content:has(div)").length === 0) {
    displayMyPlace({});
  }
};

$("#button-logout").click((e) => { window.location.replace("/"); });
