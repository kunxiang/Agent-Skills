# Common Mistakes in Skill Creation

## Mistake 1: "When to Use" in Body Instead of Description

### Wrong
```yaml
---
name: code-review
description: "Review code for quality"
---

# Code Review

## When to Use This Skill
Use this skill when you need to review pull requests...
```

### Correct
```yaml
---
name: code-review
description: "Review code for quality and security. Use when reviewing pull requests, checking code style, finding bugs, or ensuring best practices compliance."
---

# Code Review

## Quick Start
[Instructions start immediately]
```

**Why**: Claude reads descriptions at startup to decide when to activate skills. Body content isn't loaded until after activation.

## Mistake 2: SKILL.md Too Long

### Wrong
```markdown
# My Skill

[500+ lines of detailed documentation...]
```

### Correct
```markdown
# My Skill

## Quick Reference
[Essential info in ~50 lines]

## Core Instructions
[Main guidance in ~100 lines]

## Detailed Topics
- See [references/topic-a.md](references/topic-a.md)
- See [references/topic-b.md](references/topic-b.md)
```

**Why**: Long SKILL.md files consume excessive context. Use progressive disclosure.

## Mistake 3: Duplicated Content

### Wrong
```
skill/
├── SKILL.md          # Contains API reference
└── references/
    └── api.md        # Same API reference again
```

### Correct
```
skill/
├── SKILL.md          # "For API details, see references/api.md"
└── references/
    └── api.md        # Full API reference (only place)
```

**Why**: Duplication wastes tokens and creates maintenance burden.

## Mistake 4: Vague Description

### Wrong
```yaml
description: "Helps with coding"
description: "A useful skill"
description: "Does things with files"
```

### Correct
```yaml
description: "Generate unit tests for Python functions using pytest. Use when writing tests, improving coverage, or testing edge cases."
```

**Why**: Vague descriptions don't trigger correctly and waste Claude's decision-making.

## Mistake 5: Creating Auxiliary Documentation

### Wrong
```
skill/
├── SKILL.md
├── README.md           # Unnecessary
├── INSTALLATION.md     # Unnecessary
├── QUICK_REFERENCE.md  # Unnecessary
└── CHANGELOG.md        # Unnecessary
```

### Correct
```
skill/
├── SKILL.md            # Everything needed
└── references/
    └── detailed.md     # Only if truly needed
```

**Why**: Skills are self-contained. External docs add noise and confusion.

## Mistake 6: Deeply Nested References

### Wrong
```
SKILL.md → refs/a.md → refs/deep/b.md → refs/deep/deeper/c.md
```

### Correct
```
SKILL.md → refs/a.md
SKILL.md → refs/b.md
SKILL.md → refs/c.md
```

**Why**: Deep nesting makes navigation difficult and increases token usage.

## Mistake 7: Scripts as Documentation

### Wrong
```python
# scripts/process.py
"""
This script processes data...
[Long documentation that Claude reads into context]
"""
def process():
    ...
```

### Correct
```python
# scripts/process.py
"""Process data files."""
def process():
    ...
```

Document in references/, keep scripts minimal.

**Why**: Scripts should execute efficiently, not be documentation sources.

## Mistake 8: Missing Quick Reference

### Wrong
```markdown
# API Integration

For API documentation, see [references/api.md](references/api.md)
For examples, see [references/examples.md](references/examples.md)
For troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md)
```

### Correct
```markdown
# API Integration

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /users | GET | List users |
| /users | POST | Create user |

## Detailed Documentation
- [references/api.md](references/api.md)
```

**Why**: SKILL.md should provide immediate value without requiring reference files.

## Mistake 9: Over-Engineering

### Wrong
Creating a skill for something Claude already knows or that's too simple.

```yaml
name: hello-world
description: "Print hello world in various languages"
```

### When to Create a Skill
- Claude repeatedly needs specific domain knowledge
- Complex multi-step workflows
- Company-specific processes
- Tool integrations with custom logic

**Why**: Skills have overhead. Don't create them for trivial tasks.

## Mistake 10: Inconsistent Naming

### Wrong
```yaml
---
name: MySkill
---
```

Directory: `my_skill/` or `MySkill/`

### Correct
```yaml
---
name: my-skill
---
```

Directory: `my-skill/`

**Why**: Consistency enables reliable skill discovery and invocation.

## Mistake 11: No Tool Restrictions When Needed

### Wrong (for read-only skill)
```yaml
---
name: code-analyzer
description: "Analyze code without making changes"
# No allowed-tools restriction
---
```

### Correct
```yaml
---
name: code-analyzer
description: "Analyze code without making changes"
allowed-tools: Read, Grep, Glob
---
```

**Why**: Users expect read-only skills to not modify files.

## Mistake 12: Hardcoded Paths

### Wrong
```markdown
Run the script:
\`\`\`bash
/Users/john/projects/my-skill/scripts/process.py
\`\`\`
```

### Correct
```markdown
Run the script:
\`\`\`bash
./scripts/process.py
# or
python scripts/process.py
\`\`\`
```

**Why**: Skills are portable; hardcoded paths break on other systems.

## Mistake 13: Missing Error Handling in Scripts

### Wrong
```python
# scripts/process.py
data = json.load(open("input.json"))
# Crashes if file doesn't exist
```

### Correct
```python
# scripts/process.py
import sys
import json

try:
    with open("input.json") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: input.json not found", file=sys.stderr)
    sys.exit(1)
```

**Why**: Claude needs clear error messages to recover and help users.

## Mistake 14: Abstract Instructions

### Wrong
```markdown
## Guidelines
- Write good code
- Follow best practices
- Be thorough
```

### Correct
```markdown
## Guidelines
- Functions under 50 lines
- One assertion per test
- Use descriptive variable names (no single letters except i, j, k)
```

**Why**: Specific instructions produce consistent results.

## Mistake 15: Ignoring Progressive Disclosure

### Wrong
Loading everything at once regardless of need.

### Correct
```markdown
## Quick Start
[Immediate value - always loaded]

## If you need X
See [references/x.md](references/x.md)

## If you need Y
See [references/y.md](references/y.md)
```

**Why**: Progressive disclosure saves context and improves performance.
