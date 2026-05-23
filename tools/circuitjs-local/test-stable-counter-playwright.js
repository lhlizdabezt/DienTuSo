const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright-core");

const root = __dirname;
const edgePath =
  process.env.EDGE_PATH ||
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const outDir = path.join(root, "test-artifacts");
const circuitName = "roundabout_stable_counter.txt";

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function startServer() {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ["start-demo.js", circuitName, "--no-open"], {
      cwd: root,
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";
    const timeout = setTimeout(() => {
      child.kill();
      reject(new Error(`Timed out waiting for CircuitJS server.\n${stdout}\n${stderr}`));
    }, 15000);

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
      const match = stdout.match(/Demo URL:\s+(http:\/\/127\.0\.0\.1:\d+\/\S+)/);
      if (match) {
        clearTimeout(timeout);
        resolve({ child, url: match[1] });
      }
    });

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("exit", (code) => {
      if (!stdout.includes("Demo URL:")) {
        clearTimeout(timeout);
        reject(new Error(`CircuitJS server exited with code ${code}.\n${stdout}\n${stderr}`));
      }
    });
  });
}

async function canvasFingerprint(page) {
  return page.evaluate(() => {
    const canvas = document.querySelector("canvas");
    if (!canvas) {
      return null;
    }
    const context = canvas.getContext("2d", { willReadFrequently: true });
    const image = context.getImageData(0, 0, canvas.width, canvas.height).data;
    let hash = 2166136261;
    let red = 0;
    let yellow = 0;
    let green = 0;
    for (let i = 0; i < image.length; i += 4) {
      const r = image[i];
      const g = image[i + 1];
      const b = image[i + 2];
      const a = image[i + 3];
      hash ^= (r << 16) ^ (g << 8) ^ b ^ a;
      hash = Math.imul(hash, 16777619) >>> 0;
      if (r > 180 && g < 90 && b < 90) red += 1;
      if (r > 180 && g > 150 && b < 90) yellow += 1;
      if (g > 180 && r < 120 && b < 120) green += 1;
    }
    return {
      width: canvas.width,
      height: canvas.height,
      hash: hash.toString(16).padStart(8, "0"),
      red,
      yellow,
      green,
    };
  });
}

function bufferHash(buffer) {
  let hash = 2166136261;
  for (const byte of buffer) {
    hash ^= byte;
    hash = Math.imul(hash, 16777619) >>> 0;
  }
  return hash.toString(16).padStart(8, "0");
}

async function circuitState(page) {
  return page.evaluate(() => {
    const sim = window.CircuitJS1;
    if (!sim) {
      return null;
    }
    const labels = ["RA", "YA", "GA", "RB", "YB", "GB", "RC", "YC", "GC", "RD", "YD", "GD"];
    const voltages = {};
    for (const label of labels) {
      try {
        voltages[label] = sim.getNodeVoltage(label);
      } catch (error) {
        voltages[label] = null;
      }
    }
    return {
      running: sim.isRunning(),
      time: sim.getTime(),
      voltages,
    };
  });
}

async function main() {
  fs.mkdirSync(outDir, { recursive: true });

  const server = await startServer();
  let browser;
  try {
    browser = await chromium.launch({
      executablePath: edgePath,
      headless: true,
      args: ["--disable-gpu"],
    });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    await page.goto(server.url, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForFunction(() => window.CircuitJS1, null, { timeout: 30000 });
    await page.evaluate(() => window.CircuitJS1.setSimRunning(true));
    await wait(3000);

    const samples = [];
    for (let i = 0; i < 4; i += 1) {
      const file = path.join(outDir, `stable-counter-${i}.png`);
      await page.evaluate(() => window.CircuitJS1.setSimRunning(true));
      const screenshot = await page.screenshot({ path: file, fullPage: true });
      samples.push({
        file,
        screenshotHash: bufferHash(screenshot),
        fingerprint: await canvasFingerprint(page),
        state: await circuitState(page),
      });
      await wait(1500);
    }

    const uniqueScreenshotHashes = new Set(samples.map((sample) => sample.screenshotHash));
    const uniqueTimes = new Set(samples.map((sample) => sample.state && sample.state.time));
    const loaded = samples.every((sample) => sample.state);
    const animated = uniqueScreenshotHashes.size > 1 || uniqueTimes.size > 1;

    console.log(`URL: ${server.url}`);
    console.log(`CircuitJS API loaded: ${loaded ? "YES" : "NO"}`);
    console.log(`Page or simulation changed over time: ${animated ? "YES" : "NO"}`);
    for (const [index, sample] of samples.entries()) {
      const fp = sample.fingerprint;
      const state = sample.state;
      const high = state
        ? Object.entries(state.voltages)
            .filter(([, value]) => value !== null && value > 2.5)
            .map(([label]) => label)
            .join(",")
        : "";
      console.log(
        `sample ${index}: pageHash=${sample.screenshotHash} canvasHash=${fp && fp.hash} running=${state && state.running} time=${state && state.time} high=${high} file=${sample.file}`,
      );
    }

    if (!loaded || !animated) {
      process.exitCode = 1;
    }
  } finally {
    if (browser) {
      await browser.close();
    }
    server.child.kill();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
