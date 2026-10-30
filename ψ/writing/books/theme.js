// Dark / light toggle shared by every page. The head snippet (theme_head in the builders) sets data-theme
// before the CSS paints; this wires the button and keeps its label in step.
(function(){var r=document.documentElement,b=document.getElementById('themebtn');if(!b)return;
 function label(){var l=r.dataset.theme==='light';var th=(r.lang||'').indexOf('th')===0;
  b.textContent=l?(th?'☾ โหมดมืด':'☾ Dark'):(th?'☀ โหมดสว่าง':'☀ Light');b.setAttribute('aria-pressed',String(l))}
 b.onclick=function(){r.dataset.theme=r.dataset.theme==='light'?'dark':'light';try{localStorage.setItem('aiexpo-theme',r.dataset.theme)}catch(e){}label()};
 window.aiexpoThemeLabel=label;label();if(window.matchMedia)matchMedia('(prefers-color-scheme: light)').addEventListener('change',function(e){if(!localStorage.getItem('aiexpo-theme')){r.dataset.theme=e.matches?'light':'dark';label()}})})();
