# Common Mistakes in Skill Creation

## Description Mistakes

### Mistake 1: Wrong Person in Description

**Wrong** (first/second person):
```yaml
description: "I can help you process PDF files"
description: "You can use this to analyze spreadsheets"
```

**Correct** (third person):
```yaml
description: "Processes PDF files and extracts text. Use when working with PDF documents or when user mentions PDFs."
```

**Why**: The description is injected into the system prompt. Inconsistent point-of-view causes discovery problems.

### Mistake 2: "When to Use" in Body Instead of Description

**Wrong**:
```yaml
---
name: code-review
description: "Review code for quality"
---

# Code Review

## When to Use This Skill
Use this skill when you need to review pull requests...
```

**Correct**:
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

### Mistake 3: Vague Description

**Wrong**:
```yaml
description: "Helps with coding"
description: "A useful skill"
description: "Does things with files"
```

**Correct**:
```yaml
description: "Generate unit tests for Python functions using pytest. Use when writing tests, improving coverage, or testing edge cases."
```

**Why**: Vague descriptions don't trigger correctly and waste Claude's decision-making.

## Structure Mistakes

### Mistake 4: SKILL.md Too Long

**Wrong**:
```markdown
# My Skill

[500+ lines of detailed documentation...]
```

**Correct**:
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

### Mistake 5: Duplicated Content

**Wrong**:
```
skill/
├── SKILL.md          # Contains API reference
└── references/
    └── api.md        # Same API reference again
```

**Correct**:
```
skill/
├── SKILL.md          # "For API details, see references/api.md"
└── references/
    └── api.md        # Full API reference (only place)
```

**Why**: Duplication wastes tokens and creates maintenance burden.

### Mistake 6: Creating Auxiliary Documentation

**Wrong**:
```
skill/
├── SKILL.md
├── README.md           # Unnecessary
├── INSTALLATION.md     # Unnecessary
├── QUICK_REFERENCE.md  # Unnecessary
└── CHANGELOG.md        # Unnecessary
```

**Correct**:
```
skill/
├── SKILL.md            # Everything needed
└── references/
    └── detailed.md     # Only if truly needed
```

**Why**: Skills are self-contained. External docs add noise and confusion.

### Mistake 7: Deeply Nested References

**Wrong**:
```
SKILL.md → refs/a.md → refs/deep/b.md → refs/deep/deeper/c.md
```

**Correct**:
```
SKILL.md → refs/a.md
SKILL.md → refs/b.md
SKILL.md → refs/c.md
```

**Why**: Deep nesting makes navigation difficult. Claude may partially read nested files.

## Naming Mistakes

### Mistake 8: Inconsistent Naming

**Wrong**:
```yaml
---
name: MySkill
---
```
Directory: `my_skill/` or `MySkill/`

**Correct**:
```yaml
---
name: my-skill
---
```
Directory: `my-skill/`

**Why**: Consistency enables reliable skill discovery and invocation.

### Mistake 9: Vague or Reserved Names

**Wrong**:
```yaml
name: helper
name: utils
name: tools
name: claude-assistant
name: anthropic-helper
```

**Correct**:
```yaml
name: pdf-processing
name: code-analysis
name: data-visualization
```

**Why**: Vague names don't indicate purpose. Reserved words ("claude", "anthropic") are not allowed.

## Content Mistakes

### Mistake 10: Over-Explaining What Claude Knows

