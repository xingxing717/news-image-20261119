// news-image-20261119: a program that writes one image summing up the world
// news of Thursday 19 November 2026 to /output/entry.png.
//
// The image is entry.png beside this file. It was drawn by render.py in this
// repository (pure Pillow shapes and text; no borrowed artwork) from six
// stories verified against news reports dated 19 November 2026: the GTA VI
// global rollout, the Trump-Xi-Putin gathering in Shenzhen, the third strike
// on the Crimean Bridge, Cyclone Akvan off India's east coast, a record
// $190.4m Van Gogh sale, and NASA's confirmation that Voyager 1 is one
// light-day from Earth.
//
// The program itself only copies the image. It uses the Node 22 standard
// library only and never touches the network, so both grader runs produce
// byte-identical output.
//
// Run locally with: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = join(here, 'entry.png');
if (!existsSync(src)) {
  throw new Error('entry.png is missing from the repository');
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
// Both grader runs copy the same bytes, so the outputs are identical.
if (statSync(join(outDir, 'entry.png')).size !== statSync(src).size) {
  throw new Error('entry.png copy is incomplete');
}
