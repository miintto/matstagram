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
