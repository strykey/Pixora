import webview
import base64
import io
import math
import os
from PIL import Image

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Pixora</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#e4f1fa;
  --surface:#eef7fd;
  --panel:#f8fcff;
  --border:#c5e2f5;
  --border-soft:#daeef9;
  --accent:#4fa8d8;
  --accent-h:#3d96c6;
  --accent-dim:#8ec9e8;
  --accent-soft:#dceef9;
  --text:#244f66;
  --muted:#6a9eb8;
  --muted-s:#9dbfd3;
  --font-px:'Press Start 2P',monospace;
  --font-ui:'DM Sans',sans-serif;
  --r:10px;
  --sh:0 2px 12px rgba(79,168,216,.1);
  --sh-md:0 8px 32px rgba(79,168,216,.14);
}
html,body{height:100%;overflow:hidden;background:var(--bg);-webkit-font-smoothing:antialiased}
body{font-family:var(--font-ui);color:var(--text);display:flex;flex-direction:column;user-select:none}

/* SPLASH */
#splash{
  position:fixed;inset:0;z-index:999;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;
  background:linear-gradient(155deg,#cde8f7 0%,#e4f1fa 55%,#eef7fd 100%);
}
#splash.out{animation:splashOut .55s cubic-bezier(.4,0,.2,1) forwards}
.s-logo{
  font-family:var(--font-px);font-size:clamp(18px,3vw,30px);
  letter-spacing:8px;color:var(--accent);text-shadow:3px 3px 0 var(--accent-dim);
  animation:riseIn .65s cubic-bezier(.22,1,.36,1) both;
}
.s-sub{
  font-size:11px;color:var(--muted);letter-spacing:4px;text-transform:uppercase;
  margin-top:-16px;animation:riseIn .65s .12s cubic-bezier(.22,1,.36,1) both;
}
.s-ring{
  width:36px;height:36px;border-radius:50%;
  border:3px solid var(--border);border-top-color:var(--accent);
  animation:spin .9s linear infinite;
}

/* APP SHELL */
#app{display:none;flex-direction:column;height:100vh;opacity:0;transition:opacity .4s}

header{
  height:52px;padding:0 24px;
  display:flex;align-items:center;justify-content:space-between;
  background:var(--panel);border-bottom:1.5px solid var(--border);flex-shrink:0;
  animation:slideDown .5s .1s cubic-bezier(.22,1,.36,1) both;
}
.logo{font-family:var(--font-px);font-size:11px;color:var(--accent);letter-spacing:3px}
.logo em{font-style:normal;color:var(--muted-s);font-size:7px;margin-left:12px;letter-spacing:2px;font-family:var(--font-ui);font-weight:500}
.credit{font-size:11px;color:var(--muted-s);letter-spacing:.3px}

/* LAYOUT */
.workspace{
  display:flex;flex-direction:row;
  flex:1;overflow:hidden;
  animation:riseIn .5s .2s cubic-bezier(.22,1,.36,1) both;
}
.resizer{
  width:5px;flex-shrink:0;cursor:col-resize;
  background:var(--border);transition:background .15s;
  position:relative;z-index:10;
}
.resizer:hover,.resizer.dragging{background:var(--accent)}

/* SIDEBAR */
.sidebar{
  background:var(--panel);
  display:flex;flex-direction:column;overflow-y:auto;padding:20px 18px;gap:22px;
  width:290px;flex-shrink:0;
}
.sidebar::-webkit-scrollbar{width:3px}
.sidebar::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

.block{display:flex;flex-direction:column;gap:10px}
.blk-ttl{
  font-size:9px;letter-spacing:2px;text-transform:uppercase;
  color:var(--muted);font-weight:600;padding-bottom:8px;border-bottom:1px solid var(--border-soft);
}

