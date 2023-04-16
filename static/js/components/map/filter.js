const deactivateTag = (target) => {
  target.removeClass("filter-tag-active");
  target.addClass("filter-tag-inactive");
};

const activateTag = (target) => {
  target.removeClass("filter-tag-inactive");
  target.addClass("filter-tag-active");
};

const choiceFilterTag = (e) => {
  const target = $(e.currentTarget);
  if (target.hasClass("filter-tag-active")) {
    deactivateTag(target);
    if ($(".filter-tag-active").length === 0) {
      activateTag($("#filter-tag-all"));
    };
  } else {
    if (target.index(0) === 0) {
      deactivateTag($(".filter-tag-normal"));
    } else {
      deactivateTag($("#filter-tag-all"));
    };
    activateTag(target);
  };
};

$("#button-apply-filter").click((e) => {
  let tagList = [];
  $(".filter-tag-active").each((idx, tag) => {
    tagList.push($(tag).find(".filter-tag-id").text());
  });
  map.getLayers().getArray()
    .filter(layer => layer.get("name") === "Marker")
    .forEach(layer => map.removeLayer(layer));
  displayPlaces({tags: tagList.join(",")});
  $("#filter").hide();
});

$("#button-cancel-filter").click((e) => { $("#filter").hide(); });
