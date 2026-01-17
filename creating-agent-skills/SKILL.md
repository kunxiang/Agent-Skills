---
name: creating-agent-skills
description: "**Meta-skill** for creating Claude Agent Skills. This is the foundational skill that produces other skills - use it to: (1) Create new skills from scratch, (2) Convert documentation/workflows into skills, (3) Refactor existing skills, (4) Learn skill development best practices. Guides through structure, frontmatter, progressive disclosure, and quality validation."
---

# Creating Agent Skills (Meta-Skill)

> **This is a meta-skill**: Unlike regular skills that perform specific tasks, this skill creates other skills. It serves as the foundational blueprint for all skill development in this repository.

## Quick Reference

| Constraint | Requirement |
|------------|-------------|
| SKILL.md max lines | **< 500 lines** |
| Name format | lowercase, alphanumeric, hyphens only, max 64 chars |
| Description max | 1024 characters |
| Required frontmatter | `name`, `description` |
| Description person | **Third person only** (not "I" or "You") |
| Reserved words | Cannot use "anthropic", "claude" in name |

## Core Concept: What Skills Actually Are

Skills are **prompt templates** that inject domain-specific instructions into conversation context. They are NOT executable code. When invoked:

1. **Conversation context modified**: Instructions injected as messages
2. **Execution context modified**: Tool permissions and model may change
3. **Selection via LLM reasoning**: Claude reads descriptions to decide which skill matches

## Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required - Core instructions (< 500 lines)
├── references/           # Text loaded into context via Read tool
│   └── detailed-docs.md
├── scripts/              # Executed via Bash, NOT loaded into context
│   └── helper.py
└── assets/               # Referenced by path, NOT loaded into context
    └── template.html
```

**Key distinction**:
- `references/` → Claude reads content into context (costs tokens)
- `scripts/` → Claude executes directly (efficient, no token cost)
- `assets/` → Claude references path only (no token cost)

## Required Frontmatter

```yaml
---
name: skill-name
description: "Processes X and generates Y. Use when user wants to Z or mentions keywords A, B, C."
---
```

**Critical Rules**:
1. Description is the **PRIMARY triggering mechanism**
2. Write in **third person**: "Processes files" not "I process files"
3. Include both **what it does** AND **when to use it**
4. Include **trigger keywords** users would naturally say

## Optional Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `allowed-tools` | Restrict tools | `Read, Grep, Glob` or `Bash(python:*)` |
| `model` | Override model | `claude-sonnet-4-20250514` |
| `context` | Isolated execution | `fork` |
| `agent` | Agent type for fork | `Explore`, `Plan`, `general-purpose` |
| `user-invocable` | Show in slash menu | `false` |
| `disable-model-invocation` | Prevent auto-invoke | `true` |

## Creation Process

### Step 1: Research Phase (Important!)

**Before creating a skill, thoroughly research the target domain**:

1. **Use WebSearch** (WebFetch often returns 403):
   - Official documentation and API references
   - Forum discussions and FAQs
   - Blog posts and experience sharing
   - GitHub/GitLab repositories and examples

2. **Language Strategy**:
   | Domain | Search Language |
   |--------|-----------------|
   | JTL-Shop, JTL-Wawi | **German** (Deutsch) |
   | SAP, DATEV | **German** |
   | Chinese platforms (Taobao, WeChat) | **Chinese** |
   | Other technologies | English |

3. **Search Examples**:
   ```
   # JTL-related - use German
   "JTL-Shop 5 NOVA Child Template erstellen Anleitung"
   "JTL-Wawi Plugin Entwicklung Dokumentation"

   # General tech - use English
   "React hooks best practices 2024"
   ```

4. **Organize Collected Content**:
   - Official resource links → Add to SKILL.md resource table
   - Code examples → Add to references/
   - Common errors → Add to troubleshooting table

### Step 2: Evaluation-Driven Development
1. Run Claude on representative tasks WITHOUT a skill
2. Document specific failures or missing context
3. Create 3+ test scenarios that expose these gaps
4. Only then write the skill to address actual gaps

### Step 3: Design Structure
- What goes in SKILL.md (< 500 lines)
- What goes in references/ (detailed docs)
- What goes in scripts/ (automation)
- What goes in assets/ (templates)

### Step 4: Write SKILL.md Body

**Recommended Structure**:
```markdown
# Skill Title

## Quick Start
[Minimal working example]

## Core Instructions
[Step-by-step - use imperative form: "Analyze", not "You should analyze"]

## Examples
[Input/output pairs]

## References
- For X details: [references/x.md](references/x.md)
```

### Step 5: Iterate with Claude
1. Test skill with Claude B (fresh instance)
2. Observe where it struggles
3. Refine with Claude A (your helper)
4. Repeat until reliable

## Core Principles

### 1. Concise is Key
Challenge each piece: "Does Claude really need this? Can I assume Claude knows this?"

**Good** (~50 tokens):
```markdown
Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad** (~150 tokens): "PDF files are a common format that contains text..."

### 2. Degrees of Freedom

| Level | When to Use | Format |
|-------|-------------|--------|
| **High** | Multiple valid approaches | Text guidance |
| **Medium** | Preferred pattern exists | Pseudocode with parameters |
| **Low** | Operations are fragile | Exact scripts, no modification |

### 3. Progressive Disclosure
- At startup: Only name + description loaded (~100 tokens)
- On activation: SKILL.md body loaded
- On demand: References loaded as needed

## Naming Conventions

**Recommended**: Gerund form (verb + -ing)
- `processing-pdfs`, `analyzing-spreadsheets`, `testing-code`

**Acceptable**: Noun phrases or action-oriented
- `pdf-processing`, `process-pdfs`

**Avoid**: `helper`, `utils`, `tools`, `data`

## Templates & References

- **Basic template**: [assets/templates/basic-skill.md](assets/templates/basic-skill.md)
- **Complex template**: [assets/templates/complex-skill.md](assets/templates/complex-skill.md)
- **Full specification**: [references/specification.md](references/specification.md)
- **Best practices**: [references/best-practices.md](references/best-practices.md)
- **Design patterns**: [references/design-patterns.md](references/design-patterns.md)
- **Validation checklist**: [references/validation-checklist.md](references/validation-checklist.md)
- **Common mistakes**: [references/common-mistakes.md](references/common-mistakes.md)

## Anti-Patterns

1. **DO NOT** put "When to use" in body (use description)
2. **DO NOT** exceed 500 lines in SKILL.md
3. **DO NOT** use first/second person in description
4. **DO NOT** nest references deeper than 1 level
5. **DO NOT** offer multiple tool options without a default
6. **DO NOT** include time-sensitive information
7. **DO NOT** use Windows-style paths (use forward slashes)