/* Drop zone */
.dz{
  border:1.5px dashed var(--accent-dim);border-radius:var(--r);
  padding:28px 16px;text-align:center;cursor:pointer;
  background:var(--accent-soft);
  transition:border-color .2s,background .2s,transform .2s cubic-bezier(.34,1.56,.64,1);
  position:relative;overflow:hidden;
}
.dz:hover{border-color:var(--accent);background:#d4e9f7;transform:scale(1.01)}
.dz.over{border-color:var(--accent);background:#c8e3f4;transform:scale(1.02)}
.dz-ico{
  width:36px;height:36px;margin:0 auto 12px;
  border-radius:8px;background:var(--panel);border:1.5px solid var(--border);
  display:flex;align-items:center;justify-content:center;box-shadow:var(--sh);
  transition:transform .3s cubic-bezier(.34,1.56,.64,1);
}
.dz:hover .dz-ico{transform:translateY(-4px) scale(1.08)}
.dz-ico svg{width:16px;height:16px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.dz-h{font-size:13px;font-weight:600;color:var(--text);margin-bottom:3px}
.dz-p{font-size:11px;color:var(--muted);line-height:1.8}

/* Buttons */
.row2{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.btn{
  padding:9px 12px;border-radius:8px;
  border:1.5px solid var(--border);background:var(--surface);
  color:var(--text);font-family:var(--font-ui);font-size:12px;font-weight:500;
  cursor:pointer;
  transition:background .18s,border-color .18s,transform .18s cubic-bezier(.34,1.56,.64,1),box-shadow .18s;
  display:flex;align-items:center;justify-content:center;gap:6px;
}
.btn:hover{background:var(--accent-soft);border-color:var(--accent-dim);transform:translateY(-2px);box-shadow:var(--sh)}
.btn:active{transform:scale(.95);transition-duration:.08s}
.btn:disabled{opacity:.35;cursor:not-allowed;transform:none;box-shadow:none;pointer-events:none}

.btn.primary{
  grid-column:1/-1;padding:13px;
  background:var(--accent);border-color:var(--accent);color:#fff;
  font-family:var(--font-px);font-size:9px;letter-spacing:2px;
  box-shadow:0 4px 16px rgba(79,168,216,.22);
}
.btn.primary:hover{background:var(--accent-h);border-color:var(--accent-h);box-shadow:0 8px 24px rgba(79,168,216,.32);transform:translateY(-2px)}
.btn.primary:active{transform:scale(.97)}
.btn.primary:disabled{background:var(--accent-dim);border-color:var(--accent-dim);box-shadow:none}

.btn.export{grid-column:1/-1;padding:12px;font-family:var(--font-px);font-size:9px;letter-spacing:2px}
.btn.export:not(:disabled):hover{background:var(--accent-soft);border-color:var(--accent)}

/* Settings */
.setting{display:flex;flex-direction:column;gap:7px}
.s-row{display:flex;align-items:center;justify-content:space-between;font-size:12px;font-weight:500}
.chip{
  font-family:var(--font-px);font-size:7px;color:var(--accent);
  background:var(--accent-soft);padding:3px 8px;border-radius:6px;transition:background .2s,color .2s;
}
input[type=range]{
  -webkit-appearance:none;width:100%;height:4px;
  background:var(--border);border-radius:10px;outline:none;cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:16px;height:16px;border-radius:4px;
  background:var(--accent);border:2.5px solid var(--panel);
  box-shadow:0 2px 8px rgba(79,168,216,.28);cursor:pointer;
  transition:transform .2s cubic-bezier(.34,1.56,.64,1);
}
input[type=range]::-webkit-slider-thumb:hover{transform:scale(1.3)}

.tgl-row{display:flex;align-items:center;justify-content:space-between;font-size:12px;font-weight:500;min-height:28px}
.tgl{
  width:34px;height:18px;border-radius:9px;background:var(--border);
  border:none;cursor:pointer;position:relative;flex-shrink:0;
  transition:background .25s cubic-bezier(.4,0,.2,1);
}
.tgl.on{background:var(--accent)}
.tgl::after{
  content:'';position:absolute;top:3px;left:3px;width:12px;height:12px;
  border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.15);
  transition:left .25s cubic-bezier(.4,0,.2,1);
}
.tgl.on::after{left:19px}

/* Progress */
.prog-wrap{display:flex;flex-direction:column;gap:7px}
.prog{height:4px;background:var(--border);border-radius:10px;overflow:hidden;opacity:0;transition:opacity .3s}
.prog.on{opacity:1}
.prog-bar{
  height:100%;width:0%;border-radius:10px;
  background:linear-gradient(90deg,var(--accent-dim),var(--accent));
  transition:width .4s cubic-bezier(.4,0,.2,1);
  position:relative;overflow:hidden;
}
.prog-bar::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);
  animation:shimmer 1.2s linear infinite;
}
.prog-bar.indef{animation:indef 1.4s ease-in-out infinite}
.prog-txt{font-size:10px;color:var(--muted);text-align:center;min-height:14px;font-family:var(--font-px);letter-spacing:1px}

/* CANVAS AREA */
.cv-area{display:flex;flex-direction:column;flex:1;overflow:hidden;min-width:0}

.toolbar{
  height:46px;padding:0 18px;display:flex;align-items:center;gap:8px;
  background:var(--panel);border-bottom:1.5px solid var(--border);flex-shrink:0;
}
.tabs{display:flex;border:1.5px solid var(--border);border-radius:8px;overflow:hidden;background:var(--surface)}
.tab{
  padding:6px 16px;font-size:11px;font-weight:500;border:none;
  background:transparent;color:var(--muted);cursor:pointer;transition:background .18s,color .18s;
}
.tab.active{background:var(--accent-soft);color:var(--accent)}

.zoom-grp{display:flex;align-items:center;gap:5px;margin-left:auto}
.z-btn{
  width:26px;height:26px;border-radius:6px;border:1.5px solid var(--border);
  background:var(--surface);color:var(--text);font-size:14px;font-weight:600;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background .16s,transform .16s cubic-bezier(.34,1.56,.64,1),border-color .16s;
}
.z-btn:hover{background:var(--accent-soft);border-color:var(--accent-dim);transform:scale(1.12)}
.z-btn:active{transform:scale(.9)}
.z-val{font-family:var(--font-px);font-size:7px;color:var(--muted);min-width:38px;text-align:center}

/* Stage */
.stage{
  flex:1;display:flex;align-items:flex-start;justify-content:flex-start;
  overflow:auto;padding:32px;background:var(--bg);
  min-width:0;
}
.stage-inner{
  margin:auto;
  min-width:0;
}
.stage::-webkit-scrollbar{width:6px;height:6px}
.stage::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.stage::-webkit-scrollbar-corner{background:var(--bg)}

.empty{
  display:flex;flex-direction:column;align-items:center;gap:14px;
  text-align:center;pointer-events:none;
  animation:riseIn .5s .4s cubic-bezier(.22,1,.36,1) both;
}
.e-grid{display:grid;grid-template-columns:repeat(12,12px);gap:2px;opacity:.25;margin-bottom:4px}
.e-grid div{height:12px;border-radius:2px}
.e-h{font-family:var(--font-px);font-size:10px;color:var(--muted);letter-spacing:2px}
.e-p{font-size:12px;color:var(--muted);opacity:.65;line-height:1.7}

/* Canvas wrapper — no transform, real CSS dimensions for proper scroll */
.cv-wrap{
  display:none;
  position:relative;
  box-shadow:0 12px 48px rgba(79,168,216,.17),0 0 0 1.5px var(--border);
  border-radius:3px;overflow:hidden;
  flex-shrink:0;
}
.cv-wrap.show{display:inline-block}
.cv-wrap.pop{animation:cvPop .38s cubic-bezier(.22,1,.36,1)}
canvas{display:block;image-rendering:pixelated;image-rendering:crisp-edges;}

/* Info bar */
.infobar{
  height:36px;padding:0 18px;display:flex;align-items:center;gap:18px;
  background:var(--panel);border-top:1.5px solid var(--border);flex-shrink:0;
}
.ii{font-size:10px;color:var(--muted);display:flex;align-items:center;gap:5px}
.ii b{font-family:var(--font-px);font-size:7px;color:var(--text);transition:color .35s}
.ii b.flash{color:var(--accent)}

/* Toast */
.toast{
  position:fixed;bottom:22px;right:22px;z-index:800;
  padding:10px 16px;background:var(--panel);border:1.5px solid var(--border);border-radius:10px;
  font-family:var(--font-px);font-size:8px;letter-spacing:1px;color:var(--text);
  box-shadow:var(--sh-md);
  transform:translateY(14px) scale(.96);opacity:0;
  transition:transform .3s cubic-bezier(.22,1,.36,1),opacity .3s;pointer-events:none;
}
.toast.show{transform:translateY(0) scale(1);opacity:1}
.toast.ok{border-color:var(--accent);color:var(--accent)}
.toast.err{border-color:#d4879a;color:#a03050}

#fi{display:none}

@keyframes spin{to{transform:rotate(360deg)}}
@keyframes splashOut{0%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(1.04)}}
@keyframes riseIn{0%{opacity:0;transform:translateY(12px)}100%{opacity:1;transform:translateY(0)}}
@keyframes slideDown{0%{opacity:0;transform:translateY(-14px)}100%{opacity:1;transform:translateY(0)}}
@keyframes cvPop{0%{opacity:0;transform:scale(.96)}100%{opacity:1;transform:scale(1)}}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}
@keyframes indef{0%{transform:translateX(-150%) scaleX(.4)}50%{transform:translateX(50%) scaleX(.6)}100%{transform:translateX(200%) scaleX(.4)}}
</style>
</head>
<body>

