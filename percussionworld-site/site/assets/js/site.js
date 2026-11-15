// Percussion World — menu, taalkeuze en lightbox voor afbeeldingen
(function () {
  // Uitschuifbaar zijmenu (smalle schermen)
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var backdrop = document.createElement('div');
    backdrop.className = 'nav-backdrop';
    document.body.appendChild(backdrop);
    var setNav = function (open) {
      nav.classList.toggle('open', open);
      backdrop.classList.toggle('show', open);
      toggle.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', function () { setNav(!nav.classList.contains('open')); });
    backdrop.addEventListener('click', function () { setNav(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
  }

  // Taalkeuze: uitschuifmenu in de kop
  var lang = document.querySelector('.lang');
  if (lang) {
    var langBtn = lang.querySelector('.lang-toggle');
    var setLang = function (open) {
      lang.classList.toggle('open', open);
      langBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    langBtn.addEventListener('click', function (e) { e.stopPropagation(); setLang(!lang.classList.contains('open')); });
    document.addEventListener('click', function (e) { if (!lang.contains(e.target)) setLang(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setLang(false); });
  }
  // Onthoud de gekozen taal en houd de plek op de pagina (#anker) vast bij wisselen
  Array.prototype.forEach.call(document.querySelectorAll('a[hreflang]'), function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('pw-lang', a.getAttribute('hreflang')); } catch (err) {}
      if (location.hash) a.href = a.href.split('#')[0] + location.hash;
    });
  });

  var box = document.querySelector('.lightbox');
  if (!box) return;
  var img = box.querySelector('img');
  var cap = box.querySelector('figcaption');
  var prev = box.querySelector('.lightbox-prev');
  var next = box.querySelector('.lightbox-next');
  var group = [];
  var index = 0;
  var lastFocus = null;

  function captionOf(a) {
    if (a.dataset.caption) return a.dataset.caption;
    var fig = a.closest('figure');
    var fc = fig && fig.querySelector('figcaption');
    if (fc) return fc.textContent.trim();
    var span = a.querySelector('span');
    if (span) return span.textContent.trim();
    var im = a.querySelector('img');
    return im ? im.alt : '';
  }

  function show(i) {
    index = (i + group.length) % group.length;
    var a = group[index];
    img.src = a.getAttribute('href');
    img.alt = captionOf(a);
    cap.textContent = captionOf(a);
    var multi = group.length > 1;
    prev.hidden = !multi;
    next.hidden = !multi;
  }

  function open(a) {
    var key = a.dataset.group || (a.closest('[data-gallery]') && a.closest('[data-gallery]').dataset.gallery) || null;
    group = key
      ? Array.prototype.filter.call(document.querySelectorAll('a.lb'), function (el) {
          var k = el.dataset.group || (el.closest('[data-gallery]') && el.closest('[data-gallery]').dataset.gallery);
          return k === key;
        })
      : [a];
    lastFocus = a;
    show(group.indexOf(a));
    box.hidden = false;
    document.body.style.overflow = 'hidden';
    box.querySelector('.lightbox-close').focus();
  }

  function close() {
    box.hidden = true;
    img.removeAttribute('src');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a.lb');
    if (!a) return;
    e.preventDefault();
    open(a);
  });
  box.querySelector('.lightbox-close').addEventListener('click', close);
  prev.addEventListener('click', function () { show(index - 1); });
  next.addEventListener('click', function () { show(index + 1); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft' && group.length > 1) show(index - 1);
    if (e.key === 'ArrowRight' && group.length > 1) show(index + 1);
  });
})();
