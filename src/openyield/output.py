"""Trace serialization and offline rendering; no simulation logic."""
import json
from pathlib import Path


def export(scenario, result, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    trace = json.dumps(result, indent=2, allow_nan=False)
    (destination / "trace.json").write_text(trace + "\n", encoding="utf-8")
    (destination / "summary.json").write_text(
        json.dumps(result["summary"], indent=2, allow_nan=False) + "\n", encoding="utf-8")
    # Escape markup even when user-supplied IDs contain closing script tags.
    payload = json.dumps(result, allow_nan=False).replace("<", "\\u003c")
    (destination / "replay.html").write_text(HTML.replace("__TRACE__", payload), encoding="utf-8")


HTML = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenYield scripted replay</title>
<style>body{background:#111827;color:#eee;font:18px system-ui;margin:3vw}
canvas{background:#293548;width:100%;max-width:1200px}button,input{margin:12px}</style>
<h1>OpenYield v0.1 — scripted encounter</h1>
<p>Demonstration only. Fixed rectangles and lateral translation; no negotiation or steering model.</p>
<canvas id="view" width="1200" height="400" aria-label="Top-down encounter replay"></canvas>
<div><button id="play">Pause</button><input id="seek" aria-label="Frame" type="range" min="0" value="0"></div>
<p id="status"></p><p>Green: passing space · Grey: parked obstacles · Blue: A · Orange: B. Units: metres.</p>
<script>
const trace=__TRACE__, frames=trace.frames, s=trace.scenario;
const canvas=document.getElementById('view'), ctx=canvas.getContext('2d');
const seek=document.getElementById('seek'), play=document.getElementById('play');
let index=0, playing=true, last=0; seek.max=frames.length-1;
const scale=Math.min(1100/s.road.length,280/s.road.width);
function rect(r,color,label){const x=600+(r.x-s.road.x-r.length/2)*scale;
const y=200-(r.y-s.road.y+r.width/2)*scale;
ctx.fillStyle=color;ctx.fillRect(x,y,r.length*scale,r.width*scale);
if(label){ctx.fillStyle='white';ctx.font='18px system-ui';ctx.fillText(label,x+8,y+22);}}
function draw(){ctx.clearRect(0,0,1200,400);rect(s.road,'#596575');
rect(s.passing_space,'#287557','passing space');s.obstacles.forEach(o=>rect(o,'#252d38','parked'));
const f=frames[index];f.vehicles.forEach((v,i)=>rect(v,i?'#ce741a':'#166ac4',v.id+(v.heading===0?' →':' ←')));
document.getElementById('status').textContent='t = '+f.time.toFixed(2)+' s | '+f.actions.join(' / ')+
' | outcome: '+trace.summary.outcome+' — '+trace.summary.reason;seek.value=index;}
play.onclick=()=>{if(index===frames.length-1)index=0;playing=!playing;play.textContent=playing?'Pause':'Play';draw();};
seek.oninput=()=>{index=Number(seek.value);playing=false;play.textContent='Play';draw();};
function tick(now){if(playing && now-last>=s.dt*1000){index=Math.min(index+1,frames.length-1);last=now;
if(index===frames.length-1){playing=false;play.textContent='Play';}draw();}requestAnimationFrame(tick);}
draw();requestAnimationFrame(tick);
</script></html>'''
