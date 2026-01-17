# Claude Agent Skills Complete Specification

## What Skills Actually Are

Skills are **prompt-based conversation and execution context modifiers** that work through a meta-tool architecture. They are NOT executable code.

**Key insight**: Skills = Prompt Template + Conversation Context Injection + Execution Context Modification + Optional bundled files

When a skill is invoked:
1. **Conversation context modified**: Instructions injected as user messages (with `isMeta: true` to hide from UI)
2. **Execution context modified**: Tool permissions changed, model may be overridden
3. **Selection via LLM reasoning**: Claude reads descriptions to match user intent (no algorithmic matching)

## Internal Architecture

### The Skill Meta-Tool

The `Skill` tool (capital S) is a meta-tool that manages all individual skills. It appears in Claude's `tools` array alongside Read, Write, Bash, etc.

```
Traditional Tools vs Skills:
┌─────────────────────────────────────────────────────────┐
│ Aspect          │ Traditional Tools │ Skills            │
├─────────────────────────────────────────────────────────┤
│ Execution       │ Synchronous       │ Prompt expansion  │
│ Purpose         │ Perform actions   │ Guide workflows   │
│ Return          │ Immediate results │ Context changes   │
│ Token overhead  │ Minimal (~100)    │ Significant (1500+)│
└─────────────────────────────────────────────────────────┘
```

### Message Injection

When a skill executes, TWO user messages are injected:

1. **Metadata message** (`isMeta: false` - visible to user):
```xml
<command-message>The "pdf" skill is loading</command-message>
<command-name>pdf</command-name>
```

2. **Skill prompt message** (`isMeta: true` - hidden from UI):
```markdown
You are a PDF processing specialist...
[Full SKILL.md content]
Base directory: /path/to/skill
```

This dual-message design solves transparency vs. clarity: users see what's happening without being overwhelmed by implementation details.

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
├── references/           # Text loaded into context (costs tokens)
│   ├── api-docs.md       # Claude reads via Read tool
│   └── examples.md
├── scripts/              # Executed, NOT loaded (efficient)
│   ├── helper.py         # Run directly via Bash
│   └── validate.sh
└── assets/               # Referenced by path only (no token cost)
    ├── template.md       # Copied to output
    └── boilerplate/
```

**Critical distinction**:
- `references/`: Text content → loaded into context → consumes tokens
- `scripts/`: Executable code → run directly → no context tokens
- `assets/`: Static files → path reference only → no context tokens

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
disable-model-invocation: false  # Prevent auto-invocation
hooks:                        # Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
---
```

### Body (Markdown)

The body contains instructions Claude follows when the skill is active.

**Recommended structure**:
1. **Quick Start** - Minimal working example
2. **Core Instructions** - Step-by-step guidance (imperative form)
3. **Examples** - Concrete input/output pairs
4. **References** - Links to detailed documentation

## Frontmatter Field Details

### name (required)
- Format: lowercase, alphanumeric, hyphens only
- Max length: 64 characters
- Cannot contain: XML tags, "anthropic", "claude"
- Should match directory name

**Naming conventions**:
- Recommended: Gerund form (`processing-pdfs`, `analyzing-data`)
- Acceptable: Noun phrases (`pdf-processing`) or actions (`process-pdfs`)
- Avoid: Vague names (`helper`, `utils`, `tools`)

### description (required)
- Max length: 1024 characters
- **PRIMARY triggering mechanism** - Claude uses this to decide activation
- **Must be third person**: "Processes files" not "I process files"

**Must include**:
- What the skill does
- When to use it (trigger conditions)
- Keywords users would naturally say

**Good example**:
```yaml
description: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
```

**Bad examples**:
```yaml
description: "Helps with documents"  # Too vague
description: "I can process PDFs"    # Wrong person
description: "You can use this for PDFs"  # Wrong person
```

### allowed-tools (optional)
Restricts which tools Claude can use when skill is active.

```yaml
# String format
allowed-tools: Read, Grep, Glob

# List format
allowed-tools:
  - Read
  - Grep
  - Bash(python:*)
  - Bash(git status:*)
```

**Tool pattern syntax**:
- `Bash(python:*)` - Only python commands
- `Bash(npm run build:*)` - Specific npm scripts
- `Bash(git:*)` - All git commands

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
agent: Explore  # Agent type: Explore, Plan, general-purpose
```

### disable-model-invocation (optional)
When `true`, prevents Claude from automatically invoking the skill. Can only be invoked manually via `/skill-name`.

```yaml
disable-model-invocation: true
```

Use for: dangerous operations, configuration commands, interactive workflows requiring explicit user control.

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
          command: "./scripts/format.sh"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
```

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Arguments passed when invoking the skill |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `{baseDir}` | Skill's installation directory |

## Progressive Disclosure Architecture

Three-level loading system:

### Level 1: Metadata (Always Loaded at Startup)
- Name and description only (~100 tokens)
- Used for skill matching/triggering
- Token budget limit: 15,000 characters by default

### Level 2: SKILL.md Body (On Activation)
- Full instructions (< 500 lines / ~5000 words)
- User sees confirmation prompt before loading

### Level 3: Bundled Resources (On Demand)
- References loaded when Claude needs them
- Scripts executed without loading content
- Assets referenced by path

## Execution Lifecycle

### Phase 1: Discovery (Startup)
```
Claude Code scans:
├── ~/.claude/skills/          # Personal
├── .claude/skills/            # Project
├── Plugin skills directories  # Plugins
└── Built-in skills           # System
```

### Phase 2: Turn 1 - User Request & Skill Selection
1. User sends request
2. Claude receives message + tools array (including Skill meta-tool)
3. Claude reads `<available_skills>` in Skill tool description
4. Claude reasons about which skill matches (pure LLM reasoning, no algorithmic matching)
5. Claude returns tool_use with `name: "Skill"` and `input: { command: "skill-name" }`

### Phase 3: Skill Tool Execution
1. **Validation**: Check skill exists, is enabled, type is "prompt"
2. **Permission check**: Check allow/deny rules, ask user if needed
3. **Load skill file**: Parse SKILL.md, extract frontmatter and body
4. **Generate messages**: Metadata message + skill prompt message
5. **Apply context modifier**: Set tool permissions, override model if specified
6. **Yield result**: Return messages and context modifier

### Phase 4: Subsequent Turns
- Claude follows skill instructions with modified context
- Pre-approved tools work without user prompts
- References loaded as needed via Read tool
- Scripts executed as needed via Bash tool

## Security Considerations

1. **Trust sources**: Only install skills from trusted sources
2. **Audit code**: Review all scripts before enabling
3. **Limit tools**: Use `allowed-tools` to restrict capabilities
4. **Version control**: Track skill changes in git
5. **No secrets**: Never store credentials in skills

## MCP Tool References

If your skill uses MCP tools, use fully qualified names:

```markdown
Use the BigQuery:bigquery_schema tool to retrieve schemas.
Use the GitHub:create_issue tool to create issues.
```

Format: `ServerName:tool_name`
