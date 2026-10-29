(function () {
  "use strict";

  var shelfEl = document.getElementById("shelf");
  var countEl = document.getElementById("pack-count");
  var errEl = document.getElementById("shelf-error");
  var runtimeMeta = document.getElementById("runtime-meta");
  var waitlistLink = document.getElementById("waitlist-link");
  var waitlistEmail = document.getElementById("waitlist-email");

  function truncate(sha, n) {
    n = n || 12;
    if (!sha) return "";
    return sha.length > n * 2 ? sha.slice(0, n) + "…" + sha.slice(-n) : sha;
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") node.textContent = attrs[k];
        else if (k === "html") node.innerHTML = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function field(label, value, opts) {
    opts = opts || {};
    var wrap = el("div", { class: "field" + (opts.hash ? " hash-block" : "") });
    wrap.appendChild(el("label", { text: label }));
    var val = el("div", { class: "value", title: value || "" });
    val.textContent = opts.full ? value || "—" : truncate(value, opts.n) || "—";
    if (opts.full && value) val.textContent = value;
    wrap.appendChild(val);
    return wrap;
  }

  function renderCard(pack, runtime) {
    var card = el("article", { class: "card", role: "listitem", "data-pack-id": pack.id });
    var head = el("div", null, [
      el("span", { class: "badge", text: pack.verify_kind || "verify" }),
      el("h3", { text: pack.name || pack.id }),
    ]);
    card.appendChild(head);
    card.appendChild(el("p", { class: "summary", text: pack.summary || "" }));

    card.appendChild(field("Pinned ref", pack.pinned_ref, { full: true }));
    card.appendChild(field("Content SHA-256", pack.content_sha256, { full: true, hash: true }));

    var verify = el("div", { class: "field" });
    verify.appendChild(el("label", { text: "Verify" }));
    var vlink = el("a", {
      href: pack.verify_url || "#",
      rel: "noopener",
      text: pack.verify_url || "(missing)",
    });
    verify.appendChild(vlink);
    card.appendChild(verify);

    var license = el("div", { class: "field" });
    license.appendChild(el("label", { text: "License · repo" }));
    var repo = el("a", { href: pack.repo_url || "#", rel: "noopener noreferrer", target: "_blank" });
    repo.textContent = (pack.license || "unknown") + " · " + (pack.repo_url || "");
    license.appendChild(repo);
    card.appendChild(license);

    var hasHash = !!(pack.content_sha256 && String(pack.content_sha256).trim());
    var installWrap = el("div", { class: "install-wrap" });
    installWrap.appendChild(el("label", { text: "Install (" + (runtime || "cursor") + ")" }));
    var pre = el("pre");
    pre.textContent = pack.install_command || "";
    installWrap.appendChild(pre);

    if (hasHash) {
      var copyBtn = el("button", { class: "btn primary", type: "button", text: "Copy install command" });
      copyBtn.addEventListener("click", function () {
        if (navigator.clipboard && pack.install_command) {
          navigator.clipboard.writeText(pack.install_command).catch(function () {});
        }
      });
      installWrap.appendChild(copyBtn);
    } else {
      var disabled = el("button", {
        class: "btn",
        type: "button",
        text: "Install unavailable (missing hash)",
        disabled: "disabled",
        "aria-disabled": "true",
      });
      installWrap.appendChild(disabled);
    }
    card.appendChild(installWrap);
    return card;
  }

  function applyConfig(config) {
    if (!config) return;
    if (runtimeMeta) {
      runtimeMeta.innerHTML =
        "Install runtime: <code>" +
        (config.install_runtime || "cursor") +
        "</code> · Vertical: <code>" +
        (config.vertical || "design-anti-slop") +
        "</code>";
    }
    if (waitlistLink && config.waitlist_url) {
      waitlistLink.href = config.waitlist_url;
      waitlistLink.setAttribute("data-waitlist-url", config.waitlist_url);
    }
    if (waitlistEmail && config.waitlist_email) {
      waitlistEmail.href = "mailto:" + config.waitlist_email;
      waitlistEmail.textContent = config.waitlist_email;
    }
  }

  function renderShelf(shelf, config) {
    var packs = (shelf && shelf.packs) || [];
    var max = (config && config.max_packs) || 10;
    if (packs.length > max) {
      errEl.hidden = false;
      errEl.textContent = "Shelf exceeds max of " + max + " packs (" + packs.length + ").";
      countEl.textContent = "0 shown (oversize)";
      return;
    }
    shelfEl.innerHTML = "";
    packs.forEach(function (p) {
      shelfEl.appendChild(renderCard(p, config && config.install_runtime));
    });
    countEl.textContent = packs.length + " / " + max + " packs";
  }

  Promise.all([
    fetch("data/shelf.json").then(function (r) {
      if (!r.ok) throw new Error("shelf.json HTTP " + r.status);
      return r.json();
    }),
    fetch("data/config.json").then(function (r) {
      if (!r.ok) throw new Error("config.json HTTP " + r.status);
      return r.json();
    }),
  ])
    .then(function (pair) {
      applyConfig(pair[1]);
      renderShelf(pair[0], pair[1]);
    })
    .catch(function (err) {
      errEl.hidden = false;
      errEl.textContent = "Failed to load shelf: " + err.message;
      countEl.textContent = "error";
    });
})();
