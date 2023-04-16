const displaySharePlaces = () => {
  requestSharePlaceList(
    queryParams = {"k": window.location.pathname.split("/").pop()},
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

const displayMyPlaceShared = (tags) => {
  requestSharePlaceList(
    queryParams = {"k": window.location.pathname.split("/").pop()},
    successFunc = (data) => {
      const placeComponent = drawMyPlace(data["data"]);
      $("#my-place-content").html(placeComponent);
    }
  )
}

const onClickMyPlaceShared = () => {
  $("#filter").hide();
  $("#place-info").hide();
  $("#my-place").show();
  if ($("#my-place-content:has(div)").length === 0) {
    displayMyPlaceShared();
  }
};

const onClickCopyURL = () => {
  const textarea = document.createElement("textarea");
  textarea.textContent = window.location.href;
  document.body.append(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
  alert("링크가 복사되었습니다")
}
