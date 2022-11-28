const displayUserProfile = () => {
  requestUserProfile(
    successFunc = (data) => {
      const userProfile = data["data"];
      if (userProfile.profile_image !== null) {
        $("#profile-image-section").html(`<img src=` + userProfile.profile_image + `>`);
      }
      $("#profile-user-name").html(`<p>` + userProfile.user_name + `</p>`);
      $("#profile-user-email").html(`<p>` + userProfile.user_email + `</p>`);
      $("#profile-created-dtm").html(`<p>` + userProfile.created_dtm + `</p>`);
      $("#profile-permission").html(`<p>` + userProfile.user_permission + `</p>`);
      let tags = "";
      userProfile.tags.forEach((data) => {
        tags = tags + `
        <div class="tag-label-section filter-tag-active">
          <p>#` + data.tag_name + `</p>
        </div>`;
      });
      $("#profile-tag-list").html(tags);
    },
    errorFunc = (err) => {
      $("#profile-user-name").html("<p>null</p>");
      $("#profile-user-email").html("<p>anonymous@miintto.com</p>");
      $("#profile-created-dtm").html("<p>2022-01-01 00:00:00</p>");
      $("#profile-permission").html("<p>anonymous</p>");
    },
  );
};

const activateUpdateForm = () => {
  $("#profile-image-section-blur").show();
  $("#profile-close-section").hide();
  $("#profile-update-section").show();
  $(".profile-value-updatable").hide();
  $(".profile-update-value").show();
  $("#profile-update").hide();
};

const disableUpdateForm = () => {
  $("#profile-image-section-preview").html("");
  $("#profile-image-section-preview").hide();
  $("#profile-image-section-blur").hide();
  $("#profile-update-section").hide();
  $("#profile-close-section").show();
  $(".profile-update-value").hide();
  $(".profile-value-updatable").show();
  $("#profile-update").show();
};

$("#profile-update").click((e) => {
  activateUpdateForm();
  $("#input-profile-user-name").val($("#profile-user-name").text());
  $("#input-profile-user-email").val($("#profile-user-email").text());
});

$("#button-cancel-update").click((e) => {
  disableUpdateForm();
});

$("#profile-image-section-blur").click((e) => {
  const button = document.getElementById("upload-profile-image");
  button.click();
});

$("#upload-profile-image").change(() => {
  const imageFile = document.getElementById("upload-profile-image").files;
  const formData = new FormData();
  formData.append("profile_image", imageFile[0]);
  requestUploadProfileImage(
    data = formData,
    successFunc = (data) => {
      $("#profile-image-section-preview").html(`<img src=` + data.data + `>`);
      $("#profile-image-section-preview").show();
    },
    errorFunc = (data, textStatus, xhr) => {
      alert(data.responseJSON["message"]);
    },
  );
});

$("#button-save-profile").click((e) => {
  requestUpdateProfile(
    userName = $("#input-profile-user-name").val(),
    userEmail = $("#input-profile-user-email").val(),
    profileImage = $("#profile-image-section-preview>img").attr("src"),
    successFunc = (data) => {
      $("#profile-image-section").html(`<img src=` + data.data.profile_image + `>`);
      $("#profile-user-name").html(`<p>` + data.data.user_name + `</p>`);
      $("#profile-user-email").html(`<p>` + data.data.user_email + `</p>`);
      disableUpdateForm();
    },
    errorFunc = (data, textStatus, xhr) => {
      alert(data.responseJSON["message"]);
    },
  );
});

$("#button-close-profile").click((e) => {
  $("#my-place").css("position", "");
  $("#profile").hide();
});
