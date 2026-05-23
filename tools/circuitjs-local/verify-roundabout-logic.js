function stateBits(n) {
  return {
    q0: Boolean(n & 1),
    q1: Boolean(n & 2),
    q2: Boolean(n & 4),
    q3: Boolean(n & 8),
  };
}

function decode(n, opts = {}) {
  const { emergency = false, night = false, clock = false } = opts;
  const normal = !emergency && !night;
  const flashYellow = night && !emergency && clock;
  const phase = [
    "A_G",
    "A_Y",
    "ALL_RED",
    "B_G",
    "B_Y",
    "ALL_RED",
    "C_G",
    "C_Y",
    "ALL_RED",
    "D_G",
    "D_Y",
    "ALL_RED",
  ][n % 12];

  const out = {
    A: { R: false, Y: false, G: false },
    B: { R: false, Y: false, G: false },
    C: { R: false, Y: false, G: false },
    D: { R: false, Y: false, G: false },
  };

  for (const key of Object.keys(out)) {
    const active = phase === `${key}_G` || phase === `${key}_Y`;
    out[key].R = emergency || (normal && !active);
    out[key].G = normal && phase === `${key}_G`;
    out[key].Y = flashYellow || (normal && phase === `${key}_Y`);
  }

  return { bits: stateBits(n), phase, out };
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

for (let n = 0; n < 12; n++) {
  const { phase, out } = decode(n);
  const greenCount = Object.values(out).filter((x) => x.G).length;
  const yellowCount = Object.values(out).filter((x) => x.Y).length;
  const redCount = Object.values(out).filter((x) => x.R).length;
  if (phase === "ALL_RED") {
    assert(redCount === 4 && greenCount === 0 && yellowCount === 0, `state ${n} should be all red`);
  } else if (phase.endsWith("_G")) {
    assert(greenCount === 1 && redCount === 3 && yellowCount === 0, `state ${n} should be one green`);
  } else if (phase.endsWith("_Y")) {
    assert(yellowCount === 1 && redCount === 3 && greenCount === 0, `state ${n} should be one yellow`);
  }
  console.log(`${n.toString().padStart(2, "0")} ${phase.padEnd(7)} A=${fmt(out.A)} B=${fmt(out.B)} C=${fmt(out.C)} D=${fmt(out.D)}`);
}

const emergency = decode(0, { emergency: true }).out;
assert(Object.values(emergency).every((x) => x.R && !x.Y && !x.G), "emergency should force all red");

const nightOn = decode(0, { night: true, clock: true }).out;
assert(Object.values(nightOn).every((x) => !x.R && x.Y && !x.G), "night clock high should flash all yellow");

const nightOff = decode(0, { night: true, clock: false }).out;
assert(Object.values(nightOff).every((x) => !x.R && !x.Y && !x.G), "night clock low should turn lamps off");

console.log("OK: normal cycle, emergency mode, and night mode passed.");

function fmt(x) {
  return `${x.R ? "R" : "-"}${x.Y ? "Y" : "-"}${x.G ? "G" : "-"}`;
}
