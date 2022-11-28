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

const requestUpdateProfile = (userName, userEmail, profileImage, successFunc, errorFunc) => {
  $.ajax({
    url: "/api/user",
    type: "PATCH",
    dataType: "JSON",
    contentType: "application/json;",
    data: JSON.stringify({
      "user_name": userName,
      "user_email": userEmail,
      "profile_image": profileImage,
    }),
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    error: errorFunc,
  });
};

const requestUploadProfileImage = (data, successFunc, errorFunc) => {
  $.ajax({
    url: "/api/user/image",
    type: "POST",
    processData: false,
    contentType: false,
    data: data,
    beforeSend: (xhr) => {
      const token = getAuthToken();
      xhr.setRequestHeader("Authorization", "JWT " + token)
    },
    success: successFunc,
    error: errorFunc,
  });
};
