const displayMyPlace = (tags) => {
  requestPlaceList(
    queryParams = tags,
    successFunc = (data) => {
      const places = data["data"];
      let placeComponent = "";
      if (places.length === 0) {
        placeComponent = `
        <div class="my-place-blank center">
          <p>등록된 맛집이</p>
          <p>없습니다.</p>
        <div>`
      } else {
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
      }
      $("#my-place-content").html(placeComponent);
    }
  )
}

$("#button-profile").click((e) => {
  $("#profile").show();
  $("#my-place").css("position", "fixed");
  if ($("#profile-user-name:has(p)").length === 0) {
    displayUserProfile();
  }
});

$("#button-register-place").click((e) => {
  $("#my-place").hide();
});

$("#button-close-my-place").click((e) => {
  $("#my-place").hide();
});
