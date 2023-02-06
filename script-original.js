document.onreadystatechange = function() {
  if(document.readyState == 'interactive') {
    var pc = RegExp(/windows|x11|mac/i);
    var ibooks = RegExp(/ibooks|图书|圖書|図書/i);
    var noteLogo = document.querySelectorAll('sup');
    var noteText = document.querySelectorAll('aside');
    if(navigator.userAgent.match(ibooks) == null) {
      noteLogo.onload = changeNote(noteLogo,noteText);
      window.onresize = changeNote(noteLogo,noteText);
    }
    function changeNote(a,b) {
      for(let i = 0;i < b.length;i++) {
        var notePanel = b[i].parentNode;
        var link = a[i].querySelector('a');
        var href = link.href;
        var id = b[i].id;
        if(href.match('#' + id)) {
          var text = a[i].parentNode;
          notePanel.classList.add('change');
          link.removeAttribute('href');
          b[i].querySelector('a').removeAttribute('href');
          if(navigator.userAgent.match(pc)) {
            link.onmouseover = note;
            link.onmouseout = fade
          }
          else {
            link.ontouchstart = note;
            link.ontouchend = fade
          }
          function note() {
            b[i].removeEventListener('webkitAnimationend',z);
            b[i].removeEventListener('animationend',z);
            b[i].removeAttribute('style');
            b[i].removeAttribute('class');
            let dir = '';
            let w = function() {
              return document.body.clientWidth || document.documentElement.clientWidth;
            }();
            let h = window.innerHeight;
            let mw = a[i].offsetWidth;
            let mh = a[i].offsetHeight;
            let pw = notePanel.offsetWidth;
            let ph = notePanel.offsetHeight;
            let left = a[i].offsetLeft;
            let top = a[i].offsetTop;
            let right = pw - left;
            let bottom = ph - top;
            let ml = mw / 2 + left;
            let mt = a[i].getBoundingClientRect().top;
            if(w >= pw * 2) {
              w /= 2;
              if(ml > w) {
                ml -= w
              }
            }
            let vw = ml * 100 / w;
            if(vw > 80) {
              b[i].style.left = 'auto';
              b[i].style.right = right - mw / 2 + 1 + 'px';
              dir += 'zuo-out'
            }
            else if(vw > 50) {
              b[i].style.left = 'auto';
              b[i].style.right = right - mw / 2 - 51 + 'px';
              dir += 'zuo'
            }
            else if(vw > 20) {
              b[i].style.left = left + mw / 2 - 51 + 'px';
              dir += 'you'
            }
            else {
              b[i].style.left = left + mw / 2 + 1 + 'px';
              dir += 'you-out'
            }
            let nh = b[i].offsetHeight;
            if(mt <= nh + 10 && mt < h / 2) {
              b[i].style.top = top + mh + 10 + 'px';
              dir += '-xia'
            }
            else {
              b[i].style.top = 'auto';
              b[i].style.bottom = bottom + 10 + 'px';
              dir += '-shang'
            }
            b[i].classList.add(dir);
            b[i].style.zIndex = '1';
            b[i].style.webkitAnimation = 'show 0.3s 1 forwards';
            b[i].style.animation = 'show 0.3s 1 forwards'
          }
          function fade() {
            b[i].style.webkitAnimation = 'fade 0.3s 1 forwards';
            b[i].style.animation = 'fade 0.3s 1 forwards';
            b[i].addEventListener('webkitAnimationend',z);
            b[i].addEventListener('animationend',z)
          }
          function z() {
            b[i].style.zIndex = '-1'
          }
        }
      }
    }
    if(navigator.userAgent.match(pc)) {
      var body = document.body;
	  if(body.bgColor) {
	    body.onload = bgcolor;
	    function bgcolor(){
		  body.parentNode.style.backgroundColor = body.bgColor
	    }
	  }
	}
	else {
      if(document.images.length == 1) {
        var img = document.querySelector('img');
        img.onload = rotate;
        window.onresize = rotate;
        function rotate() {
          if(img.parentNode.classList.contains('kuchie')) {
            let w = window.innerWidth;
            let h = window.innerHeight;
            let iw = img.width;
            let ih = img.height;
            if(iw > ih && ih/iw > w/h) {
              if(img.classList.contains('change') == false) {
                img.classList.add('change')
              }
            }
            else if(img.classList.contains('change')) {
              img.classList.remove('change')
            }
          }
        }
      }
    }
  }
}