**Wrong** (~150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well...
```

**Correct** (~50 tokens):
```markdown
## Extract PDF text

Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Why**: Claude already knows what PDFs are. Only add what Claude doesn't know.

### Mistake 11: Multiple Options Without Default

**Wrong**:
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or...
```

**Correct**:
```markdown
Use pdfplumber for text extraction:
import pdfplumber

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

**Why**: Too many choices confuse Claude. Provide a default with escape hatch.

### Mistake 12: Time-Sensitive Information

**Wrong**:
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Correct**:
```markdown
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

**Why**: Time-sensitive content becomes wrong. Use "current" vs "old patterns" structure.

### Mistake 13: Inconsistent Terminology

**Wrong**:
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

**Correct**:
- Always "API endpoint"
- Always "field"
- Always "extract"

**Why**: Consistency helps Claude understand and follow instructions.

### Mistake 14: Abstract Instructions

**Wrong**:
```markdown
## Guidelines
- Write good code
- Follow best practices
- Be thorough
```

**Correct**:
```markdown
## Guidelines
- Functions under 50 lines
- One assertion per test
- Use descriptive variable names (no single letters except i, j, k)
```

**Why**: Specific instructions produce consistent results.

## Tool & Script Mistakes

### Mistake 15: No Tool Restrictions When Needed

**Wrong** (for read-only skill):
```yaml
---
name: code-analyzer
description: "Analyze code without making changes"
# No allowed-tools restriction
---
```

**Correct**:
```yaml
---
name: code-analyzer
description: "Analyze code without making changes"
allowed-tools: Read, Grep, Glob
---
```

**Why**: Users expect read-only skills to not modify files.

### Mistake 16: Hardcoded Paths

**Wrong**:
```markdown
Run the script:
/Users/john/projects/my-skill/scripts/process.py
```

**Correct**:
```markdown
Run the script:
python {baseDir}/scripts/process.py
# or
python scripts/process.py
```

**Why**: Skills are portable; hardcoded paths break on other systems.

### Mistake 17: Windows-Style Paths

**Wrong**:
```markdown
scripts\helper.py
reference\guide.md
```

**Correct**:
```markdown
scripts/helper.py
reference/guide.md
```

**Why**: Unix-style paths work across all platforms. Windows-style paths fail on Unix.

### Mistake 18: Scripts That Punt Errors to Claude

**Wrong**:
```python
def process_file(path):
    return open(path).read()  # Crashes if file doesn't exist
```

**Correct**:
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
```

**Why**: Claude needs clear error messages to recover and help users.

### Mistake 19: Unexplained Magic Numbers

**Wrong**:
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

**Correct**:
```python
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

**Why**: Unexplained constants ("voodoo constants") create maintenance burden.

### Mistake 20: Scripts as Documentation

**Wrong**:
```python
# scripts/process.py
"""
This script processes data...
[Long documentation that Claude reads into context]
"""
def process():
    ...
```

**Correct**:
```python
# scripts/process.py
"""Process data files."""
def process():
    ...
```

Document in `references/`, keep scripts minimal.

**Why**: Scripts should execute efficiently, not be documentation sources.

## Workflow Mistakes

### Mistake 21: Missing Quick Reference

**Wrong**:
```markdown
# API Integration

For API documentation, see [references/api.md](references/api.md)
For examples, see [references/examples.md](references/examples.md)
```

**Correct**:
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

### Mistake 22: Missing Validation Steps

**Wrong**:
```markdown
## Process
1. Make changes
2. Save file
3. Done
```

**Correct**:
```markdown
## Process
1. Make changes
2. **Validate**: `python scripts/validate.py output.txt`
3. If validation fails, fix and validate again
4. Only proceed when validation passes
5. Save file
```

**Why**: Validation catches errors early before they propagate.

### Mistake 23: Over-Engineering

Creating a skill for something Claude already knows or that's too simple.

**Wrong**:
```yaml
name: hello-world
description: "Print hello world in various languages"
```

**When to create a skill**:
- Claude repeatedly needs specific domain knowledge
- Complex multi-step workflows
- Company-specific processes
- Tool integrations with custom logic

**Why**: Skills have overhead. Don't create them for trivial tasks.

## MCP Tool Mistakes

### Mistake 24: Missing Server Prefix for MCP Tools

**Wrong**:
```markdown
Use the bigquery_schema tool to retrieve schemas.
```

**Correct**:
```markdown
Use the BigQuery:bigquery_schema tool to retrieve schemas.
```

**Why**: Without server prefix, Claude may fail to locate the tool when multiple MCP servers are available.

## Validation Quick Commands

```bash
# Check SKILL.md line count
wc -l SKILL.md  # Should be < 500

# Validate YAML frontmatter
head -50 SKILL.md | grep -A 20 "^---"

# Check directory structure
find . -type f -name "*.md" | head -20

# Verify no auxiliary docs
ls -la | grep -E "(README|CHANGELOG|INSTALLATION)"
# Should return nothing

# Check for Windows paths
grep -r '\\' *.md  # Should return nothing
```
