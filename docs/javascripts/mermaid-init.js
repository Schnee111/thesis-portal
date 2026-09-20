/* mermaid-init.js — render diagram mermaid dan ikut tema terang/gelap.
   Alasan (R-31): blok ```mermaid di progres.md tampil sebagai teks mentah
   karena pustaka mermaid dimuat tanpa pernah diinisialisasi. Skrip ini
   menginisialisasi tiap navigasi (kompatibel navigation.instant) dan
   me-render ulang saat pengguna mengganti tema. Jika pustaka gagal
   dimuat (misal luring), blok tetap terbaca sebagai kode (fallback aman). */
(function () {
  "use strict";

  function colorScheme() {
    var attr = document.body && document.body.getAttribute("data-md-color-scheme");
    return attr || "slate";
  }

  function render() {
    if (!window.mermaid) return;
    var nodes = Array.prototype.slice.call(document.querySelectorAll("pre.mermaid"));
    if (!nodes.length) return;
    nodes.forEach(function (el) {
      if (!el.getAttribute("data-mermaid-src")) {
        el.setAttribute("data-mermaid-src", el.textContent);
      } else if (el.getAttribute("data-processed")) {
        el.removeAttribute("data-processed");
        el.textContent = el.getAttribute("data-mermaid-src");
      }
    });
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: colorScheme() === "slate" ? "dark" : "default",
        securityLevel: "loose"
      });
      window.mermaid.run({ nodes: nodes });
    } catch (e) {
      /* biarkan blok kode apa adanya */
    }
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(render);
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
  window.addEventListener("load", render);

  if (window.MutationObserver && document.body) {
    var last = colorScheme();
    new MutationObserver(function () {
      var now = colorScheme();
      if (now !== last) {
        last = now;
        render();
      }
    }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }
})();
