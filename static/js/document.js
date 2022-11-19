const requestLogin = (userEmail, password) => {
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
    success: (data, textStatus, xhr) => {
      const accessToken = data["data"]["access"];
      setCookie("access", accessToken);
      window.location.replace("/documents");
    },
    error: (data, textStatus, xhr) => {
      $('.exception-message').text(data.responseJSON["message"]);
    }
  });
}

const submitLogin = () => {
  const userEmail = document.getElementById("input-user-email");
  const password = document.getElementById("input-password");
  requestLogin(userEmail.value, password.value);
}

const onkeyupLogin = () => {
	if (window.event.keyCode == 13) {
    submitLogin();
  }
}