<div id="splash">
  <div class="s-logo">PIXORA</div>
  <div class="s-sub">Pixel Art Converter</div>
  <div class="s-ring"></div>
</div>

<div id="app">
  <header>
    <div class="logo">PIXORA <em>Pixel Art Converter</em></div>
    <div class="credit">Made by Strykey</div>
  </header>

  <div class="workspace">
    <div class="sidebar">

      <div class="block">
        <div class="blk-ttl">Import</div>
        <div class="dz" id="dz" onclick="document.getElementById('fi').click()">
          <div class="dz-ico">
            <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          </div>
          <div class="dz-h">Drop image here</div>
          <div class="dz-p">or click to browse<br/>PNG · JPG · WEBP · BMP · GIF</div>
        </div>
        <input type="file" id="fi" accept="image/*"/>
        <div class="row2">
          <button class="btn" onclick="document.getElementById('fi').click()">Browse</button>
          <button class="btn" id="psteBtn">Paste</button>
        </div>
      </div>

      <div class="block">
        <div class="blk-ttl">Settings</div>
        <div class="setting">
          <div class="s-row">Pixel Size <span class="chip" id="pxV">Auto</span></div>
          <input type="range" id="pxS" min="0" max="32" value="0"
            oninput="pxO=+this.value;document.getElementById('pxV').textContent=this.value==0?'Auto':this.value+'px'"/>
        </div>
        <div class="setting">
          <div class="s-row">Color Depth <span class="chip" id="coV">64</span></div>
          <input type="range" id="coS" min="4" max="128" step="4" value="64"
            oninput="cD=+this.value;document.getElementById('coV').textContent=this.value"/>
        </div>
        <div class="setting">
          <div class="s-row">Dither <span class="chip" id="diV">60%</span></div>
          <input type="range" id="diS" min="0" max="100" value="60"
            oninput="dS=+this.value/100;document.getElementById('diV').textContent=this.value+'%'"/>
        </div>
        <div class="tgl-row">
          Edge Enhance
          <button class="tgl on" id="edgTgl" onclick="this.classList.toggle('on');eE=this.classList.contains('on')"></button>
        </div>
      </div>

      <div class="block">
        <div class="row2">
          <button class="btn primary" id="cvtBtn" disabled onclick="startConvert()">Convert</button>
          <button class="btn export" id="expBtn" disabled onclick="exportImg()">Export 4K</button>
        </div>
        <div class="prog-wrap">
          <div class="prog" id="prog"><div class="prog-bar" id="pb"></div></div>
          <div class="prog-txt" id="pt"></div>
        </div>
      </div>

    </div>
    <div class="resizer" id="resizer"></div>

    <div class="cv-area">
      <div class="toolbar">
        <div class="tabs">
          <button class="tab active" id="tR" onclick="setView('out',this)">Result</button>
          <button class="tab" id="tO" onclick="setView('src',this)">Original</button>
        </div>
        <div class="zoom-grp">
          <button class="z-btn" onclick="dZoom(-.2)">&#8722;</button>
          <span class="z-val" id="zV">100%</span>
          <button class="z-btn" onclick="dZoom(.2)">+</button>
          <button class="z-btn" onclick="fitZoom()">&#8857;</button>
        </div>
      </div>

      <div class="stage" id="stage">
        <div class="stage-inner" id="stageInner">
          <div class="empty" id="emp">
            <div class="e-grid" id="eg"></div>
            <div class="e-h">No image loaded</div>
            <div class="e-p">Drop an image or click Browse<br/>to get started</div>
          </div>
          <div class="cv-wrap" id="cvW">
            <canvas id="oC"></canvas>
            <canvas id="sC" style="display:none"></canvas>
          </div>
        </div>
      </div>

      <div class="infobar">
        <div class="ii">Source <b id="iS">&#8212;</b></div>
        <div class="ii">Output <b id="iO">&#8212;</b></div>
        <div class="ii">Block <b id="iB">&#8212;</b></div>
        <div class="ii">Colors <b id="iC">&#8212;</b></div>
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let pxO=0,cD=64,dS=0.6,eE=true,zL=1,view='out',r64=null,hasImg=false;

