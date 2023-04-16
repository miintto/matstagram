const requestSharePlaceList = (queryParams, successFunc) => {
  $.ajax({
    url: "/api/share/place",
    type: "GET",
    dataType: "JSON",
    data: queryParams,
    success: successFunc,
    fail: (err) => {
      console.log(err);
    }
  });
};
