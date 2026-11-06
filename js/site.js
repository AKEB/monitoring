(function () {
  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      nav.classList.toggle("is-open");
      var open = nav.classList.contains("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function markActiveNav() {
    var path = location.pathname.replace(/\/index\.html$/, "/").replace(/\/$/, "") || "/";
    document.querySelectorAll(".site-nav a[href], .docs-sidebar a[href]").forEach(function (link) {
      try {
        var href = link.getAttribute("href");
        if (!href || href.startsWith("http") || href.startsWith("mailto:") || href.startsWith("#")) return;
        var url = new URL(href, location.href);
        var linkPath = url.pathname.replace(/\/index\.html$/, "/").replace(/\/$/, "") || "/";
        if (linkPath === path || (path.endsWith(linkPath) && linkPath.length > 1)) {
          link.classList.add("is-active");
        }
      } catch (e) {
        /* ignore bad urls */
      }
    });
  }

  function enhanceCodeBlocks() {
    document.querySelectorAll(".pre-wrap pre, .docs-content pre, .env-file pre").forEach(function (pre) {
      if (pre.parentElement && pre.parentElement.classList.contains("pre-wrap")) {
        ensureCopyButton(pre.parentElement, pre);
        return;
      }
      var wrap = document.createElement("div");
      wrap.className = "pre-wrap";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);
      ensureCopyButton(wrap, pre);
    });
  }

  function ensureCopyButton(wrap, pre) {
    if (wrap.querySelector(".copy-btn")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      var text = pre.innerText;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = "Copied";
          setTimeout(function () {
            btn.textContent = "Copy";
          }, 1200);
        });
      }
    });
    wrap.appendChild(btn);
  }

  function initMermaid() {
    if (!document.querySelector(".mermaid")) return;
    if (window.mermaid) {
      window.mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
      return;
    }
    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js";
    script.onload = function () {
      window.mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
      window.mermaid.run({ querySelector: ".mermaid" });
    };
    document.head.appendChild(script);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    markActiveNav();
    enhanceCodeBlocks();
    initMermaid();
  });
})();