window.addEventListener('load',()=>{
  buildGrid();
  initDrop();
  initPaste();
  setTimeout(()=>{
    const sp=document.getElementById('splash');
    sp.classList.add('out');
    sp.addEventListener('animationend',()=>{
      sp.style.display='none';
      const app=document.getElementById('app');
      app.style.display='flex';
      requestAnimationFrame(()=>requestAnimationFrame(()=>{app.style.opacity='1'}));
    },{once:true});
  },1500);
});

function buildGrid(){
  const g=document.getElementById('eg');
  const c=['#8ec9e8','#b8ddf0','#4fa8d8','#cce8f7','#9dbfd3'];
  for(let i=0;i<72;i++){
    const d=document.createElement('div');
    d.style.background=c[i%c.length];
    d.style.opacity=(.08+Math.random()*.38).toFixed(2);
    g.appendChild(d);
  }
}

function initDrop(){
  const dz=document.getElementById('dz');
  const st=document.getElementById('stage');
  [dz,st].forEach(el=>{
    el.addEventListener('dragover',e=>{e.preventDefault();dz.classList.add('over')});
    el.addEventListener('dragleave',e=>{if(!dz.contains(e.relatedTarget))dz.classList.remove('over')});
    el.addEventListener('drop',e=>{
      e.preventDefault();dz.classList.remove('over');
      const f=e.dataTransfer.files[0];
      if(f&&f.type.startsWith('image/'))readFile(f);
      else showToast('Please drop an image file','err');
    });
  });
  document.getElementById('fi').addEventListener('change',e=>{
    if(e.target.files[0])readFile(e.target.files[0]);
    e.target.value='';
  });
}

