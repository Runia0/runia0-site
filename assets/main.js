// Project filter + search. Without JavaScript every project stays visible.
(function () {
  var buttons = document.querySelectorAll(".filters button");
  var input = document.getElementById("q");
  if (!buttons.length && !input) return;
  var cards = document.querySelectorAll(".card");
  var groups = document.querySelectorAll("[data-group-section]");
  var empty = document.querySelector(".empty");
  var status = document.getElementById("filter-status");
  var filter = "all";

  function norm(s) {
    return (s || "").toLocaleLowerCase(document.documentElement.lang || undefined)
      .normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ı/g, "i");
  }

  function apply() {
    var q = norm(input ? input.value.trim() : "");
    var shown = 0;
    cards.forEach(function (c) {
      var okF = filter === "all" || c.dataset.group === filter ||
        (" " + c.dataset.cats + " ").indexOf(" " + filter + " ") !== -1;
      var okQ = !q || norm(c.dataset.search).indexOf(q) !== -1;
      c.hidden = !(okF && okQ);
      if (!c.hidden) shown++;
    });
    groups.forEach(function (g) { g.hidden = !g.querySelector(".card:not([hidden])"); });
    if (empty) empty.hidden = shown !== 0;
    if (status) status.textContent = shown + " " + (status.dataset.label || "");
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      buttons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      filter = b.dataset.filter;
      apply();
    });
  });
  if (input) input.addEventListener("input", apply);
})();
