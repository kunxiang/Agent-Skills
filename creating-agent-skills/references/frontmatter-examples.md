# Frontmatter Examples

## Minimal (Required Only)

```yaml
---
name: my-skill
description: "Brief description of what this skill does and when to use it"
---
```

## Read-Only Skill

```yaml
---
name: code-analyzer
description: "Analyze code quality, find patterns, and generate reports. Use when reviewing code, finding bugs, or understanding codebase structure."
allowed-tools: Read, Grep, Glob
---
```

## Tool-Restricted Skill

```yaml
---
name: python-data-analysis
description: "Analyze data using Python pandas and matplotlib. Use for data exploration, statistical analysis, and visualization."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(python:*)
  - Write
---
```

## Forked Context Skill

```yaml
---
name: deep-code-exploration
description: "Comprehensive codebase exploration and documentation. Use when you need thorough analysis of large codebases or complex architectures."
context: fork
agent: Explore
---
```

## Model Override Skill

```yaml
---
name: complex-reasoning
description: "Handle complex multi-step reasoning tasks requiring deep analysis."
model: claude-opus-4-20250514
---
```

## Internal-Only Skill (Not User-Invocable)

```yaml
---
name: internal-standards
description: "Apply internal coding standards when writing or reviewing code."
user-invocable: false
---
```

## Skill with Hooks

```yaml
---
name: secure-operations
description: "Perform file operations with security validation."
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "./scripts/security-check.sh $TOOL_INPUT"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
---
```

## Skill with Session Logging

```yaml
---
name: audit-logger
description: "Log all operations for audit compliance."
---

# Audit Logger

Log all operations to: `logs/${CLAUDE_SESSION_ID}.log`

Process arguments: $ARGUMENTS
```

## Complex Multi-Feature Skill

```yaml
---
name: enterprise-deployment
description: "Deploy applications to production with full validation, security checks, and rollback capabilities. Use when deploying to staging or production environments."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(docker:*)
  - Bash(kubectl:*)
  - Bash(git:*)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/pre-deploy-check.sh"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/log-operation.sh"
  Stop:
    - type: command
      command: "./scripts/deployment-summary.sh"
---
```

## Description Writing Examples

### Bad Descriptions

```yaml
# Too vague
description: "A tool for PDFs"

# No trigger conditions
description: "Helps with code"

# Too long, unfocused
description: "This is a comprehensive skill that can do many things including but not limited to processing files and generating reports and analyzing data..."
```

### Good Descriptions

```yaml
# Clear purpose + triggers
description: "Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction."

# Specific domain + use cases
description: "JTL-Shop 5 NOVA template customization. Use when creating Child-Templates, customizing SCSS/CSS, modifying Smarty templates, or building parametric product catalogs."

# Action-oriented + keywords
description: "Generate and validate API documentation from OpenAPI specs. Use for API docs, Swagger files, or REST endpoint documentation."
```

## Allowed-Tools Patterns

### Common Restrictions

```yaml
# Read-only (safest)
allowed-tools: Read, Grep, Glob

# Read + Python execution
allowed-tools: Read, Grep, Glob, Bash(python:*)

# Read + specific commands
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(npm test:*)
  - Bash(npm run lint:*)

# Full Bash but restricted Write
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write  # Use with caution

# No Bash at all
allowed-tools: Read, Write, Grep, Glob, Edit
```

### Tool Pattern Syntax

```yaml
# All python commands
Bash(python:*)

# Specific npm scripts
Bash(npm run build:*)
Bash(npm test:*)

# Git commands
Bash(git:*)

# Docker commands
Bash(docker:*)
Bash(docker-compose:*)
```
