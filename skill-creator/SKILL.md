---
name: skill-creator
description: "Create well-structured Claude Agent Skills following official specifications. Use when: (1) Creating a new skill from scratch, (2) Converting existing documentation/workflows into skills, (3) Refactoring or improving existing skills, (4) Learning skill development best practices. This skill guides you through the complete skill creation process including structure, frontmatter, progressive disclosure, and quality validation."
---

# Claude Agent Skill Creator

## Quick Reference

| Constraint | Requirement |
|------------|-------------|
| SKILL.md max lines | **< 500 lines** |
| Name format | lowercase, alphanumeric, hyphens only, max 64 chars |
| Description max | 1024 characters |
| Required frontmatter | `name`, `description` |

## Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required - Core instructions (< 500 lines)
├── references/           # Optional - Documentation loaded on-demand
│   ├── api-docs.md
│   └── examples.md
├── scripts/              # Optional - Executable code (not loaded into context)
│   └── helper.py
└── assets/               # Optional - Templates, images, boilerplate
    └── template.md
```

## Required Frontmatter

```yaml
---
name: skill-name
description: "What this skill does. Use when: (trigger conditions)"
---
```

**Critical**: The `description` is the PRIMARY triggering mechanism. Claude uses it to decide when to activate the skill. Include all "when to use" information here, NOT in the body.

## Optional Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `allowed-tools` | Restrict available tools | `Read, Grep, Glob` |
| `model` | Override model | `claude-sonnet-4-20250514` |
| `context` | Isolated execution | `fork` |
| `agent` | Agent type for fork | `Explore`, `Plan`, `general-purpose` |
| `user-invocable` | Show in slash menu | `false` |

## Creation Process

### Step 1: Gather Requirements
- Collect 3-5 concrete usage examples
- Identify what Claude doesn't already know
- Determine required tools and restrictions

### Step 2: Design Structure
- Outline main instructions for SKILL.md
- Plan references for detailed documentation
- Identify scripts for automation
- List assets for templates/boilerplate

### Step 3: Write SKILL.md

**Body Structure:**
```markdown
# Skill Title

## Quick Reference
[Essential lookup table]

## Core Instructions
[Step-by-step guidance - imperative form]

## Examples
[Concrete, minimal examples]

## References
- For [topic], see [file.md](references/file.md)
```

### Step 4: Validate

Use checklist from [references/validation-checklist.md](references/validation-checklist.md)

## Core Principles

### 1. Concise is Key
- Only add information Claude doesn't already have
- Prefer examples over verbose explanations
- Claude is already very smart - don't over-explain

### 2. Progressive Disclosure
- SKILL.md = Overview + Navigation (< 500 lines)
- References = Detailed docs (loaded on-demand)
- Scripts = Executable code (run, not loaded)
- Assets = Output templates (copied, not loaded)

### 3. Degrees of Freedom
| Level | Format | Use Case |
|-------|--------|----------|
| High | Text guidance | Multiple valid approaches |
| Medium | Pseudocode | Preferred pattern exists |
| Low | Exact scripts | Operations are fragile |

## Templates

- Basic skill: [assets/templates/basic-skill.md](assets/templates/basic-skill.md)
- Complex skill: [assets/templates/complex-skill.md](assets/templates/complex-skill.md)
- Frontmatter examples: [references/frontmatter-examples.md](references/frontmatter-examples.md)

## Detailed References

- **Full Specification**: [references/specification.md](references/specification.md)
- **Frontmatter Fields**: [references/frontmatter-examples.md](references/frontmatter-examples.md)
- **Design Patterns**: [references/design-patterns.md](references/design-patterns.md)
- **Validation Checklist**: [references/validation-checklist.md](references/validation-checklist.md)
- **Common Mistakes**: [references/common-mistakes.md](references/common-mistakes.md)

## Anti-Patterns to Avoid

1. **DO NOT** put "When to use" sections in the body (use description)
2. **DO NOT** exceed 500 lines in SKILL.md
3. **DO NOT** duplicate content between SKILL.md and references
4. **DO NOT** create README.md, CHANGELOG.md, or auxiliary docs
5. **DO NOT** deeply nest references (max 1 level from SKILL.md)
