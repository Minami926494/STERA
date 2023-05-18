document.onreadystatechange = function () {
  if (document.readyState == 'interactive') {
    var pc = RegExp(/windows|x11|mac/i);
    var ibooks = RegExp(/ibooks|图书|圖書|図書/i);
    if (!navigator.userAgent.match(ibooks)) {
      window.onload = changeNote;
      window.onresize = changeNote;
    }
    function changeNote() {
      var n = document.querySelectorAll('note');
      for (let i = 0; i < n.length; i++) {
        let sup = n[i].querySelectorAll('sup');
        let aside = n[i].querySelectorAll('aside');
        for (let j = 0; j < sup.length; j++) {
          let link = sup[j].querySelector('a');
          let pic = sup[j].querySelector('img');
          let href = link.href;
          let id = aside[j].id;
          if (href.match('#' + id)) {
            n[i].classList.add('change');
            link.removeAttribute('href');
            aside[j].querySelector('a').removeAttribute('href');
            if (navigator.userAgent.match(pc)) {
              link.onmouseover = note;
              link.onmouseout = fade
            }
            else {
              link.ontouchstart = note;
              link.ontouchend = fade
            }
            function note() {
              aside[j].removeEventListener('webkitAnimationend', z);
              aside[j].removeEventListener('animationend', z);
              aside[j].removeAttribute('style');
              aside[j].removeAttribute('class');
              let dir = '';
              let w = function () {
                return document.body.clientWidth || document.documentElement.clientWidth;
              }();
              let h = window.innerHeight;
              let mw = pic.offsetWidth;
              let mh = pic.offsetHeight;
              let pw = n[i].offsetWidth;
              let ph = n[i].offsetHeight;
              let left = pic.offsetLeft;
              let top = pic.offsetTop;
              let right = pw - left;
              let bottom = ph - top;
              let ml = mw / 2 + left;
              let mt = pic.getBoundingClientRect().top;
              if (w >= pw * 2) {
                w /= 2;
                if (ml > w) {
                  ml -= w
                }
              }
              let vw = ml * 100 / w;
              if (vw > 80) {
                aside[j].style.left = 'unset';
                aside[j].style.right = right - mw / 2 + 1 + 'px';
                dir += 'zuo-out'
              }
              else if (vw > 50) {
                aside[j].style.left = 'unset';
                aside[j].style.right = right - mw / 2 - 51 + 'px';
                dir += 'zuo'
              }
              else if (vw > 20) {
                aside[j].style.left = left + mw / 2 - 51 + 'px';
                dir += 'you'
              }
              else {
                aside[j].style.left = left + mw / 2 + 1 + 'px';
                dir += 'you-out'
              }
              let nh = aside[j].offsetHeight;
              if (mt <= nh + 10 && mt < h / 2) {
                aside[j].style.top = top + mh + 10 + 'px';
                dir += '-xia'
              }
              else {
                aside[j].style.top = 'unset';
                aside[j].style.bottom = bottom + 10 + 'px';
                dir += '-shang'
              }
              aside[j].classList.add(dir);
              aside[j].style.zIndex = '1';
              aside[j].style.webkitAnimation = 'show 0.3s 1 forwards';
              aside[j].style.animation = 'show 0.3s 1 forwards'
            }
            function fade() {
              aside[j].style.webkitAnimation = 'fade 0.3s 1 forwards';
              aside[j].style.animation = 'fade 0.3s 1 forwards';
              aside[j].addEventListener('webkitAnimationend', z);
              aside[j].addEventListener('animationend', z)
            }
            function z() {
              aside[j].style.zIndex = '-1'
            }
          }
        }
      }
    }
    if (navigator.userAgent.match(pc)) {
      var body = document.body;
      if (body.bgColor) {
        body.onload = function () {
          body.parentNode.style.backgroundColor = body.bgColor
        }
      }
    }
    else {
      if (document.images.length == 1) {
        var img = document.querySelector('img');
        img.onload = rotate;
        window.onresize = rotate;
        function rotate() {
          if (img.parentNode.classList.contains('kuchie')) {
            let w = window.innerWidth;
            let h = window.innerHeight;
            let iw = img.width;
            let ih = img.height;
            if (iw > ih && ih / iw > w / h) {
              if (!img.classList.contains('change')) {
                img.classList.add('change')
              }
            }
            else if (img.classList.contains('change')) {
              img.classList.remove('change')
            }
          }
        }
      }
    }
  }
}