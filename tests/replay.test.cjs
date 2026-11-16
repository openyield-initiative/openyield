const {test} = require('node:test');
const assert = require('node:assert/strict');
const {createPlayback, describeFrame, labelMetrics} = require('../src/openyield/replay/player.js');
const frames = [0, .25, .5, .75, 1].map(time => ({time}));

test('starts paused, catches up by elapsed time and stops at final frame', () => {
  const p = createPlayback(frames);
  p.advance(1000);
  assert.equal(p.index, 0);
  assert.equal(p.playing, false);
  p.play(1000);
  p.advance(1750);
  assert.equal(p.index, 3);
  p.advance(5000);
  assert.equal(p.index, 4);
  assert.equal(p.playing, false);
});

test('speed change preserves elapsed progress; scrub and restart pause', () => {
  const p = createPlayback(frames);
  p.setSpeed(.5, 0);
  p.play(0);
  p.advance(500);
  assert.equal(p.index, 1);
  p.setSpeed(2, 500);
  p.advance(750);
  assert.equal(p.index, 3);
  p.seek(1);
  assert.equal(p.playing, false);
  p.play(10000);
  p.advance(10125);
  assert.equal(p.index, 2);
  p.restart();
  assert.equal(p.index, 0);
  assert.equal(p.playing, false);
});

test('pause prevents hidden-page catchup and play from end restarts', () => {
  const p = createPlayback(frames);
  p.play(0);
  p.advance(250);
  p.pause(); // visibilitychange calls this same operation
  p.advance(90000);
  assert.equal(p.index, 1);
  p.play(90000);
  p.advance(90250);
  assert.equal(p.index, 2);
  p.seek(4);
  p.play(91000);
  assert.equal(p.index, 0);
});

test('fractional elapsed time survives frequent updates and paused speed changes', () => {
  const p = createPlayback(frames);
  p.play(0);
  for (let now = 10; now <= 250; now += 10) p.advance(now);
  assert.equal(p.index, 1);
  p.pause();
  p.setSpeed(2, 1000);
  assert.equal(p.playing, false);
  assert.throws(() => p.setSpeed(0, 1000));
});

test('stage descriptions use recorded actions, not fixed times or early success', () => {
  const a = {x:12,length:4}, b = {x:5,length:4};
  const make = actions => ({time:10,actions,vehicles:[a,b]});
  const summary = {outcome:'success',reason:'destinations reached'};
  assert.match(describeFrame(make(['wait in passing space','proceed west']), false, summary).title, /cleared/i);
  assert.match(describeFrame(make(['scripted lateral translation','proceed west']), false, summary).detail, /steering is not simulated/i);
  assert.match(describeFrame(make(['custom','other']), false, summary).detail, /custom.*other/);
  assert.doesNotMatch(describeFrame(make(['initial','initial']), false, summary).title, /success|completed/i);
  assert.match(describeFrame(make(['proceed east','wait at destination']), true, summary).title, /success/i);
  assert.match(describeFrame(make(['initial','initial']), true, {outcome:'violation',reason:'road boundary'}).detail, /road boundary/);
  assert.match(describeFrame(make(['initial','initial']), true, {outcome:'timeout',reason:'duration reached'}).title, /timeout/i);
});

test('captions identify configured vehicles instead of assuming IDs A and B', () => {
  const frame = {actions:['wait in passing space','proceed west'], vehicles:[
    {id:'East-17',x:12,length:4}, {id:'West-24',x:26,length:4}
  ]};
  assert.match(describeFrame(frame,false,{}).detail, /East-17.*West-24/);
});

test('mobile callout font remains at least twelve displayed pixels', () => {
  for (const width of [280,317,390]) {
    const metrics = labelMetrics(width);
    assert.equal(metrics.external, true);
    assert.ok(metrics.font * width / 1440 >= 12);
  }
  assert.equal(labelMetrics(1200).external, false);
});
