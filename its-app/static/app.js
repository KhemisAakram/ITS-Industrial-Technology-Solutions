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