function initPaste(){
  document.getElementById('psteBtn').onclick=()=>showToast('Press Ctrl+V / Cmd+V');
  document.addEventListener('paste',e=>{
    const it=[...e.clipboardData.items].find(x=>x.type.startsWith('image/'));
    if(it)readFile(it.getAsFile());
  });
}

function readFile(f){
  const r=new FileReader();
  r.onload=e=>loadSrc(e.target.result);
  r.readAsDataURL(f);
}

function loadSrc(src){
  const img=new Image();
  img.onload=()=>{
    hasImg=true;
    const W=img.naturalWidth,H=img.naturalHeight;

    const sc=document.getElementById('sC');
    sc.width=W;sc.height=H;
    sc.getContext('2d').drawImage(img,0,0);

    const oc=document.getElementById('oC');
    oc.width=W;oc.height=H;
    oc.getContext('2d').drawImage(img,0,0);

    document.getElementById('emp').style.display='none';
    const w=document.getElementById('cvW');
    w.classList.add('show');
    w.classList.remove('pop');void w.offsetWidth;w.classList.add('pop');

    setInfo('iS',W+'x'+H);
    setInfo('iO','—');setInfo('iB','—');setInfo('iC','—');
    document.getElementById('cvtBtn').disabled=false;
    document.getElementById('expBtn').disabled=true;
    r64=null;

    setView('out',document.getElementById('tR'));
    fitZoom();
    showToast('Image loaded','ok');
  };
  img.onerror=()=>showToast('Could not read image','err');
  img.src=src;
}

