/*虚空文学旅团STERAePub++*/
const full = RegExp(/[一-龥　]/g);
const sys = navigator.platform || navigator.userAgent;
const brand = navigator.vendor || navigator.userAgent;
const isPC = sys.match(/win|x11|linux|mac/i) ? true : false;
const isApple = brand.match(/apple/i) ? true : false;
function changeNote() {
  const n = document.querySelectorAll('note');
  for (let i = 0; i < n.length; i++) {
    const sup = n[i].querySelectorAll('sup');
    const aside = n[i].querySelectorAll('aside');
    for (let j = 0; j < sup.length; j++) {
      const nbody = aside[j];
      const ref = nbody.querySelector('a');
      const style = nbody.style;
      const id = nbody.id;
      const noteInner = nbody.querySelector('p');
      const text = noteInner.innerText;
      const index = text.indexOf('：');
      if (index !== -1 && index < 6) {
        const fullchar = text.slice(0, index).match(full);
        const len = fullchar ? (index + fullchar.length) / 2 + 1 : index / 2 + 1;
        noteInner.style.marginLeft = len + 'em';
        noteInner.style.textIndent = -len + 'em';
      }
      if (isApple) {
        ref.style.color = '#000';
        nbody.querySelector('ol').style.listStyle = 'none';
        continue;
      }
      const link = sup[j].querySelector('a');
      const pic = sup[j].querySelector('img');
      const href = link.href;
      if (href.match('#' + id)) {
        style.display = 'none';
        n[i].classList.add('change');
        link.removeAttribute('href');
        nbody.removeAttribute('href');
        if (isPC) {
          link.onmouseover = note;
          link.onmouseout = fade;
        }
        else {
          link.ontouchstart = note;
          document.ontouchend = fade;
        }
        function note() {
          nbody.removeEventListener('webkitAnimationend', z);
          nbody.removeEventListener('animationend', z);
          nbody.removeAttribute('style');
          nbody.removeAttribute('class');
          const mw = pic.offsetWidth;
          const mh = pic.offsetHeight;
          const pw = n[i].offsetWidth;
          const ph = n[i].offsetHeight;
          const left = pic.offsetLeft;
          const top = pic.offsetTop;
          const right = pw - left;
          const bottom = ph - top;
          const mt = pic.getBoundingClientRect().top;
          let dir = '';
          let w = document.body.clientWidth || document.documentElement.clientWidth;
          let ml = mw / 2 + left;
          if (w >= pw * 2) {
            w /= 2;
            if (ml > w) ml -= w;
          }
          const vw = ml * 100 / w;
          if (vw > 80) {
            style.left = 'unset';
            style.right = right - mw / 2 + 1 + 'px';
            dir += 'zuo-out';
          }
          else if (vw > 50) {
            style.left = 'unset';
            style.right = right - mw / 2 - 51 + 'px';
            dir += 'zuo';
          }
          else if (vw > 20) {
            style.left = left + mw / 2 - 51 + 'px';
            dir += 'you';
          }
          else {
            style.left = left + mw / 2 + 1 + 'px';
            dir += 'you-out';
          }
          if (mt <= nbody.offsetHeight + 10 && mt < window.innerHeight / 2) {
            style.top = top + mh + 10 + 'px';
            dir += '-xia';
          }
          else {
            style.top = 'unset';
            style.bottom = bottom + 10 + 'px';
            dir += '-shang';
          }
          nbody.classList.add(dir);
          style.zIndex = '1';
          style.webkitAnimation = 'show 0.3s 1 forwards';
          style.animation = 'show 0.3s 1 forwards';
        }
        function fade() {
          style.webkitAnimation = 'fade 0.3s 1 forwards';
          style.animation = 'fade 0.3s 1 forwards';
          nbody.addEventListener('webkitAnimationend', z);
          nbody.addEventListener('animationend', z);
        }
        function z() {
          style.zIndex = '-1';
        }
      }
    }
  }
}
document.onreadystatechange = function () {
  if (document.readyState == 'interactive') {
    window.onload = changeNote;
    window.onresize = changeNote;
    if (isPC) {
      const body = document.body;
      const html = body.parentNode;
      const bgcolor = window.getComputedStyle(body).backgroundColor;
      if (bgcolor && bgcolor !== window.getComputedStyle(html).backgroundColor) body.onload = function () {
        html.style.backgroundColor = bgcolor;
      }
    }
    else if (document.images.length === 1) {
      const img = document.querySelector('img');
      img.onload = rotate;
      window.onresize = rotate;
      function rotate() {
        if (img.parentNode.classList.contains('kuchie')) {
          const iw = img.width;
          const ih = img.height;
          if (iw > ih && ih / iw > window.innerWidth / window.innerHeight) {
            if (!img.classList.contains('change')) img.classList.add('change');
          }
          else if (img.classList.contains('change')) img.classList.remove('change');
        }
      }
    }
  }
}