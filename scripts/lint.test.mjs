// Black-box tests for lint.mjs: write a temp file, run the CLI against it,
// and check what it reports. Testing through the CLI (rather than importing
// internals) keeps this in sync with what `node scripts/lint.mjs <file>`
// actually does for a user.
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "lint.mjs");

function runLint(content, filename) {
  const dir = mkdtempSync(join(tmpdir(), "lint-test-"));
  const file = join(dir, filename);
  writeFileSync(file, content, "utf-8");
  try {
    return execFileSync("node", [SCRIPT, "--json", file], {
      encoding: "utf-8",
    });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function findingsFor(content, filename) {
  return JSON.parse(runLint(content, filename));
}

test("flags a Japanese sentence wrapped mid-way at a particle", () => {
  const content =
    "石炭をば早や積み果てつ。中等室の卓のほとりはいと静かにて、\n" +
    "熾熱灯の光の晴れがましきも徒なり。\n";
  const findings = findingsFor(content, "sample.md");
  assert.equal(findings.length, 1);
  assert.equal(findings[0].line, 1);
});

test("flags an English sentence wrapped mid-way with no terminal punctuation", () => {
  const content =
    "It is a truth universally acknowledged, that a single\n" +
    "man in possession of a good fortune, must be in want of a wife.\n";
  const findings = findingsFor(content, "sample.md");
  assert.equal(findings.length, 1);
  assert.equal(findings[0].line, 1);
});

test("does not flag a properly joined paragraph", () => {
  const content =
    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.\n";
  assert.deepEqual(findingsFor(content, "sample.md"), []);
});

test("does not flag list items, headings, or blank-line paragraph boundaries", () => {
  const content =
    "# A heading\n" +
    "\n" +
    "- first item\n" +
    "- second item\n" +
    "\n" +
    "A short paragraph that ends cleanly.\n";
  assert.deepEqual(findingsFor(content, "sample.md"), []);
});

test("does not flag content inside a fenced code block", () => {
  const content = "```\nfoo bar of\nbaz\n```\n";
  assert.deepEqual(findingsFor(content, "sample.md"), []);
});

test("does not flag a Markdown table row", () => {
  const content = "| a | b of |\n| - | - |\n";
  assert.deepEqual(findingsFor(content, "sample.md"), []);
});

test("does not flag YAML key: value lines in a .yml file", () => {
  const content = "name: example\ndescription: a wrapped value continuing\n";
  assert.deepEqual(findingsFor(content, "sample.yml"), []);
});

test("does not flag YAML frontmatter in a Markdown file", () => {
  const content =
    "---\n" + "title: a value that looks wrapped\n" + "---\n" + "Body text.\n";
  assert.deepEqual(findingsFor(content, "sample.md"), []);
});

test("only compares comment lines in non-Markdown source files, never code", () => {
  const content =
    "// This comment sentence is split across two lines and\n" +
    "// continues here.\n" +
    "const of = 1;\n" +
    "const bar = of +\n" +
    "  2;\n";
  const findings = findingsFor(content, "sample.ts");
  assert.equal(findings.length, 1);
  assert.equal(findings[0].line, 1);
});

test("prints a plain-text summary when no issues are found", () => {
  const dir = mkdtempSync(join(tmpdir(), "lint-test-"));
  const file = join(dir, "clean.md");
  writeFileSync(file, "A single clean paragraph.\n", "utf-8");
  try {
    const output = execFileSync("node", [SCRIPT, file], {
      encoding: "utf-8",
    });
    assert.match(output, /No suspicious line breaks found\./);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
