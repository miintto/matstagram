const submitDocumentLogin = () => {
  requestLogin(
    userEmail = document.getElementById("input-user-email").value,
    password = document.getElementById("input-password").value,
    successFunc = (data, textStatus, xhr) => {
      const accessToken = data["data"]["access"];
      setCookie("access", accessToken);
      location.replace("/documents");
    },
    errorFunc = (data, textStatus, xhr) => {
      $('.exception-message').text(data.responseJSON["message"]);
    },
  );
};

$("#button-login-document").click((e) => {
  submitDocumentLogin();
});

$("#button-document-back").click((e) => {
  location.href = "/";
});

const onkeyupLogin = () => {
	if (window.event.keyCode === 13) {
    submitDocumentLogin();
  }
};
