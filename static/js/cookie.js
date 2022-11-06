const setCookie = (cookie_name, value) => {
  document.cookie = cookie_name + "=" + value;
};

const getCookie = (key) => {
  var x, y;
  var val = document.cookie.split(";");

  for (let i = 0; i < val.length; i++) {
    x = val[i].substr(0, val[i].indexOf("="));
    y = val[i].substr(val[i].indexOf("=") + 1);
    x = x.replace(/^\s+|\s+$/g, "");
    if (x == key) {
      return unescape(y);
    }
  }
}

const getAuthToken = () => {
  const token = getCookie("access");
  if (token === undefined) {
    window.location.replace("/");
  }
  return token;
}
