/* Data-driven screen replay. The method rail is shared with article case embeds. */
window.DemoReplay = (() => {
  const make = EvidenceUI.make, timing = DemoTiming;
  const seconds = n => n.toFixed(2) + ' s';
  const button = (label, cls, title = label) => {
    const b = make('button', cls, label); b.type = 'button'; b.setAttribute('aria-label', title); return b;
  };
  async function mount(root, {data, base}) {
    let playing = false, speed = 1, previousFrame = 0, raf = 0, dialog;
    const views = [], duration = Math.max(...data.runs.map(r => r.total));
    const playback = timing.createClock(data.runs);
    root.classList.add('evidence-reader');
    const displayName = run => run.label + (run.precision === 'BF16' ? '' : ' ' + run.precision);
    // Decode all snapshots before playback: no blank image between decisions or methods.
    const urls = [...new Set(data.runs.flatMap(r => [...r.steps.map(s => s.image), r.final]))];
    async function decode(path) {
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          await new Promise((resolve, reject) => {
            const image = new Image(); image.onload = () => image.decode().then(resolve, reject);
            image.onerror = () => reject(Error('Could not load replay screenshot: ' + path));
            image.src = new URL(path, base).href;
          });
          return;
        } catch (error) {
          if (attempt === 1) throw error;
          await new Promise(resolve => setTimeout(resolve, 250));
        }
      }
    }
    // Bound image requests so a cold load also works on small local preview servers.
    let nextImage = 0;
    await Promise.all(Array.from({length:3}, async () => {
      while (nextImage < urls.length) await decode(urls[nextImage++]);
    }));
    root.replaceChildren();
    const railRoot = make('div'); root.append(railRoot);
    const controls = make('div', 'replay-controls'), play = button('Play', 'replay-play', 'Play synchronized replay');
    const clock = make('span', 'replay-clock'), clockValue = make('output', '', '0.00'); clockValue.setAttribute('aria-live', 'off'); clock.append(clockValue, ' / ' + seconds(duration));
    const seek = make('input', 'replay-seek'); seek.type = 'range'; seek.min = 0; seek.max = duration; seek.step = 'any'; seek.value = 0; seek.setAttribute('aria-label', 'Shared replay time in seconds');
    const rateLabel = make('label', 'replay-rate', 'Speed'), rate = make('select'); rate.setAttribute('aria-label', 'Playback speed');
    for (const value of [.5, 1, 2]) { const option = make('option', '', value + '×'); option.value = value; option.selected = value === 1; rate.append(option); }
    rateLabel.append(rate); controls.append(play, clock, seek, rateLabel);
    const key = make('div', 'replay-key');
    for (const [phase, name] of [['infer', 'Model inference'], ['act', 'Environment execution'], ['observe', 'Observation & overhead']]) {
      const item = make('span', '', name); item.dataset.phase = phase; item.prepend(make('i')); key.append(item);
    }
    function setPlaying(value) {
      playing = value; play.textContent = playing ? 'Pause' : playback.time >= duration ? 'Replay' : 'Play';
      play.setAttribute('aria-label', playing ? 'Pause synchronized replay' : 'Play synchronized replay');
      views.forEach(v => { v.screen.dataset.active = String(playing && !playback.isLocal(v.run.id)); });
      cancelAnimationFrame(raf); previousFrame = 0;
      if (playing) raf = requestAnimationFrame(tick);
    }
    function tick(now) {
      if (!playing) return;
      if (previousFrame) playback.advance((now - previousFrame) / 1000 * speed);
      previousFrame = now; render();
      if (playback.time >= duration) setPlaying(false); else raf = requestAnimationFrame(tick);
    }
    function jump(value) { playback.seekAll(value); setPlaying(false); render(); }
    function inspect(id, value) { playback.seekRun(id, value); render(); }
    function openScreen(view) {
      setPlaying(false);
      if (!dialog) {
        dialog = make('dialog', 'replay-dialog'); document.body.append(dialog);
        dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
      }
      const header = make('header'), title = make('h3', '', displayName(view.run)), close = button('Close', '');
      title.id = 'replay-dialog-title-' + data.id; close.onclick = () => dialog.close(); header.append(title, close);
      const screen = view.screen.cloneNode(true); screen.dataset.active = 'false';
      const state = timing.at(view.run, playback.forRun(view.run.id));
      dialog.replaceChildren(header, screen, make('p', '', `Step ${state.step.index + 1} · ${state.step.title}`));
      dialog.setAttribute('aria-labelledby', title.id); dialog.showModal(); close.focus();
    }
    function card(run) {
      const node = make('section', 'replay-card'); node.dataset.method = run.id;
      const heading = make('header', 'replay-heading');
      const stats = make('p'); stats.append('Inference ', make('strong', '', seconds(run.inference)), ' · Total ', make('strong', '', seconds(run.total)));
      const methodTitle = make('h3', '', run.label);
      if (run.precision !== 'BF16') methodTitle.append(make('span', 'replay-precision', run.precision));
      heading.append(methodTitle, stats);
      const body = make('div', 'replay-body'), screenButton = button('', 'replay-screen-button', `Enlarge ${run.label} screen`), screen = make('div', 'replay-screen');
      const img = make('img'); img.width = data.width; img.height = data.height;
      const tap = make('span', 'replay-tap'), input = make('div', 'replay-input');
      const swipe = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      swipe.classList.add('replay-swipe'); swipe.setAttribute('viewBox', `0 0 ${data.width} ${data.height}`); swipe.setAttribute('aria-hidden', 'true');
      const swipePath = document.createElementNS(swipe.namespaceURI, 'path'); swipe.append(swipePath); tap.hidden = input.hidden = true; tap.setAttribute('aria-hidden', 'true');
      screen.append(img, tap, swipe, input); screenButton.append(screen);
      const reading = make('div', 'replay-reading'), stateLine = make('p', 'replay-state'), stepLabel = make('span'), phaseLabel = make('span'), title = make('h4');
      stateLine.append(stepLabel, phaseLabel);
      const output = make('div', 'replay-output'); output.setAttribute('role', 'region'); output.setAttribute('aria-label', run.label + ' current model output');
      const stepNav = make('div', 'replay-step-nav'), previous = button('Previous', '', run.label + ': previous decision'), next = button('Next', '', run.label + ': next decision'); stepNav.append(previous, next);
      reading.append(stateLine, title, output, stepNav); body.append(screenButton, reading);
      const timingBox = make('div', 'replay-timing'), timingLabel = make('div', 'replay-timing-label'), timeline = make('div', 'replay-timeline'), head = make('span', 'replay-playhead');
      timeline.setAttribute('aria-label', run.label + ' decisions');
      const steps = run.steps.map(s => {
        const b = button('', 'replay-step', `${run.label}, step ${s.index + 1}: ${s.title}. Inference ${seconds(s.actStart - s.inferStart)}, execution ${seconds(s.end - s.actStart)}`);
        b.style.left = 100 * s.start / duration + '%'; b.style.width = 100 * (s.end - s.start) / duration + '%'; b.title = `Step ${s.index + 1} · ${s.title}`;
        for (const [phase, span] of [['observe', s.inferStart - s.start], ['infer', s.actStart - s.inferStart], ['act', s.end - s.actStart]]) { const piece = make('span'); piece.dataset.phase = phase; piece.style.width = 100 * span / (s.end - s.start) + '%'; b.append(piece); }
        b.onclick = () => inspect(run.id, timing.decisionTime(s)); timeline.append(b); return b;
      });
      const scale = make('div', 'replay-scale'), end = make('span', '', seconds(run.total));
      end.style.left = 100 * run.total / duration + '%'; scale.append(make('span', '', '0 s'), end);
      timeline.append(head); timingBox.append(timingLabel, timeline, scale); node.append(heading, body, timingBox);
      const view = {run, node, screen, img, tap, swipe, swipePath, input, stepLabel, phaseLabel, title, output, timingLabel, head, steps, previous, next, cache:''};
      previous.onclick = () => { const state = timing.at(run, playback.forRun(run.id)); inspect(run.id, timing.decisionTime(run.steps[Math.max(0, state.step.index - 1)])); };
      next.onclick = () => { const localTime = playback.forRun(run.id), state = timing.at(run, localTime); const i = Math.min(run.steps.length - 1, state.step.index + (localTime >= state.step.actStart ? 1 : 0)); inspect(run.id, timing.decisionTime(run.steps[i])); };
      screenButton.onclick = () => openScreen(view); views.push(view); return node;
    }
    const items = data.runs.map(run => ({id:run.id, title:run.label, detail:run.precision === 'BF16' ? '' : run.precision, node:card(run)}));
    const rail = ArticleCaseRail.mount(railRoot, {id:data.id + '-demo', label:data.title + ' replay', language:'en', items, initial:'bf16', stability:'content'});
    railRoot.querySelector('.rail-toolbar').after(controls);
    controls.append(key);
    function render() {
      clockValue.value = playback.time.toFixed(2); seek.value = playback.time; seek.setAttribute('aria-valuetext', seconds(playback.time));
      for (const v of views) {
        const s = timing.at(v.run, playback.forRun(v.run.id)), step = s.step, available = s.phase === 'act' || s.finished;
        v.timingLabel.replaceChildren(make('span', '', `Inference ${seconds(s.inference)} · Execution ${seconds(s.execution)}`), make('span', 'replay-local-time', `${playback.isLocal(v.run.id) ? 'Local · ' : ''}${seconds(s.time)}`));
        v.screen.dataset.active = String(playing && !playback.isLocal(v.run.id) && !s.finished);
        v.head.style.left = Math.min(100, s.time / duration * 100) + '%';
        const outputStep = available ? step : v.run.steps[step.index - 1];
        const cache = `${step.index}:${s.phase}`;
        if (cache === v.cache) continue; v.cache = cache;
        const image = new URL(s.finished ? v.run.final : step.image, base).href;
        if (v.img.src !== image) v.img.src = image;
        v.img.alt = `${v.run.label}, step ${step.index + 1}: ${step.title}${s.finished ? ', final screen' : ''}`;
        v.stepLabel.textContent = `Step ${step.index + 1} / ${v.run.steps.length}`;
        v.phaseLabel.textContent = s.finished ? (v.run.success ? 'Completed' : 'Not completed') : ({observe:'Observing', infer:'Thinking', act:'Executing'})[s.phase];
        v.phaseLabel.classList.toggle('replay-outcome', s.finished);
        v.phaseLabel.dataset.failed = String(s.finished && !v.run.success);
        v.title.textContent = step.title;
        v.previous.disabled = step.index === 0; v.next.disabled = step.index === v.run.steps.length - 1 && available;
        v.steps.forEach((b, i) => { if (i === step.index) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current'); });
        const action = step.executed, executing = s.phase === 'act';
        v.tap.hidden = !(executing && action.action === 'tap');
        if (!v.tap.hidden) { v.tap.style.left = 100 * action.x / data.width + '%'; v.tap.style.top = 100 * action.y / data.height + '%'; }
        v.swipe.style.display = executing && action.action === 'swipe' ? '' : 'none';
        if (executing && action.action === 'swipe') {
          const {x1,y1,x2,y2} = action, angle = Math.atan2(y2-y1,x2-x1), size = 20;
          const a = [x2-size*Math.cos(angle-.5),y2-size*Math.sin(angle-.5)], b = [x2-size*Math.cos(angle+.5),y2-size*Math.sin(angle+.5)];
          v.swipePath.setAttribute('d', `M${x1} ${y1}L${x2} ${y2}M${a[0]} ${a[1]}L${x2} ${y2}L${b[0]} ${b[1]}`);
        }
        v.input.hidden = !(executing && ['input_text', 'press_enter'].includes(action.action));
        if (!v.input.hidden) v.input.replaceChildren(make('small', '', action.action === 'input_text' ? 'Typing' : 'Key press'), document.createTextNode(action.text || 'Enter'));
        v.output.replaceChildren(); v.output.scrollTop = 0;
        if (!outputStep) v.output.append(make('p', 'replay-waiting', s.phase === 'infer' ? 'Generating the next action…' : 'Reading the screen…'));
        else {
          if (!available) v.output.append(make('p', 'replay-previous-output', `Latest output · step ${outputStep.index + 1}`));
          const thought = make('p', 'ev-prose'); thought.lang = v.run.id === 'qad' ? 'en' : 'zh-CN';
          thought.append(EvidenceUI.highlightedText(outputStep.thought, outputStep.thoughtHighlights));
          const thoughtFrame = EvidenceUI.frame('Thinking', thought);
          const thoughtBody = thoughtFrame.querySelector('.ev-body'); thoughtBody.tabIndex = 0; thoughtBody.setAttribute('role', 'region'); thoughtBody.setAttribute('aria-label', v.run.label + ' thinking');
          v.output.append(thoughtFrame);
          const actionFrame = EvidenceUI.frame('Action', EvidenceUI.action(outputStep.actionEvent), {tone:outputStep.actionEvent.tone === 'neutral' ? '' : outputStep.actionEvent.tone});
          const actionBody = actionFrame.querySelector('.ev-body'); actionBody.tabIndex = 0; actionBody.setAttribute('role', 'region'); actionBody.setAttribute('aria-label', v.run.label + ' action');
          v.output.append(actionFrame);
        }
      }
    }
    play.onclick = () => {
      if (!playing) playback.seekAll(playback.time >= duration ? 0 : playback.time);
      setPlaying(!playing); render();
    };
    seek.addEventListener('input', () => jump(Number(seek.value)));
    rate.onchange = () => { speed = Number(rate.value); };
    const onVisibility = () => { if (document.hidden) setPlaying(false); };
    document.addEventListener('visibilitychange', onVisibility);
    const visibility = new IntersectionObserver(entries => { if (!entries[0].isIntersecting) setPlaying(false); });
    visibility.observe(root);
    render(); root.dataset.ready = 'true';
    return {
      pause: () => setPlaying(false),
      activate: () => render(),
      destroy() { setPlaying(false); visibility.disconnect(); document.removeEventListener('visibilitychange', onVisibility); rail.destroy(); dialog?.remove(); }
    };
  }
  return {mount};
})();
