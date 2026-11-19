// gta6-meme-x-01 entrypoint (Node 22, standard library only).
//
// The entry here is not a program the judge runs for fun: it is a single
// X post. The agent drew a GTA 6 meme, the user posted it on X from a
// public account with the make.fun ghost and the account's play code in
// its text, and this repository points at that post through POST.json.
// All this program does is hand that pointer to the gate: it reads
// POST.json from the repository root, checks it really names one X post,
// and copies it to /output/POST.json. The house then fetches the post
// itself (first picture + text) and builds the dossier the judge sees.
// Nothing written by this program is judged — only the post is.
//
// Local run (mirrors the grader, which mounts the repo at /bot and
// expects output at /output):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const POST_FILE = join(BOT_DIR, 'POST.json');

// Read POST.json first and make sure it is a real pointer before the
// gate ever sees it: a JSON object whose "url" is a string naming one
// post. Anything else fails loudly here instead of silently handing
// the gate a file it will refuse.
let postUrl: string;
try {
  const parsed: unknown = JSON.parse(readFileSync(POST_FILE, 'utf8'));
  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error('POST.json must be a JSON object');
  }
  const url = (parsed as { url?: unknown }).url;
  if (typeof url !== 'string' || url.length === 0) {
    throw new Error('POST.json must carry a "url" string');
  }
  postUrl = url;
} catch (err) {
  console.error(`POST.json is not a usable post pointer: ${(err as Error).message}`);
  process.exit(1);
}

let postHost: string;
try {
  postHost = new URL(postUrl).host;
} catch {
  console.error(`POST.json url is not a valid URL: ${postUrl}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(POST_FILE, join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

console.log(`entry post: ${postUrl} (host: ${postHost})`);
