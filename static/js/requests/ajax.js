const requestLogin = (userEmail, password, successFunc, errorFunc) => {
  $.ajax({
    url: "/api/auth/login",
    type: "POST",
    dataType: "JSON",
    contentType: "application/json;",
    data: JSON.stringify({
      "user_email": userEmail,
      "password": password,
    }),
    beforeSend: () => {
      $('.exception-message').text("");
    },
    success: successFunc,
    error: errorFunc,
  });
}

const requestSignup = (userEmail, password, passwordCheck, successFunc, errorFunc) => {
  $.ajax({
    url: "/api/auth/signup",
    type: "POST",
    dataType: "JSON",
    contentType: "application/json;",
    data: JSON.stringify({
      "user_email": userEmail,
      "password": password,
      "password_check": passwordCheck,
    }),
    beforeSend: () => {
      $('.exception-message').text("");
    },
    success: successFunc,
    error: errorFunc,
  });
}

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

const requestUserProfile = (successFunc, errorFunc) => {
  $.ajax({
    url: "/api/user",
    type: "GET",
    dataType: "JSON",
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    error: errorFunc,
  });
};

const requestUpdateProfile = (userName, userEmail, successFunc, errorFunc) => {
  $.ajax({
    url: "/api/user",
    type: "PATCH",
    dataType: "JSON",
    contentType: "application/json;",
    data: JSON.stringify({
      "user_name": userName,
      "user_email": userEmail,
    }),
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    error: errorFunc,
  });
};
