const requestDisplayPlaces = (queryParams) => {
  $.ajax({
    url: "/api/place",
    type: "GET",
    dataType: "JSON",
    data: queryParams,
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: (data) => {
      const places = data["data"]
      var markerSource = new ol.source.Vector();
      for (let i = 0; i < places.length; i++) {
        feature = createFeature(places[i])
        markerSource.addFeature(feature);
      }
      markerLayer = new ol.layer.Vector({
        name: 'Marker',
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

const requestTagList = () => {
  $.ajax({
    url: "/api/tag",
    type: "GET",
    dataType: "JSON",
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: (data) => {
      let tags = `
      <div id="filter-tag-all" class="filter-tag-section filter-tag-active" onclick="choiceFilterTag(event)">
        <p>전체 선택</p>
      </div>`;
      data["data"].forEach((data) => {
        tags = tags + `
        <div class="filter-tag-section filter-tag-inactive filter-tag-normal" onclick="choiceFilterTag(event)">
          <div class="filter-tag-id">` + data.id + `</div>
          <p>#` + data.tag_name + `</p>
        </div>`;
      });
      $(".filter-tag-list").html(tags);
    },
    fail: (err) => {
      console.log(err);
    }
  });
};
