const requestPlaceList = (queryParams, successFunc) => {
  $.ajax({
    url: "/api/place",
    type: "GET",
    dataType: "JSON",
    data: queryParams,
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    fail: (err) => {
      console.log(err);
    }
  });
};

const requestTagList = (successFunc) => {
  $.ajax({
    url: "/api/tag",
    type: "GET",
    dataType: "JSON",
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    fail: (err) => {
      console.log(err);
    }
  });
};
