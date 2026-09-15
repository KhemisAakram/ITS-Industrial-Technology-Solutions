/* ITS Command Center — tiny vanilla behaviours (theme + misc). */
function toggleTheme() {
  document.documentElement.setAttribute(
    "data-theme",
    document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark"
  );
  localStorage.setItem("its-theme", document.documentElement.getAttribute("data-theme"));
}

(function applyTheme() {
  try {
    var t = localStorage.getItem("its-theme");
    if (t) document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
})();

/* ---------------- Kanban drag-and-drop ---------------- */
(function kanbanDragDrop() {
  var kanban = document.getElementById("kanban");
  if (!kanban || !window.fetch) return;
  var dragging = null;

  kanban.addEventListener("dragstart", function (ev) {
    var card = ev.target.closest(".kanban-card");
    if (!card) return;
    dragging = card;
    card.classList.add("dragging");
    ev.dataTransfer.effectAllowed = "move";
    try { ev.dataTransfer.setData("text/plain", card.dataset.wo); } catch (e) {}
  });
  kanban.addEventListener("dragend", function () {
    if (dragging) { dragging.classList.remove("dragging"); dragging = null; }
    document.querySelectorAll(".dropzone").forEach(function (z) { z.classList.remove("drop-over"); });
  });

  kanban.querySelectorAll(".dropzone").forEach(function (zone) {
    zone.addEventListener("dragover", function (ev) {
      ev.preventDefault();
      zone.classList.add("drop-over");
    });
    zone.addEventListener("dragleave", function () { zone.classList.remove("drop-over"); });
    zone.addEventListener("drop", function (ev) {
      ev.preventDefault();
      zone.classList.remove("drop-over");
      if (!dragging) return;
      var wo = dragging.dataset.wo;
      var stage = zone.dataset.stage;
      var oldStage = dragging.dataset.stage;
      if (!wo || !stage || stage === oldStage) return;
      if (stage === "Other") { alert("That column is only for unlisted statuses."); return; }
      if (!confirm("Move work order " + wo + " to “" + stage + "”?")) return;
      var fd = new FormData();
      fd.append("status", stage);
      fetch("/jobs/update/" + encodeURIComponent(wo), { method: "POST", body: fd })
        .then(function () { location.reload(); })
        .catch(function () { location.reload(); });
    });
  });
})();