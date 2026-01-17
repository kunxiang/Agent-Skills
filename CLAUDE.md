# CLAUDE.md - AI Assistant Guidelines

This document provides context for AI assistants working with this repository.

## Repository Overview

This is a **Claude Agent Skills** collection repository containing reusable skills for AI-assisted development workflows. Skills are prompt templates that inject domain-specific instructions into conversation context.

**Primary Language**: Chinese (README), German (JTL-related skills), English (documentation)

## Directory Structure

```
Agent-Skills/
├── CLAUDE.md                           # This file - AI assistant guidelines
├── README.md                           # Repository documentation (Chinese)
├── best-practices.md                   # Official Anthropic skill authoring guide
├── .gitignore                          # Excludes *.zip files
│
├── skill-creator/                      # Meta-skill for creating new skills
│   ├── SKILL.md                        # Main skill definition
│   ├── references/                     # Detailed documentation
│   │   ├── specification.md
│   │   ├── best-practices.md
│   │   ├── design-patterns.md
│   │   ├── validation-checklist.md
│   │   ├── common-mistakes.md
│   │   └── frontmatter-examples.md
│   └── assets/templates/               # Skill templates
│       ├── basic-skill.md
│       └── complex-skill.md
│
├── creating-jtl-shop-5-plugins/        # JTL-Shop 5 plugin development (German)
│   ├── SKILL.md
│   ├── references/
│   │   ├── info-xml.md
│   │   ├── bootstrap-hooks.md
│   │   ├── plugin-architecture.md
│   │   └── troubleshooting.md
│   └── assets/templates/
│       ├── info.xml
│       └── Bootstrap.php
│
└── creating-jtl-shop-nova-template/    # JTL-Shop NOVA template development (German)
    ├── SKILL.md
    ├── references/
    │   ├── scss-variables.md
    │   ├── smarty-blocks.md
    │   ├── parametric-catalog.md
    │   ├── parametric-catalog-js.md
    │   └── parametric-catalog-styles.md
    └── assets/
        ├── Bootstrap.php
        ├── js/parametric-catalog.js
        ├── templates/productlist/
        └── themes/_parametric-catalog.scss
```

## Available Skills

| Skill | Invocation | Purpose |
|-------|------------|---------|
| `skill-creator` | `/skill-creator` | Create new Claude Agent Skills following specifications |
| `creating-jtl-shop-5-plugins` | `/creating-jtl-shop-5-plugins` | JTL-Shop 5 plugin development |
| `creating-jtl-shop-nova-template` | `/creating-jtl-shop-nova-template` | JTL-Shop 5 NOVA child template development |

## Skill File Structure Convention

Every skill follows this structure:

```
skill-name/
├── SKILL.md              # REQUIRED: Core instructions (< 500 lines)
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

## SKILL.md Frontmatter Requirements

| Field | Requirement |
|-------|-------------|
| `name` | Required. Max 64 chars, lowercase + numbers + hyphens only |
| `description` | Required. Max 1024 chars, third person, includes triggers |
| Reserved words | Cannot use "anthropic" or "claude" in name |

**Example**:
```yaml
---
name: my-skill-name
description: "Processes X and generates Y. Use when user wants to Z or mentions keywords A, B, C."
---
```

## Development Workflow

### Creating a New Skill

1. Use the `skill-creator` skill: `/skill-creator`
2. Follow the skill structure conventions
3. Keep SKILL.md under 500 lines
4. Use progressive disclosure (reference files for details)
5. Test with representative tasks

### Modifying Existing Skills

1. Read the existing SKILL.md first
2. Understand the references structure
3. Keep changes focused and minimal
4. Maintain the file structure conventions
5. Test changes with real scenarios

## Code Conventions

### File Paths
- Always use forward slashes (`/`) even on Windows
- Use relative paths in references: `[references/detail.md](references/detail.md)`

### Frontmatter Descriptions
- Write in **third person**: "Processes files" not "I process files"
- Include both what it does AND when to use it
- Include trigger keywords users would naturally say

### Token Efficiency
- Challenge each piece: "Does Claude really need this?"
- Assume Claude knows common concepts
- Keep SKILL.md body under 500 lines
- Split detailed content into reference files

## Common Tasks

### Installing a Skill
```bash
# Copy to personal directory (recommended)
cp -r <skill-name>/ ~/.claude/skills/

# Or copy to project directory
cp -r <skill-name>/ .claude/skills/

# Or symlink
ln -s /path/to/Agent-Skills/<skill-name> ~/.claude/skills/<skill-name>
```

### Testing a Skill
1. Install the skill
2. Invoke with `/skill-name`
3. Verify it handles representative tasks
4. Check token usage is reasonable

## JTL-Specific Notes

For JTL-Shop related skills:

- **Language**: Documentation and code comments are in **German**
- **Search queries**: Use German when searching for JTL documentation
- **Official resources**:
  - Dev Guide: https://jtl-devguide.readthedocs.io/
  - Forum: https://forum.jtl-software.de/
  - NOVAChild: https://build.jtl-shop.de/get/template/NOVAChild-master.zip

## Anti-Patterns to Avoid

1. **DO NOT** exceed 500 lines in SKILL.md
2. **DO NOT** use first/second person in descriptions
3. **DO NOT** nest references deeper than 1 level from SKILL.md
4. **DO NOT** offer multiple tool options without a default
5. **DO NOT** include time-sensitive information
6. **DO NOT** use Windows-style paths
7. **DO NOT** assume packages are installed without checking

## Git Workflow

- Main branch for stable releases
- Feature branches for development
- Commit messages should be clear and descriptive
- ZIP files are ignored (see .gitignore)

## References

- **Anthropic Best Practices**: See `best-practices.md` in repository root
- **Skill Specification**: See `skill-creator/references/specification.md`
- **Design Patterns**: See `skill-creator/references/design-patterns.md`
- **Common Mistakes**: See `skill-creator/references/common-mistakes.md`
