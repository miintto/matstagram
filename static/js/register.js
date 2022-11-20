const requestSignup = (userEmail, password, passwordCheck) => {
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
    success: (data, textStatus, xhr) => {
      const accessToken = data["data"]["access"];
      setCookie("access", accessToken);
      window.location.replace("/map");
    },
    error: (data, textStatus, xhr) => {
      $('.exception-message').text(data.responseJSON["message"]);
    }
  });
}

const submitRegister = () => {
  const userEmail = document.getElementById("input-user-email");
  const password = document.getElementById("input-password");
  const passwordCheck = document.getElementById("input-password-check");
  requestSignup(userEmail.value, password.value, passwordCheck.value);
}

const onkeyupRegister = () => {
	if (window.event.keyCode == 13) {
    submitRegister();
  }
}
