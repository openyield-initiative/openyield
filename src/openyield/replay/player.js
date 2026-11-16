/* Presentation only. The trace and simulation are never modified. */
function createPlayback(frames) {
  let index = 0, playing = false, speed = 1, position = frames[0].time, last = null;
  const end = frames.at(-1).time;
  const player = {
    get index() { return index; }, get playing() { return playing; }, get speed() { return speed; },
    advance(now) {
      if (!playing) return;
      position = Math.min(end, position + Math.max(0, now - last) * speed / 1000); last = now;
      while (index < frames.length - 1 && frames[index + 1].time <= position + 1e-10) index++;
      if (position >= end) player.pause();
    },
    play(now) {if (index === frames.length - 1) player.restart(); playing = true; last = now;},
    pause() {playing = false; last = null;},
    seek(value) {index = Math.max(0, Math.min(frames.length - 1, Math.trunc(value))); position = frames[index].time; player.pause();},
    restart() {player.seek(0);},
    setSpeed(value, now) {if (![.5,1,2].includes(value)) throw new Error('Unsupported playback speed'); player.advance(now); speed = value;}
  };
  return player;
}

function describeFrame(frame, terminal, summary) {
  if (terminal) return {title:`Run ended: ${summary.outcome}`, detail:summary.reason};
  const [a,b] = frame.actions;
  const aId = frame.vehicles[0].id ?? 'A', bId = frame.vehicles[1].id ?? 'B';
  if (a === 'initial' && b === 'initial') return {title:'Starting positions', detail:'The recorded starting positions are shown before either vehicle moves.'};
  if (a === 'wait in passing space' && b === 'proceed west') {
    const cleared = frame.vehicles[1].x + frame.vehicles[1].length / 2 < frame.vehicles[0].x - frame.vehicles[0].length / 2;
    return cleared ? {title:`${bId} has cleared ${aId}`, detail:`${bId} has passed ${aId}. The scripted controller still keeps ${aId} waiting.`} :
      {title:`${aId} waits while ${bId} passes`, detail:`${aId} stays in the passing space while ${bId} proceeds west through the narrow corridor.`};
  }
  if (a === 'scripted lateral translation' && ['proceed west','wait at destination'].includes(b)) return {title:'Scripted lateral movement', detail:`${aId} slides sideways toward the corridor. Steering is not simulated.`};
  if (a === 'proceed east' && ['proceed west','wait at destination'].includes(b)) return {title:'Proceeding to destinations', detail:`${aId} proceeds east. ${bId} continues west or waits at its scripted destination.`};
  return {title:'Recorded actions', detail:frame.actions.join(' / ')};
}
function labelMetrics(displayWidth) {
  const font = Math.max(28, Math.ceil(12 * 1440 / Math.max(1, displayWidth)));
  return {font, external: displayWidth < 700};
}
if (typeof module !== 'undefined') module.exports = {createPlayback, describeFrame, labelMetrics};

