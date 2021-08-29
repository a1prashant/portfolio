$(function () {
  $("#nav-placeholder").load("nav.html");
});

$(function () {
  $("#page-wip-placeholder").load("page-wip.html");
});

$(function () {
  $("#footer-placeholder").load("footer.html");
});

$(function () {
  let fn = "techbit-uml-relations/dependency-by-parameter";
  $("#" + $fn).load($fn + ".plantuml");
});

