---
name: itemise
description: Applies the Itemisation Protocol to code files. Numbers sections, functions, and meaningful blocks so every part of the code is referenceable by address. Creates backups before modifying anything, verifies integrity after, deletes backups on success. Type /itemise to run.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Context Guard — Itemisation Protocol (/itemise)

Applies hierarchical section numbering to code files so every block is referenceable by address (e.g. "check section 2.3.1"). Backs up files first, applies numbering, verifies nothing changed except the added comment numbers, then removes backups.

## Step 0: Check the Toggle

Read `CLAUDE.md` in the current project root. Look for a line that starts with `ITEMISATION:`.

- If it says `ITEMISATION: disabled` — stop here. Inform the user: "Itemisation Protocol is disabled. Change `ITEMISATION: disabled` to `ITEMISATION: enabled` in CLAUDE.md to activate it."
- If it says `ITEMISATION: enabled` or the setting is absent — proceed.

## Step 1: Confirm Scope

Ask the user:
> "Which files or directories should I itemise? I'll process all code files by default (`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.php`, `.java`, `.cs`, `.go`, `.rb`, `.sh`), excluding `node_modules/`, `vendor/`, `dist/`, `build/`, `.git/`. Or name specific files or folders."

Wait for their answer. Then list the exact files you will process and ask them to confirm before touching anything.

## Step 2: Check for Existing Itemisation

Before creating backups, scan each file for lines matching the pattern `// N.` or `# N.` (itemisation numbers). If any file already has itemisation numbers:

- Warn the user: "This file appears to already be itemised. Re-running will renumber everything from scratch."
- Ask if they want to continue or skip that file.

## Step 3: Create Backups

For each file to be processed, create a backup:

```bash
cp "{filename}" "{filename}.itemise-backup"
```

Report: "Backups created for N files."

## Step 4: Apply Itemisation

Process each file one at a time. Read the file, then rewrite it with the numbering applied. Use the correct comment syntax for the language:

| Language | Comment syntax |
|----------|---------------|
| JS, TS, JSX, TSX, PHP, Java, C#, Go | `// N. Description` |
| Python, Ruby, Shell, YAML | `# N. Description` |
| HTML, XML, Vue (template blocks) | `<!-- N. Description -->` |
| CSS, SCSS, Less | `/* N. Description */` |
| SQL | `-- N. Description` |

### The Numbering Rules

**Number these:**

- **Top-level sections** — logical groups of related code. Use a `SECTION:` label:
  ```
  // 1. SECTION: Authentication
  ...
  // end of 1
  ```
- **Functions and methods** — each significant function body:
  ```
  // 1.1 validateToken()
  function validateToken(request) { ... }
  // end of 1.1
  ```
- **Significant conditionals** — if/else or switch blocks with meaningful business logic (not trivial single-line guards):
  ```
  // 1.1.1 Return 401 if no auth header present
  if (!authHeader) { return error('no_auth') }
  ```
- **Important loops** — for/while/foreach with non-trivial bodies:
  ```
  // 1.2.1 Process each booking slot
  for (const slot of slots) { ... }
  ```
- **Key configuration objects** — important arrays or objects passed to significant calls:
  ```
  // 1.3.2 Localise script with AJAX URL, nonce, and slot config
  wp_localize_script('calendar-js', 'data', array( ... ));
  ```
- **Notable parameters within those** — only when the parameter itself is complex or calls a function:
  ```
  // 1.3.2.1 Slot config: array of {label, start_h, start_m, end_h, end_m} objects
  'slotConfig' => getSlotConfig(),
  ```

**Do NOT number these:**

- Individual variable declarations (`$count = 0;`, `let name = 'Alice';`)
- Single-line assignments
- Simple imports, requires, includes, use statements
- Closing braces or trivial boilerplate
- Lines that are already explained by their parent block's label

### Numbering Depth

- Aim for 3 levels of depth (`1.2.3`) in most cases
- Only go to 4 levels (`1.2.3.1`) for genuinely complex nested configuration
- If you find yourself writing `1.2.3.4.5`, the code probably needs refactoring, not more numbers
- Number within a block sequentially — if 1.2 contains three notable sub-items, they are 1.2.1, 1.2.2, 1.2.3

### End Markers

Add `// end of N` markers for:
- Every top-level section (`// end of 1`)
- Every named function/method (`// end of 1.1`)
- Every significant conditional or loop that spans more than a few lines (`// end of 1.1.2`)

Skip end markers on very short blocks (2–3 lines) where the closing brace makes the boundary obvious.

## Step 5: Verify Integrity

After rewriting each file, compare it to its backup to confirm that ONLY comment-number lines were added and NO actual code was changed.

Run this check for each file (adapt comment pattern to the language):

```bash
# Strip itemisation comment lines from the new file, then diff against backup
grep -Ev "^\s*(\/\/|#)\s+[0-9]+(\.[0-9]+)*(\s|\.)|^\s*(\/\/|#)\s+end of\s+[0-9]" "{filename}" > /tmp/itemise-check
diff /tmp/itemise-check "{filename}.itemise-backup"
```

- If `diff` produces no output: **PASS** — only comment lines were added
- If `diff` produces output: **FAIL** — actual code was changed

Report pass/fail for each file. On any FAIL, immediately restore the backup:

```bash
cp "{filename}.itemise-backup" "{filename}"
```

## Step 6: Clean Up

If ALL files passed:
- Delete all backup files: `rm "{filename}.itemise-backup"` for each
- Report: "Itemisation complete. N files updated. Backups deleted."

If any file failed:
- Restore its backup (already done in Step 5)
- Delete its backup after restoring
- Report which files were restored and what the diff showed
- Leave successfully-itemised files in place

## Step 7: Summary

```
## Itemisation Complete

### Updated Files
- [filename] — N sections, M functions numbered

### Failed / Restored
- [filename] — [reason, diff output]

### Notes
- Run /itemise again after significant code changes to renumber
- Disable with ITEMISATION: disabled in CLAUDE.md
```