if (typeof document !== 'undefined') {
  const trace = JSON.parse(document.getElementById('trace').textContent);
  const frames = trace.frames, scenario = trace.scenario, player = createPlayback(frames);
  const canvas = document.getElementById('view'), ctx = canvas.getContext('2d');
  const seek = document.getElementById('seek'), play = document.getElementById('play');
  const speed = document.getElementById('speed'), recording = document.getElementById('recording');
  document.getElementById('label-a').textContent = `${scenario.vehicles[0].id} · Eastbound`;
  document.getElementById('label-b').textContent = `${scenario.vehicles[1].id} · Westbound`;
  seek.max = frames.length - 1;
  const scale = Math.min(1280 / scenario.road.length, 320 / scenario.road.width);
  function bounds(r) {return [720 + (r.x - scenario.road.x - r.length/2)*scale, 225 - (r.y - scenario.road.y + r.width/2)*scale, r.length*scale, r.width*scale];}
  const hatch = document.createElement('canvas'); hatch.width = hatch.height = 16;
  const h = hatch.getContext('2d'); h.fillStyle='#384657'; h.fillRect(0,0,16,16); h.strokeStyle='#607083'; h.lineWidth=2; h.beginPath();
  h.moveTo(-4,4); h.lineTo(4,-4); h.moveTo(0,16); h.lineTo(16,0); h.moveTo(12,20); h.lineTo(20,12); h.stroke();
  const pattern = ctx.createPattern(hatch,'repeat');
  function rectangle(r, fill, stroke, dashed=false) {const box=bounds(r); ctx.fillStyle=fill; ctx.fillRect(...box); ctx.strokeStyle=stroke; ctx.lineWidth=2; ctx.setLineDash(dashed?[12,8]:[]); ctx.strokeRect(...box); ctx.setLineDash([]); return box;}
  function diagram(frame) {
    ctx.clearRect(0,0,1440,450); rectangle(scenario.road,'#24374a','#a9bccd'); rectangle(scenario.passing_space,'#1b6656','#8de2ba',true);
    scenario.obstacles.forEach(r=>rectangle(r,pattern,'#9eafbf'));
    const metrics = labelMetrics(canvas.getBoundingClientRect().width);
    const boxes = frame.vehicles.map((v,i)=>rectangle(v,i?'#ffb454':'#479cfa',i?'#ffe0ae':'#c6e3ff'));
    frame.vehicles.forEach((v,i)=>{
      const [x,y,w,h] = boxes[i], text = `${v.id} ${v.heading===0?'→':'←'}`;
      ctx.save(); ctx.font=`bold ${metrics.font}px system-ui`; ctx.textAlign='center'; ctx.textBaseline='middle';
      if (metrics.external) {
        // Callouts are annotations outside the exact footprint, never larger cars.
        const labelWidth = Math.min(420,ctx.measureText(text).width+20), labelHeight=metrics.font+12;
        const cx = Math.max(labelWidth/2+4,Math.min(1436-labelWidth/2,x+w/2));
        const cy = Math.max(labelHeight/2+4,Math.min(446-labelHeight/2,i ? y+h+labelHeight/2+12 : y-labelHeight/2-12));
        ctx.strokeStyle=i?'#ffb454':'#479cfa';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x+w/2,y+h/2);ctx.lineTo(cx,cy);ctx.stroke();
        ctx.fillStyle='#0a1220';ctx.fillRect(cx-labelWidth/2,cy-labelHeight/2,labelWidth,labelHeight);
        ctx.strokeRect(cx-labelWidth/2,cy-labelHeight/2,labelWidth,labelHeight);ctx.fillStyle='#eaf1fa';
        ctx.fillText(text,cx,cy,labelWidth-12);
      } else {
        ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();ctx.fillStyle='#081727';
        ctx.fillText(text,x+w/2,y+h/2,Math.max(1,w-8));
      }
      ctx.restore();
    });
  }
  let drawnIndex=-1, previousTitle='';
  function draw() {
    const frame=frames[player.index], terminal=player.index===frames.length-1;
    if (drawnIndex!==player.index) {
      diagram(frame); drawnIndex=player.index; const stage=describeFrame(frame,terminal,trace.summary);
      document.getElementById('stage-title').textContent=stage.title; document.getElementById('stage-detail').textContent=stage.detail;
      document.getElementById('stage-label').textContent=terminal?'FINAL RECORDED STATE':'SCRIPTED ENCOUNTER';
      document.getElementById('clock').textContent=`${frame.time.toFixed(2)} s`;
      document.getElementById('frame-count').textContent=`${player.index} / ${frames.length-1}`;
      seek.value=player.index; seek.setAttribute('aria-valuetext',`Frame ${player.index}, ${frame.time.toFixed(2)} seconds`); previousTitle=stage.title;
    }
    play.textContent=player.playing?'Pause':terminal?'Play again':'Play';
    const status = document.getElementById('playback-status');
    const message = `${player.playing?'Playing':'Paused'} · ${player.speed}× viewing speed · ${previousTitle}`;
    if (status.textContent !== message) status.textContent = message;
  }
  play.onclick=()=>{if(player.playing){player.advance(performance.now());player.pause();}else player.play(performance.now());draw();};
  document.getElementById('restart').onclick=()=>{player.restart();draw();};
  seek.oninput=()=>{player.seek(Number(seek.value));draw();};
  speed.onchange=()=>{player.setSpeed(Number(speed.value),performance.now());draw();};
  recording.onclick=()=>{const enabled=document.body.classList.toggle('recording');recording.setAttribute('aria-pressed',String(enabled));};
  document.addEventListener('visibilitychange',()=>{if(document.hidden){player.pause();draw();}});
  new ResizeObserver(()=>{drawnIndex=-1;draw();}).observe(canvas);
  function tick(now){if(player.playing){player.advance(now);draw();}requestAnimationFrame(tick);}
  draw();requestAnimationFrame(tick);
}