function fitZoom(){
  if(!hasImg)return;
  const oc=document.getElementById('oC');
  const W=oc.width,H=oc.height;
  if(!W||!H)return;
  const st=document.getElementById('stage');
  const aw=st.clientWidth-64,ah=st.clientHeight-64;
  zL=Math.min(1,aw/W,ah/H);
  zL=parseFloat(zL.toFixed(3));
  applyZoom();
}

function startConvert(){
  if(!hasImg)return;
  document.getElementById('cvtBtn').disabled=true;
  setProg(true,'Analyzing...');
  const sc=document.getElementById('sC');
  const b64=sc.toDataURL('image/png').split(',')[1];
  pywebview.api.convert(b64,pxO,cD,dS,eE).then(res=>{
    if(res.error){showToast(res.error,'err');setProg(false);document.getElementById('cvtBtn').disabled=false;return}
    setProg(true,'Rendering...',88);
    const img=new Image();
    img.onload=()=>{
      const sc=document.getElementById('sC');
      const dispW=sc.width,dispH=sc.height;
      const oc=document.getElementById('oC');
      oc.width=dispW;oc.height=dispH;
      oc.getContext('2d').imageSmoothingEnabled=false;
      oc.getContext('2d').drawImage(img,0,0,dispW,dispH);
      r64=res.image;
      setInfo('iO',img.naturalWidth+'x'+img.naturalHeight,true);
      setInfo('iB',res.block+'px',true);
      setInfo('iC',res.colors+'',true);
      document.getElementById('expBtn').disabled=false;
      setView('out',document.getElementById('tR'));
      fitZoom();
      setProg(true,'Done',100);
      setTimeout(()=>setProg(false),1300);
      showToast('Pixel art ready','ok');
      document.getElementById('cvtBtn').disabled=false;
    };
    img.src='data:image/png;base64,'+res.image;
  }).catch(e=>{showToast('Error: '+e,'err');setProg(false);document.getElementById('cvtBtn').disabled=false});
}

function exportImg(){
  if(!r64)return;
  pywebview.api.export_image(r64).then(r=>{
    if(r.ok)showToast('Saved: '+r.path,'ok');
    else showToast(r.error,'err');
  });
}

function setView(v,btn){
  view=v;
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  if(btn)btn.classList.add('active');
  document.getElementById('oC').style.display=v==='out'?'block':'none';
  document.getElementById('sC').style.display=v==='src'?'block':'none';
}

function dZoom(d){zL=Math.max(.05,Math.min(8,zL+d));applyZoom()}
function applyZoom(){
  const oc=document.getElementById('oC');
  const sc=document.getElementById('sC');
  if(!oc.width)return;
  const nw=Math.round(oc.width*zL);
  const nh=Math.round(oc.height*zL);
  oc.style.width=nw+'px';oc.style.height=nh+'px';
  sc.style.width=nw+'px';sc.style.height=nh+'px';
  document.getElementById('zV').textContent=Math.round(zL*100)+'%';
}

