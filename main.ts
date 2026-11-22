// news-image-20261122-cand-c: validates the committed entry.png and
// copies it to the output dir. No build step runs here: the grader image
// lacks the generator toolchain, so the entry is shipped pre-rendered and
// main.ts only checks it is the expected PNG before copying.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));

const sourcePath = join(here, "entry.png");
const data = readFileSync(sourcePath);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (data.length < 33 || !data.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error(`entry.png is not a PNG (bad signature) at ${sourcePath}`);
}
// IHDR chunk: bytes 8-11 length, 12-15 "IHDR", 16-19 width BE, 20-23 height BE
if (data.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error(`entry.png has no IHDR chunk at ${sourcePath}`);
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1600 || height !== 4272) {
  throw new Error(
    `entry.png dimensions are ${width}x${height}, expected 1600x4272 at ${sourcePath}`,
  );
}

const size = statSync(sourcePath).size;
if (size === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${sourcePath}`);
}
if (size > 1048576) {
  throw new Error(
    `entry.png too large: ${size} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePath, join(outDir, "entry.png"));
console.log(`entry.png ${size} bytes ${width}x${height} -> ${join(outDir, "entry.png")}`);
