// Percussion World — navigation toggle and image lightbox
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

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
