'use strict';

const assert = require('node:assert/strict');

const validSequence = [8, 9, 10, 11, 12, 0, 1, 2, 3, 4];
const validStates = new Set(validSequence);

function bit(state, index) {
  return (state >> index) & 1;
}

function jkNext(q, j, k) {
  return (j && !q) || (!k && q) ? 1 : 0;
}

function nextState(state) {
  const q3 = bit(state, 3);
  const q2 = bit(state, 2);
  const q1 = bit(state, 1);
  const q0 = bit(state, 0);

  const n3 = jkNext(q3, q2, q2);
  const n2 = jkNext(q2, q1 && q0, 1);
  const n1 = jkNext(q1, q0, q0);
  const n0 = jkNext(q0, !q2, 1);

  return (n3 << 3) | (n2 << 2) | (n1 << 1) | n0;
}

function decoder(state) {
  const q3 = bit(state, 3);
  const q2 = bit(state, 2);
  return {
    acGreen: Boolean(q3 && !q2),
    acYellow: Boolean(q3 && q2),
    acRed: Boolean(!q3),
    bdGreen: Boolean(!q3 && !q2),
    bdYellow: Boolean(!q3 && q2),
    bdRed: Boolean(q3),
  };
}

for (let index = 0; index < validSequence.length; index += 1) {
  const state = validSequence[index];
  const expected = validSequence[(index + 1) % validSequence.length];
  assert.equal(nextState(state), expected, `state ${state} must advance to ${expected}`);
}

const unusedStates = Array.from({ length: 16 }, (_, state) => state).filter(
  (state) => !validStates.has(state),
);
for (const state of unusedStates) {
  assert.ok(validStates.has(nextState(state)), `unused state ${state} must recover in one clock edge`);
}

for (let state = 0; state < 16; state += 1) {
  const outputs = decoder(state);
  assert.ok(!(outputs.acGreen && outputs.bdGreen), `state ${state} violates green-phase exclusion`);
  assert.equal(
    Number(outputs.acGreen) + Number(outputs.acYellow) + Number(outputs.acRed),
    1,
    `state ${state} must select one A/C color`,
  );
  assert.equal(
    Number(outputs.bdGreen) + Number(outputs.bdYellow) + Number(outputs.bdRed),
    1,
    `state ${state} must select one B/D color`,
  );
}

console.log('PASS: 10 valid state transitions follow the 4-1-4-1 sequence.');
console.log('PASS: 6 unused states recover to the valid sequence in one clock edge.');
console.log('PASS: all 16 decoder inputs preserve mutually exclusive green phases.');
