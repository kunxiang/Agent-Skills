# Claude Agent Skills Complete Specification

## Overview

Agent Skills are modular, self-contained packages that extend Claude's capabilities. They consist of:

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Storage Locations

| Type | Path | Scope | Priority |
|------|------|-------|----------|
| Managed | Admin deployment | Organization-wide | Highest |
| Personal | `~/.claude/skills/` | All your projects | High |
| Project | `.claude/skills/` | Repository team | Medium |
| Plugin | `skills/` in plugin | Plugin users | Low |
| Nested | `packages/frontend/.claude/skills/` | Monorepo packages | Low |

## Directory Structure

```
skill-name/
├── SKILL.md              # Required - Core instructions
├── references/           # Optional - Documentation
│   ├── api-docs.md       # Loaded into context when needed
│   └── examples.md       # Reference material
├── scripts/              # Optional - Executable code
│   ├── helper.py         # Run directly, not loaded into context
│   └── validate.sh       # Automation scripts
└── assets/               # Optional - Output resources
    ├── template.md       # Copied to output, not loaded
    └── boilerplate/      # Starter files
```

## SKILL.md Anatomy

### Frontmatter (YAML)

```yaml
---
# Required Fields
name: skill-name              # lowercase, alphanumeric, hyphens; max 64 chars
description: "Description"    # max 1024 chars; PRIMARY trigger mechanism

# Optional Fields
allowed-tools: Read, Grep     # Tool restrictions (string or list)
model: claude-sonnet-4-20250514  # Model override
context: fork                 # Isolated execution
agent: Explore                # Agent type when forked
user-invocable: true          # Show in slash menu (default: true)
hooks:                        # Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
---
```

### Body (Markdown)

The body contains instructions Claude follows when the skill is active. Structure recommendations:

1. **Quick Reference** - Essential lookup tables
2. **Core Instructions** - Step-by-step guidance
3. **Examples** - Concrete, minimal examples
4. **References** - Links to detailed documentation

## Frontmatter Field Details

### name (required)
- Format: lowercase, alphanumeric, hyphens only
- Max length: 64 characters
- Should match directory name
- Examples: `pdf-processor`, `code-review`, `data-analysis`

### description (required)
- Max length: 1024 characters
- PRIMARY triggering mechanism - Claude uses this to decide activation
- Include:
  - What the skill does
  - When to use it (trigger conditions)
  - Keywords users would naturally say
- Bad: "A tool for PDFs"
- Good: "Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction."

### allowed-tools (optional)
Restricts which tools Claude can use when skill is active.

```yaml
# String format
allowed-tools: Read, Grep, Glob

# List format
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(python:*)

# Tool patterns
allowed-tools: Bash(npm:*)    # Only npm commands
allowed-tools: Bash(python:*) # Only python commands
```

When omitted, no restrictions apply.

### model (optional)
Override the model used when skill is active.

```yaml
model: claude-sonnet-4-20250514
model: claude-opus-4-20250514
```

### context (optional)
Set to `fork` to run in isolated sub-agent context.

```yaml
context: fork
agent: Explore  # Agent type: Explore, Plan, general-purpose, or custom
```

Benefits:
- Separate conversation history
- Doesn't clutter main conversation
- Good for complex multi-step operations

### user-invocable (optional)
Controls visibility in slash command menu.

| Setting | Slash Menu | Auto-discovery | Use Case |
|---------|-----------|----------------|----------|
| `true` (default) | Visible | Yes | User-invoked skills |
| `false` | Hidden | Yes | Model-invoked only |

### hooks (optional)
Define lifecycle hooks scoped to skill execution.

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh $TOOL_INPUT"
          once: true  # Run only once per session
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "./scripts/format.sh $OUTPUT_FILE"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
```

## String Substitutions

Available variables in skill content:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Arguments passed when invoking the skill |
| `${CLAUDE_SESSION_ID}` | Current session ID |

Example:
```markdown
Log activity to: logs/${CLAUDE_SESSION_ID}.log
Process these files: $ARGUMENTS
```

## Progressive Disclosure Architecture

Three-level loading system:

### Level 1: Metadata (Always Loaded)
- Name and description only (~100 tokens)
- Loaded at startup for all installed skills
- Used for skill matching/triggering

### Level 2: SKILL.md Body (On Activation)
- Full instructions (<5000 words / <500 lines)
- Loaded when user request matches skill description
- User sees confirmation prompt before loading

### Level 3: Bundled Resources (On Demand)
- References, scripts, assets (unlimited size)
- Loaded only when Claude needs them
- Scripts may execute without loading content

## Resource Types

### references/
- **Purpose**: Documentation loaded into context
- **When loaded**: When Claude needs the information
- **Examples**: API docs, schemas, policies, detailed guides
- **Best practice**: Keep SKILL.md lean; detailed info goes here

### scripts/
- **Purpose**: Executable code
- **When loaded**: Never - executed directly
- **Token efficiency**: High (runs without context consumption)
- **Examples**: Validation scripts, automation helpers, data processors

### assets/
- **Purpose**: Files for output, not context
- **When loaded**: Never - copied to output
- **Examples**: Templates, boilerplate, images, icons

## Skill Lifecycle

### Discovery (Startup)
1. Claude scans skill locations
2. Loads only names and descriptions
3. Creates mental index for matching

### Activation (On Request)
1. User makes request
2. Claude matches request to skill descriptions
3. User confirms skill activation
4. Full SKILL.md loads into context

### Execution (During Task)
1. Claude follows skill instructions
2. Loads references as needed
3. Executes scripts as needed
4. Copies assets as needed

### Completion
1. Hooks cleanup (if defined)
2. Skill deactivates
3. Context returns to normal

## Distribution Methods

### Project Skills
```
my-repo/
└── .claude/skills/
    └── my-skill/
        └── SKILL.md
```
Commit to version control; team gets skills with repo.

### Personal Skills
```
~/.claude/skills/
└── my-skill/
    └── SKILL.md
```
Available across all your projects.

### Plugin Skills
```
my-plugin/
└── skills/
    └── my-skill/
        └── SKILL.md
```
Distributed via plugin marketplace.

## Security Considerations

1. **Trust sources**: Only install skills from trusted sources
2. **Audit code**: Review all scripts before enabling
3. **Limit tools**: Use `allowed-tools` to restrict capabilities
4. **Version control**: Track skill changes in git
5. **No secrets**: Never store credentials in skills
