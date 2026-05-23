const fs = require("fs");
const http = require("http");
const path = require("path");
const vm = require("vm");
const { exec } = require("child_process");

const root = __dirname;
const preferredPort = Number(process.env.PORT || 8008);
const openBrowser = !process.argv.includes("--no-open");
const circuitName =
  process.env.CIRCUIT ||
  process.argv.find((arg) => arg.endsWith(".txt")) ||
  "roundabout_demo_clean.txt";
const circuitPath = circuitName.includes("/") || circuitName.includes("\\")
  ? circuitName.replace(/\\/g, "/")
  : `circuits/${circuitName}`;

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css; charset=utf-8",
  }[ext] || "application/octet-stream";
}

function makeCtz() {
  const circuitText = fs.readFileSync(path.join(root, circuitPath), "utf8");
  const lzCode = fs.readFileSync(path.join(root, "lz-string.min.js"), "utf8");
  const context = {};
  vm.createContext(context);
  vm.runInContext(`${lzCode};this.LZString=LZString;`, context);
  return context.LZString.compressToEncodedURIComponent(circuitText);
}

function makeServer() {
  return http.createServer((req, res) => {
    const rawPath = decodeURIComponent(new URL(req.url, "http://local").pathname);
    if (rawPath === "/demo") {
      res.writeHead(302, {
        Location: `/circuitjs.html?ctz=${makeCtz()}`,
      });
      res.end();
      return;
    }
    const safePath = path.normalize(rawPath).replace(/^(\.\.[/\\])+/, "");
    let filePath = path.join(root, safePath === "/" ? "circuitjs.html" : safePath);
    if (!filePath.startsWith(root)) {
      res.writeHead(403);
      res.end("Forbidden");
      return;
    }
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end("Not found");
        return;
      }
      res.writeHead(200, { "Content-Type": contentType(filePath) });
      res.end(data);
    });
  });
}

function listen(port) {
  const server = makeServer();
  server.on("error", (err) => {
    if (err.code === "EADDRINUSE" && port < preferredPort + 20) {
      listen(port + 1);
      return;
    }
    throw err;
  });
  server.listen(port, "127.0.0.1", () => {
    const url = `http://127.0.0.1:${port}/demo`;
    console.log(`CircuitJS local server: http://127.0.0.1:${port}/`);
    console.log(`Demo URL: ${url}`);
    console.log(`Circuit file: tools/circuitjs-local/${circuitPath}`);
    console.log("Press Ctrl+C to stop the local server.");
    if (openBrowser) {
      exec(`cmd /c start "" "${url}"`);
    }
  });
}

listen(preferredPort);
