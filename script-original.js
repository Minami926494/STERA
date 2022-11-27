<!--
document.onreadystatechange = function() {
  if(document.readyState == 'interactive') {
    var pc = RegExp(/windows|x11|mac/i);
    var noteLogo = document.querySelectorAll('sup');
    var noteText = document.querySelectorAll('aside');
    noteLogo.onload = changeNote(noteLogo,noteText);
    window.onresize = changeNote(noteLogo,noteText);
    function changeNote(a,b) {
      for(let i = 0;i < b.length;i++) {
        var notePanel = b[i].parentNode;
        var link = a[i].querySelector('a');
        var href = link.href;
        var id = b[i].id;
        if(href.match('#' + id)) {
          var text = a[i].parentNode;
          notePanel.classList.add('change');
          link.href = 'javascript:void(0)';
          b[i].querySelector('a').href = 'javascript:void(0)';
          if(navigator.userAgent.match(pc)) {
            link.onmouseover = note;
            link.onmouseout = function() {
              b[i].removeAttribute('style')
            }
          }
          else {
            link.onfocus = note;
            link.onblur = function() {
              b[i].removeAttribute('style')
            }
          }
          function note() {
            let w = window.innerWidth;
            let x = a[i].offsetLeft;
            let y = a[i].offsetTop;
            let mw = a[i].offsetWidth;
            let mh = a[i].offsetHeight;
            let nw = b[i].offsetWidth;
            let nh = b[i].offsetHeight;
            let pw = notePanel.offsetWidth;
            let ml = mw / 2 + x;
            let mt = event.clientY;
            if(w >= pw * 2) {
              w /= 2;
              if(ml > w) {
                ml -= w
              }
            }
            let vw = ml * 100 / w;
            if(vw > 50) {
              x -= nw
            }
            else {
              x += mw
            }
            if(mt >= nh + mh) {
              y -= nh
            }
            else {
              y += mh
            }
            b[i].style.left = x + 'px';
            b[i].style.top = y + 'px';
            b[i].style.visibility = 'visible'
          }
        }
      }
    }
    if(navigator.userAgent.match(pc) == false) {
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
//-->