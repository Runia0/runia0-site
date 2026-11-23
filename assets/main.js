// Project filter. Without JavaScript every project stays visible.
(function () {
  var buttons = document.querySelectorAll(".filters button");
  if (!buttons.length) return;
  var cards = document.querySelectorAll(".card");
  var groups = document.querySelectorAll("[data-group-section]");
  var empty = document.querySelector(".empty");
  var status = document.getElementById("filter-status");
  var isTr = document.documentElement.lang === "tr";

  function apply(filter) {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = filter === "all" ||
        c.dataset.group === filter ||
        (" " + c.dataset.cats + " ").indexOf(" " + filter + " ") !== -1;
      c.hidden = !ok;
      if (ok) shown++;
    });
    groups.forEach(function (g) {
      g.hidden = !g.querySelector(".card:not([hidden])");
    });
    if (empty) empty.hidden = shown !== 0;
    if (status) status.textContent = isTr ? shown + " proje gösteriliyor" : shown + " projects shown";
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      buttons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      apply(b.dataset.filter);
    });
  });
})();