document.addEventListener('DOMContentLoaded',()=>{
  document.getElementById('stage').addEventListener('wheel',e=>{
    e.preventDefault();dZoom(e.deltaY<0?.1:-.1);
  },{passive:false});

  // Sidebar resize via drag
  const resizer=document.getElementById('resizer');
  const sidebar=document.querySelector('.sidebar');
  let isResizing=false,startX=0,startW=0;
  resizer.addEventListener('mousedown',e=>{
    isResizing=true;startX=e.clientX;startW=sidebar.offsetWidth;
    resizer.classList.add('dragging');
    document.body.style.cursor='col-resize';
    document.body.style.userSelect='none';
  });
  document.addEventListener('mousemove',e=>{
    if(!isResizing)return;
    const newW=Math.max(220,Math.min(480,startW+(e.clientX-startX)));
    sidebar.style.width=newW+'px';
    sidebar.style.flexShrink='0';
  });
  document.addEventListener('mouseup',()=>{
    if(!isResizing)return;
    isResizing=false;resizer.classList.remove('dragging');
    document.body.style.cursor='';document.body.style.userSelect='';
  });
});

function setProg(show,txt,pct){
  const p=document.getElementById('prog'),pb=document.getElementById('pb'),pt=document.getElementById('pt');
  if(!show){p.classList.remove('on');pb.style.width='0%';pb.classList.remove('indef');pt.textContent='';return}
  p.classList.add('on');pt.textContent=txt||'';
  if(pct!==undefined){pb.classList.remove('indef');pb.style.width=pct+'%'}
  else{pb.classList.add('indef')}
}

function setInfo(id,val,flash=false){
  const el=document.getElementById(id);
  el.textContent=val;
  if(flash){el.classList.add('flash');setTimeout(()=>el.classList.remove('flash'),1100)}
}

