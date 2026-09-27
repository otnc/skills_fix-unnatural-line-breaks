#!/usr/bin/env node
// Runs the skill's own lint.mjs over every file in this repository that holds prose or comments: docs, the README base file, the skill's references and scripts, the tests, and the workflow files.
// The file list is built here rather than with shell globs so `npm run lint:self` behaves the same on Windows (cmd does not expand globs) and in CI.
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const skill = join(root, "skills", "fix-unnatural-line-breaks");
const inDir = (dir, ext) => (existsSync(dir) ? readdirSync(dir).filter((f) => f.endsWith(ext)).map((f) => join(dir, f)) : []);

const files = [
  ...["README.md", "README.ja.md", "CHANGELOG.md"].map((f) => join(root, f)).filter(existsSync),
  ...inDir(join(root, "base"), ".md"),
  join(skill, "SKILL.md"),
  ...inDir(join(skill, "references"), ".md"),
  ...inDir(join(skill, "scripts"), ".mjs"),
  ...inDir(join(root, "scripts"), ".mjs"),
  ...inDir(join(root, "tests"), ".mjs"),
  ...inDir(join(root, ".github", "workflows"), ".yml"),
].map((f) => relative(root, f));

execFileSync(process.execPath, [join(skill, "scripts", "lint.mjs"), ...files], { cwd: root, stdio: "inherit" });
