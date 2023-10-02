/*虚空文学旅团STERAePub++*/
var w=RegExp(/windows|x11|mac/i),x=RegExp(/apple books|ibooks|\u56fe\u4e66|\u5716\u66f8|\u56f3\u66f8/i),B=RegExp(/[\u4e00-\u9fa5\u3000]/g);function C(){for(var e=document.querySelectorAll("note"),d={i:0};d.i<e.length;d={h:d.h,i:d.i},d.i++){var l=e[d.i].querySelectorAll("sup");d.h=e[d.i].querySelectorAll("aside");for(var c={g:0};c.g<l.length;c={g:c.g,l:c.l,j:c.j},c.g++){var f=l[c.g].querySelector("a");c.j=l[c.g].querySelector("img");var h=f.href,q=d.h[c.g].id,u=d.h[c.g].querySelector("p"),r=u.innerText,g=r.indexOf("\uff1a");-1!==g&&6>g&&(g=(r=r.slice(0,g).match(B))?(g+r.length)/2+1:g/2+1,u.style.marginLeft=g+"em",u.style.textIndent=-g+"em");h.match("#"+q)&&(c.l=function(b,a){return function(){b.h[a.g].style.zIndex="-1"}}(d,c),h=function(b,a){return function(){b.h[a.g].style.webkitAnimation="fade 0.3s 1 forwards";b.h[a.g].style.animation="fade 0.3s 1 forwards";b.h[a.g].addEventListener("webkitAnimationend",a.l);b.h[a.g].addEventListener("animationend",a.l)}}(d,c),q=function(b,a){return function(){b.h[a.g].removeEventListener("webkitAnimationend",a.l);b.h[a.g].removeEventListener("animationend",a.l);b.h[a.g].removeAttribute("style");b.h[a.g].removeAttribute("class");var n=a.j.offsetWidth,D=a.j.offsetHeight,m=e[b.i].offsetWidth,t=a.j.offsetLeft,y=a.j.offsetTop,z=m-t,E=e[b.i].offsetHeight-y,A=a.j.getBoundingClientRect().top,k="",p=document.body.clientWidth||document.documentElement.clientWidth,v=n/2+t;p>=2*m&&(p/=2,v>p&&(v-=p));m=100*v/p;80<m?(b.h[a.g].style.left="unset",b.h[a.g].style.right=z-n/2+1+"px",k+="zuo-out"):50<m?(b.h[a.g].style.left="unset",b.h[a.g].style.right=z-n/2-51+"px",k+="zuo"):20<m?(b.h[a.g].style.left=t+n/2-51+"px",k+="you"):(b.h[a.g].style.left=t+n/2+1+"px",k+="you-out");A<=b.h[a.g].offsetHeight+10&&A<window.innerHeight/2?(b.h[a.g].style.top=y+D+10+"px",k+="-xia"):(b.h[a.g].style.top="unset",b.h[a.g].style.bottom=E+10+"px",k+="-shang");b.h[a.g].classList.add(k);b.h[a.g].style.zIndex="1";b.h[a.g].style.webkitAnimation="show 0.3s 1 forwards";b.h[a.g].style.animation="show 0.3s 1 forwards"}}(d,c),e[d.i].classList.add("change"),f.removeAttribute("href"),d.h[c.g].querySelector("a").removeAttribute("href"),navigator.userAgent.match(w)?(f.onmouseover=q,f.onmouseout=h):(f.ontouchstart=q,f.ontouchend=h))}}}document.onreadystatechange=function(){if("interactive"==document.readyState)if(navigator.userAgent.match(x)||(window.onload=C,window.onresize=C),navigator.userAgent.match(w)){var e=document.body,d=e.parentNode,l=window.getComputedStyle(e).backgroundColor;l!==window.getComputedStyle(d).backgroundColor&&(e.onload=function(){d.style.backgroundColor=l})}else if(1===document.images.length){e=function(){if(c.parentNode.classList.contains("kuchie")){var f=c.width,h=c.height;f>h&&h/f>window.innerWidth/window.innerHeight?c.classList.contains("change")||c.classList.add("change"):c.classList.contains("change")&&c.classList.remove("change")}};var c=document.querySelector("img");c.onload=e;window.onresize=e}};
/*使用Closure Compiler压缩，源码如下：
const pc = RegExp(/windows|x11|mac/i);
const apple = RegExp(/apple books|ibooks|图书|圖書|図書/i);
const full = RegExp(/[一-龥　]/g);
function changeNote() {
  const n = document.querySelectorAll('note');
  for (let i = 0; i < n.length; i++) {
    const sup = n[i].querySelectorAll('sup');
    const aside = n[i].querySelectorAll('aside');
    for (let j = 0; j < sup.length; j++) {
      const link = sup[j].querySelector('a');
      const pic = sup[j].querySelector('img');
      const href = link.href;
      const id = aside[j].id;
      const noteInner = aside[j].querySelector('p');
      const text = noteInner.innerText;
      const index = text.indexOf('：');
      if (index !== -1 && index < 6) {
        const fullchar = text.slice(0, index).match(full);
        const len = fullchar ? (index + fullchar.length) / 2 + 1 : index / 2 + 1;
        noteInner.style.marginLeft = len + 'em';
        noteInner.style.textIndent = -len + 'em';
      }
      if (href.match('#' + id)) {
        n[i].classList.add('change');
        link.removeAttribute('href');
        aside[j].querySelector('a').removeAttribute('href');
        if (navigator.userAgent.match(pc)) {
          link.onmouseover = note;
          link.onmouseout = fade;
        }
        else {
          link.ontouchstart = note;
          link.ontouchend = fade;
        }
        function note() {
          aside[j].removeEventListener('webkitAnimationend', z);
          aside[j].removeEventListener('animationend', z);
          aside[j].removeAttribute('style');
          aside[j].removeAttribute('class');
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
            if (ml > w) {
              ml -= w;
            }
          }
          const vw = ml * 100 / w;
          if (vw > 80) {
            aside[j].style.left = 'unset';
            aside[j].style.right = right - mw / 2 + 1 + 'px';
            dir += 'zuo-out';
          }
          else if (vw > 50) {
            aside[j].style.left = 'unset';
            aside[j].style.right = right - mw / 2 - 51 + 'px';
            dir += 'zuo';
          }
          else if (vw > 20) {
            aside[j].style.left = left + mw / 2 - 51 + 'px';
            dir += 'you';
          }
          else {
            aside[j].style.left = left + mw / 2 + 1 + 'px';
            dir += 'you-out';
          }
          if (mt <= aside[j].offsetHeight + 10 && mt < window.innerHeight / 2) {
            aside[j].style.top = top + mh + 10 + 'px';
            dir += '-xia';
          }
          else {
            aside[j].style.top = 'unset';
            aside[j].style.bottom = bottom + 10 + 'px';
            dir += '-shang';
          }
          aside[j].classList.add(dir);
          aside[j].style.zIndex = '1';
          aside[j].style.webkitAnimation = 'show 0.3s 1 forwards';
          aside[j].style.animation = 'show 0.3s 1 forwards';
        }
        function fade() {
          aside[j].style.webkitAnimation = 'fade 0.3s 1 forwards';
          aside[j].style.animation = 'fade 0.3s 1 forwards';
          aside[j].addEventListener('webkitAnimationend', z);
          aside[j].addEventListener('animationend', z);
        }
        function z() {
          aside[j].style.zIndex = '-1';
        }
      }
    }
  }
}
document.onreadystatechange = function () {
  if (document.readyState == 'interactive') {
    if (!navigator.userAgent.match(apple)) {
      window.onload = changeNote;
      window.onresize = changeNote;
    }
    if (navigator.userAgent.match(pc)) {
      const body = document.body;
      const html = body.parentNode;
      const bgcolor = window.getComputedStyle(body).backgroundColor;
      if (bgcolor !== window.getComputedStyle(html).backgroundColor) {
        body.onload = function () {
          html.style.backgroundColor = bgcolor
        }
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
*/