let _tt;
function showToast(msg,type=''){
  const el=document.getElementById('toast');
  el.textContent=msg;el.className='toast show'+(type?' '+type:'');
  clearTimeout(_tt);_tt=setTimeout(()=>el.classList.remove('show'),2800);
}
</script>
</body>
</html>
"""


class Api:
    def _auto_block(self, w, h):
        m = max(w, h)
        if m <= 128:  return 2
        if m <= 256:  return 3
        if m <= 512:  return 4
        if m <= 1024: return 5
        if m <= 2048: return 7
        if m <= 3000: return 9
        if m <= 4096: return 12
        return 14

    def _median_cut(self, pixels, depth):
        if depth == 0 or not pixels:
            n = len(pixels)
            return [(sum(p[0] for p in pixels)//n,
                     sum(p[1] for p in pixels)//n,
                     sum(p[2] for p in pixels)//n)]
        ranges = [max(p[c] for p in pixels) - min(p[c] for p in pixels) for c in range(3)]
        ch = ranges.index(max(ranges))
        pixels.sort(key=lambda p: p[ch])
        mid = len(pixels) // 2
        return self._median_cut(pixels[:mid], depth-1) + self._median_cut(pixels[mid:], depth-1)

    def _nearest(self, r, g, b, palette):
        best, bd = palette[0], float('inf')
        for p in palette:
            rm = (r + p[0]) / 2
            dr, dg, db = r - p[0], g - p[1], b - p[2]
            d = (2 + rm/256)*dr*dr + 4*dg*dg + (2 + (255-rm)/256)*db*db
            if d < bd:
                best, bd = p, d
        return best

    def convert(self, b64_data, px_override, color_depth, dither_strength, edge_enhance):
        try:
            data = base64.b64decode(b64_data)
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            w, h = img.size

            block = int(px_override) if int(px_override) > 0 else self._auto_block(w, h)
            gw = math.ceil(w / block)
            gh = math.ceil(h / block)

            small = img.resize((gw, gh), Image.LANCZOS)
            pixels = list(small.getdata())

            opaque = [p[:3] for p in pixels if p[3] > 30]
            if not opaque:
                return {"error": "Image has no visible content"}

            target = min(int(color_depth), 256)
            depth = min(8, max(1, math.ceil(math.log2(max(2, target)))))
            palette = self._median_cut(list(opaque), depth)
            palette = list(dict.fromkeys(palette))

            err = [[0.0, 0.0, 0.0] for _ in range(gw * gh)]
            quantized = []
            ds = float(dither_strength)

            for gy in range(gh):
                for gx in range(gw):
                    idx = gy * gw + gx
                    r, g, b, a = pixels[idx]
                    e = err[idx]
                    r2 = max(0, min(255, round(r + e[0])))
                    g2 = max(0, min(255, round(g + e[1])))
                    b2 = max(0, min(255, round(b + e[2])))
                    c = self._nearest(r2, g2, b2, palette)
                    quantized.append((*c, a))
                    if ds > 0:
                        er = (r2 - c[0]) * ds
                        eg = (g2 - c[1]) * ds
                        eb = (b2 - c[2]) * ds
                        for dx, dy, fw in ((1,0,7/16),(1,1,1/16),(0,1,5/16),(-1,1,3/16)):
                            nx, ny = gx+dx, gy+dy
                            if 0 <= nx < gw and 0 <= ny < gh:
                                ni = ny*gw+nx
                                err[ni][0] += er*fw
                                err[ni][1] += eg*fw
                                err[ni][2] += eb*fw

            if edge_enhance:
                enhanced = list(quantized)
                for gy in range(gh):
                    for gx in range(gw):
                        idx = gy*gw+gx
                        r, g, b, a = quantized[idx]
                        max_diff = 0
                        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                            nx, ny = gx+dx, gy+dy
                            if 0 <= nx < gw and 0 <= ny < gh:
                                n = quantized[ny*gw+nx]
                                rm = (r+n[0])/2
                                dr,dg,db = r-n[0],g-n[1],b-n[2]
                                d = (2+rm/256)*dr*dr + 4*dg*dg + (2+(255-rm)/256)*db*db
                                if d > max_diff:
                                    max_diff = d
                        if max_diff > 3500:
                            enhanced[idx] = (round(r*.87), round(g*.87), round(b*.87), a)
                quantized = enhanced

            # Output at 4K preserving original aspect ratio
            TARGET = 4096
            long_side = max(gw * block, gh * block)
            scale = max(1, TARGET // long_side)
            out_w = gw * block * scale
            out_h = gh * block * scale
            bs = block * scale

            out = Image.new("RGBA", (out_w, out_h))
            pix_out = out.load()
            for gy in range(gh):
                for gx in range(gw):
                    c = quantized[gy*gw+gx]
                    x0, y0 = gx*bs, gy*bs
                    for yy in range(y0, min(y0+bs, out_h)):
                        for xx in range(x0, min(x0+bs, out_w)):
                            pix_out[xx, yy] = c

            buf = io.BytesIO()
            out.save(buf, format="PNG", optimize=False)
            return {
                "image": base64.b64encode(buf.getvalue()).decode(),
                "block": block,
                "colors": len(palette)
            }
        except Exception as e:
            return {"error": str(e)}

    def export_image(self, b64_data):
        try:
            data = base64.b64decode(b64_data)
            img = Image.open(io.BytesIO(data))
            home = os.path.expanduser("~")
            pics = os.path.join(home, "Pictures")
            out_dir = pics if os.path.isdir(pics) else home
            path = os.path.join(out_dir, "pixora_export.png")
            i = 1
            while os.path.exists(path):
                path = os.path.join(out_dir, f"pixora_export_{i}.png")
                i += 1
            img.save(path, format="PNG", optimize=False)
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        "Pixora",
        html=HTML,
        js_api=api,
        width=1240,
        height=800,
        min_size=(980, 640),
        background_color="#e4f1fa",
    )
    webview.start(debug=False)
