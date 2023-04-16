const submitRegister = () => {
  requestSignup(
    userEmail = document.getElementById("input-user-email").value,
    password = document.getElementById("input-password").value,
    passwordCheck = document.getElementById("input-password-check").value,
    successFunc = (data, textStatus, xhr) => {
      const accessToken = data["data"]["access"];
      setCookie("access", accessToken);
      location.replace("/map");
    },
    errorFunc = (data, textStatus, xhr) => {
      $('.exception-message').text(data.responseJSON["message"]);
    }
  );
};

$("#button-submit-register").click((e) => {
  submitRegister();
});

$("#button-register-back").click((e) => {
  location.href = "/";
});

const onkeyupRegister = () => {
	if (window.event.keyCode === 13) {
    submitRegister();
  }
}
