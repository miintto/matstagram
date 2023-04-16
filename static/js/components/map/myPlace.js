const drawMyPlace = (places) => {
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
      if (places[i].image_url == null) {
        placeImageUrl = "/static/img/place-blank.jpg";
      } else {
        placeImageUrl = places[i].image_url;
      }
      console.log(placeImageUrl)
      placeComponent = placeComponent + `
      <div class="place-info-component">
        <div class="place-info-section image-section">
          <img src=` + placeImageUrl + ` width="120" height="120">
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
  return placeComponent
}

const displayMyPlace = (tags) => {
  requestPlaceList(
    queryParams = tags,
    successFunc = (data) => {
      const placeComponent = drawMyPlace(data["data"]);
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
