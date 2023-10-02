/*虚空文学旅团STERAePub++*/
var w=RegExp(/[\u4e00-\u9fa5\u3000]/g),x=navigator.vendor||navigator.userAgent,C=(navigator.platform||navigator.userAgent).match(/win|x11|linux|mac/i)?!0:!1,D=x.match(/apple/i)?!0:!1;
function E(){for(var c=document.querySelectorAll("note"),d={i:0};d.i<c.length;d={i:d.i},d.i++)for(var h=c[d.i].querySelectorAll("sup"),e=c[d.i].querySelectorAll("aside"),b={},f=0;f<h.length;b={g:b.g,h:b.h,l:b.l,j:b.j},f++){b.h=e[f];var k=b.h.querySelector("a");b.g=b.h.style;var r=b.h.id,m=b.h.querySelector("p"),t=m.innerText,g=t.indexOf("\uff1a");-1!==g&&6>g&&(g=(t=t.slice(0,g).match(w))?(g+t.length)/2+1:g/2+1,m.style.marginLeft=g+"em",m.style.textIndent=-g+"em");D?(k.style.color="#000",b.h.querySelector("ol").style.listStyle=
"none"):(k=h[f].querySelector("a"),b.j=h[f].querySelector("img"),k.href.match("#"+r)&&(b.l=function(a){return function(){a.g.zIndex="-1"}}(b),r=function(a){return function(){a.g.webkitAnimation="fade 0.3s 1 forwards";a.g.animation="fade 0.3s 1 forwards";a.h.addEventListener("webkitAnimationend",a.l);a.h.addEventListener("animationend",a.l)}}(b),m=function(a,y){return function(){a.h.removeEventListener("webkitAnimationend",a.l);a.h.removeEventListener("animationend",a.l);a.h.removeAttribute("style");
a.h.removeAttribute("class");var p=a.j.offsetWidth,F=a.j.offsetHeight,n=c[y.i].offsetWidth,u=a.j.offsetLeft,z=a.j.offsetTop,A=n-u,G=c[y.i].offsetHeight-z,B=a.j.getBoundingClientRect().top,l="",q=document.body.clientWidth||document.documentElement.clientWidth,v=p/2+u;q>=2*n&&(q/=2,v>q&&(v-=q));n=100*v/q;80<n?(a.g.left="unset",a.g.right=A-p/2+1+"px",l+="zuo-out"):50<n?(a.g.left="unset",a.g.right=A-p/2-51+"px",l+="zuo"):20<n?(a.g.left=u+p/2-51+"px",l+="you"):(a.g.left=u+p/2+1+"px",l+="you-out");B<=a.h.offsetHeight+
10&&B<window.innerHeight/2?(a.g.top=z+F+10+"px",l+="-xia"):(a.g.top="unset",a.g.bottom=G+10+"px",l+="-shang");a.h.classList.add(l);a.g.zIndex="1";a.g.webkitAnimation="show 0.3s 1 forwards";a.g.animation="show 0.3s 1 forwards"}}(b,d),b.g.display="none",c[d.i].classList.add("change"),k.removeAttribute("href"),b.h.removeAttribute("href"),C?(k.onmouseover=m,k.onmouseout=r):(k.ontouchstart=m,document.ontouchend=r)))}}
document.onreadystatechange=function(){if("interactive"==document.readyState)if(window.onload=E,window.onresize=E,C){var c=document.body,d=c.parentNode,h=window.getComputedStyle(c).backgroundColor;h&&h!==window.getComputedStyle(d).backgroundColor&&(c.onload=function(){d.style.backgroundColor=h})}else if(1===document.images.length){c=function(){if(e.parentNode.classList.contains("kuchie")){var b=e.width,f=e.height;b>f&&f/b>window.innerWidth/window.innerHeight?e.classList.contains("change")||e.classList.add("change"):
e.classList.contains("change")&&e.classList.remove("change")}};var e=document.querySelector("img");e.onload=c;window.onresize=c}};
/*使用Closure Compiler压缩
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
*/