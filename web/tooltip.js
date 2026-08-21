/**
 * Hanzi Kanji Cross-Reference Tooltip Controller
 */
(function () {
  var config = Object.assign(
    {
      modifier_key: "Shift",
      theme: "auto",
      popup_delay_ms: 30,
      character_font_size: 24,
      reading_font_size: 13,
      bold_characters: false,
      japanese_font: "Yu Gothic, Meiryo, 'Hiragino Sans', sans-serif",
      chinese_font: "'Microsoft YaHei', 'PingFang SC', 'Source Han Sans CN', sans-serif",
      popup_min_width: 220,
      popup_max_width: 320,
      show_pinyin: true,
      show_readings: true,
    },
    window.HANZI_KANJI_INITIAL_CONFIG || {}
  );

  var container = null;
  var highlightOverlay = null;
  var hoverTimer = null;
  var currentRequestId = 0;
  var activeChar = null;
  var activeCharRect = null;
  var lastMousePos = { x: 0, y: 0 };

  // Only match Hanzi / Kanji ideographs (ignores kana, punctuation, spaces, latin)
  function isCJKIdeograph(char) {
    if (!char) return false;
    var code = char.codePointAt(0);
    return (
      (code >= 0x4e00 && code <= 0x9fff) ||
      (code >= 0x3400 && code <= 0x4dbf) ||
      (code >= 0x20000 && code <= 0x2a6df) ||
      (code >= 0x2a700 && code <= 0x2b73f) ||
      (code >= 0x2b740 && code <= 0x2b81f) ||
      (code >= 0x2b820 && code <= 0x2ceaf) ||
      (code >= 0xf900 && code <= 0xfaff)
    );
  }

  function checkModifier(e) {
    var mod = (config.modifier_key || "Shift").toLowerCase();
    if (mod === "none") return true;
    if (mod === "shift") return e.shiftKey;
    if (mod === "alt") return e.altKey;
    if (mod === "control" || mod === "ctrl") return e.ctrlKey;
    return e.shiftKey;
  }

  function applyConfigStyles() {
    var c = createContainer();
    if (!c) return;

    var charSize = (config.character_font_size || 24) + "px";
    var readingSize = (config.reading_font_size || 13) + "px";
    var weight = config.bold_characters === true ? "700" : "400";

    c.style.setProperty("--hk-char-size", charSize);
    c.style.setProperty("--hk-reading-size", readingSize);
    c.style.setProperty("--hk-char-weight", weight);

    if (config.japanese_font) {
      c.style.setProperty("--hk-jp-font", config.japanese_font);
    }
    if (config.chinese_font) {
      c.style.setProperty("--hk-sc-font", config.chinese_font);
      c.style.setProperty("--hk-tc-font", config.chinese_font);
    }
    if (config.popup_min_width) {
      c.style.setProperty("--hk-min-width", config.popup_min_width + "px");
    }
    if (config.popup_max_width) {
      c.style.setProperty("--hk-max-width", config.popup_max_width + "px");
    }

    // Explicit Theme Switching (Light / Dark / Auto)
    c.classList.remove("hk-theme-light", "hk-theme-dark");
    var theme = (config.theme || "auto").toLowerCase();
    if (theme === "light") {
      c.classList.add("hk-theme-light");
    } else if (theme === "dark") {
      c.classList.add("hk-theme-dark");
    }
  }

  function getHighlightOverlay() {
    if (highlightOverlay && document.body.contains(highlightOverlay)) {
      return highlightOverlay;
    }
    highlightOverlay = document.getElementById("hk-highlight-overlay");
    if (!highlightOverlay) {
      highlightOverlay = document.createElement("div");
      highlightOverlay.id = "hk-highlight-overlay";
      document.body.appendChild(highlightOverlay);
    }
    return highlightOverlay;
  }

  function showHighlightOnCard(rect) {
    if (!rect || rect.width === 0 || rect.height === 0) {
      hideHighlightOnCard();
      return;
    }
    var overlay = getHighlightOverlay();
    overlay.style.left = rect.left + "px";
    overlay.style.top = rect.top + "px";
    overlay.style.width = rect.width + "px";
    overlay.style.height = rect.height + "px";
    overlay.style.display = "block";
  }

  function hideHighlightOnCard() {
    if (highlightOverlay) {
      highlightOverlay.style.display = "none";
    }
  }

  function getCharFromPoint(x, y) {
    var range, textNode, offset;

    if (document.caretRangeFromPoint) {
      range = document.caretRangeFromPoint(x, y);
      if (range) {
        textNode = range.startContainer;
        offset = range.startOffset;
      }
    } else if (document.caretPositionFromPoint) {
      var pos = document.caretPositionFromPoint(x, y);
      if (pos) {
        textNode = pos.offsetNode;
        offset = pos.offset;
      }
    }

    if (!textNode) return null;

    if (textNode.nodeType === Node.ELEMENT_NODE) {
      if (offset < textNode.childNodes.length) {
        textNode = textNode.childNodes[offset];
      } else if (textNode.childNodes.length > 0) {
        textNode = textNode.childNodes[textNode.childNodes.length - 1];
      }
    }

    while (textNode && textNode.nodeType === Node.ELEMENT_NODE && textNode.firstChild) {
      textNode = textNode.firstChild;
    }

    if (!textNode || textNode.nodeType !== Node.TEXT_NODE) {
      return null;
    }

    var text = textNode.textContent;
    if (!text || text.length === 0) return null;

    var candidates = [];
    if (offset < text.length) candidates.push(offset);
    if (offset > 0 && offset <= text.length) candidates.push(offset - 1);

    for (var i = 0; i < candidates.length; i++) {
      var off = candidates[i];
      var char = text.charAt(off);
      if (!isCJKIdeograph(char)) continue;

      try {
        var charRange = document.createRange();
        charRange.setStart(textNode, off);
        charRange.setEnd(textNode, off + 1);
        var rect = charRange.getBoundingClientRect();

        if (rect && rect.width > 0 && rect.height > 0) {
          if (
            x >= rect.left - 2 &&
            x <= rect.right + 2 &&
            y >= rect.top - 2 &&
            y <= rect.bottom + 2
          ) {
            return { char: char, rect: rect };
          }
        }
      } catch (e) {
        // Fallback
      }
    }

    return null;
  }

  function createContainer() {
    if (container && document.body.contains(container)) return container;
    container = document.getElementById("hk-tooltip-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "hk-tooltip-container";
      document.body.appendChild(container);
    }
    return container;
  }

  function hideTooltip() {
    if (hoverTimer) {
      clearTimeout(hoverTimer);
      hoverTimer = null;
    }
    if (container) {
      container.classList.remove("hk-visible");
    }
    hideHighlightOnCard();
    activeChar = null;
    activeCharRect = null;
  }

  function positionTooltip(x, y, charRect) {
    if (!container) return;

    var margin = 8;
    var docW = window.innerWidth;
    var docH = window.innerHeight;
    var rect = container.getBoundingClientRect();
    var tooltipW = rect.width || 220;
    var tooltipH = rect.height || 120;

    var left = charRect ? charRect.left : x + margin;
    var top = charRect ? charRect.bottom + margin : y + margin;

    if (left + tooltipW > docW - 10) {
      left = docW - tooltipW - 10;
    }
    if (left < 10) {
      left = 10;
    }

    if (top + tooltipH > docH - 10) {
      top = (charRect ? charRect.top : y) - tooltipH - margin;
    }
    if (top < 10) {
      top = 10;
    }

    container.style.left = left + "px";
    container.style.top = top + "px";
  }

  function renderTooltip(data, charRect) {
    createContainer();
    applyConfigStyles();

    var char = data.char || "";
    var isFound = Boolean(data.jp && data.jp.length > 0 && data.found !== false);

    var html = "";
    html += '<div class="hk-header">';
    html += '  <div class="hk-main-char">' + escapeHtml(char) + '</div>';
    html += '</div>';

    if (!isFound) {
      var msg = data.message || "No character cross-reference found";
      html += '<div class="hk-notice-message">' + escapeHtml(msg) + '</div>';
    } else {
      var jp = data.jp[0];
      var sc = (data.sc && data.sc.length) ? data.sc[0] : char;
      var tc = (data.tc && data.tc.length) ? data.tc[0] : char;

      var allDiff = Boolean(data.all_different);
      var hoveredVar = data.hovered_variant;

      var jpHlight = allDiff && hoveredVar === "jp" ? " hk-highlighted" : "";
      var scHlight = allDiff && hoveredVar === "sc" ? " hk-highlighted" : "";
      var tcHlight = allDiff && hoveredVar === "tc" ? " hk-highlighted" : "";

      html += '<div class="hk-variants-list">';
      html += '  <div class="hk-variant-row hk-variant-jp' + jpHlight + '">';
      html += '    <span class="hk-label">🇯🇵 JP</span>';
      html += '    <span class="hk-char-val">' + escapeHtml(jp) + '</span>';
      html += '  </div>';
      html += '  <div class="hk-variant-row hk-variant-sc' + scHlight + '">';
      html += '    <span class="hk-label">🇨🇳 SC</span>';
      html += '    <span class="hk-char-val">' + escapeHtml(sc) + '</span>';
      html += '  </div>';
      html += '  <div class="hk-variant-row hk-variant-tc' + tcHlight + '">';
      html += '    <span class="hk-label">🇹🇼 TC</span>';
      html += '    <span class="hk-char-val">' + escapeHtml(tc) + '</span>';
      html += '  </div>';
      html += '</div>';

      var hasPinyin = config.show_pinyin && data.pinyin && data.pinyin.length > 0;
      var onyomi = config.show_readings && data.onyomi && data.onyomi.length > 0 ? data.onyomi : null;
      var kunyomi = config.show_readings && data.kunyomi && data.kunyomi.length > 0 ? data.kunyomi : null;

      if (hasPinyin || onyomi || kunyomi) {
        html += '<div class="hk-readings">';
        if (hasPinyin) {
          html += '<div class="hk-reading-row">';
          html += '  <span class="hk-reading-label">Pinyin</span>';
          html += '  <span class="hk-reading-val">' + escapeHtml(data.pinyin.join(", ")) + '</span>';
          html += '</div>';
        }
        if (onyomi || kunyomi) {
          var readingsParts = [];
          if (onyomi) readingsParts.push("On: " + onyomi.join(", "));
          if (kunyomi) readingsParts.push("Kun: " + kunyomi.join(", "));
          html += '<div class="hk-reading-row">';
          html += '  <span class="hk-reading-label">Kana</span>';
          html += '  <span class="hk-reading-val">' + escapeHtml(readingsParts.join(" | ")) + '</span>';
          html += '</div>';
        }
        html += '</div>';
      }
    }

    container.innerHTML = html;
    positionTooltip(lastMousePos.x, lastMousePos.y, charRect);
    container.classList.add("hk-visible");
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function onMouseMove(e) {
    lastMousePos = { x: e.clientX, y: e.clientY };

    if (!checkModifier(e)) {
      hideTooltip();
      return;
    }

    var hit = getCharFromPoint(e.clientX, e.clientY);
    if (!hit) {
      hideTooltip();
      return;
    }

    showHighlightOnCard(hit.rect);
    activeCharRect = hit.rect;

    var char = hit.char;
    if (char === activeChar) {
      return;
    }

    activeChar = char;

    if (hoverTimer) {
      clearTimeout(hoverTimer);
    }

    hoverTimer = setTimeout(function () {
      currentRequestId++;
      var reqId = String(currentRequestId);
      var payload = JSON.stringify({ char: char, req_id: reqId });

      if (typeof pycmd !== "undefined") {
        pycmd("hanzikanji:lookup:" + payload, function (res) {
          if (res && window.HanziKanjiBridge) {
            window.HanziKanjiBridge.onResult(res, reqId, activeCharRect);
          }
        });
      }
    }, config.popup_delay_ms || 30);
  }

  function onKeyUp(e) {
    if (!checkModifier(e)) {
      hideTooltip();
    }
  }

  document.removeEventListener("mousemove", onMouseMove);
  document.removeEventListener("keyup", onKeyUp);
  document.addEventListener("mousemove", onMouseMove, { passive: true });
  document.addEventListener("keyup", onKeyUp, { passive: true });
  document.addEventListener("mouseleave", hideTooltip, { passive: true });
  window.addEventListener("scroll", hideTooltip, { passive: true });

  window.HanziKanjiBridge = {
    onResult: function (data, reqId, charRect) {
      if (!data) {
        hideTooltip();
        return;
      }
      if (reqId && String(reqId) !== String(currentRequestId)) {
        return;
      }
      renderTooltip(data, charRect || activeCharRect);
    },
    onConfig: function (newConfig) {
      if (newConfig) {
        config = Object.assign(config, newConfig);
        applyConfigStyles();
      }
    },
  };

  applyConfigStyles();
})();
