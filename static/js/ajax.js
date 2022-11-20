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
    },
    fail: (err) => {
      console.log(err);
    }
  });
};

const requestUserProfile = () => {
  $.ajax({
    url: "/api/user",
    type: "GET",
    dataType: "JSON",
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: (data) => {
      const userProfile = data["data"];
      $("#profile-user-name").html(`<p>` + userProfile["user_name"] + `</p>`);
      $("#profile-user-email").html(`<p>` + userProfile["user_email"] + `</p>`);
      $("#profile-created-dtm").html(`<p>` + userProfile["created_dtm"] + `</p>`);
      $("#profile-permission").html(`<p>` + userProfile["user_permission"] + `</p>`);
      let tags = "";
      userProfile["tags"].forEach((data) => {
        tags = tags + `
        <div class="tag-label-section filter-tag-active">
          <p>#` + data.tag_name + `</p>
        </div>`;
      });
      $("#profile-tag-list").html(tags);
    },
    error: (err) => {
      $("#profile-user-name").html("<p>null</p>");
      $("#profile-user-email").html("<p>anonymous@miintto.com</p>");
      $("#profile-created-dtm").html("<p>2022-01-01 00:00:00</p>");
      $("#profile-permission").html("<p>anonymous</p>");
    }
  });
};
