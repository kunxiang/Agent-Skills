# Skill Authoring Best Practices

Based on official Anthropic documentation and community experience.

## Core Principles

### 1. Concise is Key

The context window is a shared resource. Your skill competes with:
- System prompt
- Conversation history
- Other skills' metadata
- User's actual request

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have.

**Challenge each piece**:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good** (~50 tokens):
```markdown
## Extract PDF text

Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad** (~150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...
```

### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility and variability.

**High freedom** (text-based instructions):
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

```markdown
## Code review process
1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability
4. Verify adherence to project conventions
```

**Medium freedom** (pseudocode/parameterized scripts):
- Preferred pattern exists
- Some variation acceptable
- Configuration affects behavior

```markdown
## Generate report
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```

**Low freedom** (exact scripts, no modification):
- Operations are fragile and error-prone
- Consistency is critical
- Specific sequence must be followed

```markdown
## Database migration
Run exactly this script:
python scripts/migrate.py --verify --backup

Do not modify the command or add additional flags.
```

**Analogy**: Think of Claude as a robot exploring a path:
- **Narrow bridge with cliffs**: Only one safe way forward → exact instructions (low freedom)
- **Open field with no hazards**: Many paths lead to success → general direction (high freedom)

### 3. Test with All Models You Plan to Use

Skills act as additions to models, so effectiveness depends on the underlying model.

| Model | Consideration |
|-------|---------------|
| **Claude Haiku** | Does the skill provide enough guidance? |
| **Claude Sonnet** | Is the skill clear and efficient? |
| **Claude Opus** | Does the skill avoid over-explaining? |

What works perfectly for Opus might need more detail for Haiku.

## Structure Best Practices

### Writing Effective Descriptions

The `description` field enables skill discovery and is the PRIMARY triggering mechanism.

**Critical**: Always write in third person.

| Form | Example | Status |
|------|---------|--------|
| Third person | "Processes Excel files and generates reports" | ✓ Good |
| First person | "I can help you process Excel files" | ✗ Avoid |
| Second person | "You can use this to process Excel files" | ✗ Avoid |

**Be specific and include key terms**:

```yaml
# Good - specific with triggers
description: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

# Good - action-oriented with context
description: "Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files."

# Bad - too vague
description: "Helps with documents"
description: "Processes data"
```

### Naming Conventions

Use consistent naming patterns. Recommended: **gerund form** (verb + -ing).

**Good examples**:
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`

**Acceptable alternatives**:
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

**Avoid**:
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`

### Progressive Disclosure Patterns

Keep SKILL.md body under 500 lines. Split content when approaching this limit.

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing

## Quick start
[Minimal example]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing)
    ├── sales.md (pipeline, accounts)
    └── product.md (API usage, features)
```

When user asks about sales metrics, Claude only reads sales-related schemas.

**Pattern 3: Conditional details**
```markdown
## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

### Avoid Deeply Nested References

Claude may partially read files when they're referenced from other referenced files.

**Bad** (too deep):
```
SKILL.md → advanced.md → details.md → actual info
```

**Good** (one level deep):
```
SKILL.md → advanced.md
SKILL.md → reference.md
SKILL.md → examples.md
```

### Structure Longer Reference Files with TOC

For files longer than 100 lines, include a table of contents at the top:

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...
```

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps. For complex workflows, provide a checklist:

```markdown
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`
...
```

### Implement Feedback Loops

Common pattern: Run validator → fix errors → repeat

```markdown
## Document editing process
1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py unpacked_dir/ output.docx`
```

## Content Guidelines

### Avoid Time-Sensitive Information

**Bad** (will become wrong):
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Good** (use "old patterns" section):
```markdown
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

### Use Consistent Terminology

Choose one term and use it throughout:

| Good (Consistent) | Bad (Inconsistent) |
|-------------------|-------------------|
| Always "API endpoint" | Mix "API endpoint", "URL", "API route" |
| Always "field" | Mix "field", "box", "element" |
| Always "extract" | Mix "extract", "pull", "get", "retrieve" |

### Provide a Default, Not Multiple Options

**Bad** (confusing):
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...
```

**Good** (default with escape hatch):
```markdown
Use pdfplumber for text extraction:
import pdfplumber

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

## Evaluation and Iteration

### Build Evaluations First

Create evaluations BEFORE writing extensive documentation.

**Evaluation-driven development**:
1. **Identify gaps**: Run Claude on representative tasks without a skill
2. **Create evaluations**: Build 3+ scenarios that test these gaps
3. **Establish baseline**: Measure Claude's performance without the skill
4. **Write minimal instructions**: Just enough to address gaps
5. **Iterate**: Execute evaluations, compare against baseline, refine

### Develop Skills Iteratively with Claude

Work with one instance of Claude ("Claude A") to create a skill used by other instances ("Claude B").

**Creating a new skill**:
1. Complete a task with Claude A using normal prompting
2. Identify what context you repeatedly provided
3. Ask Claude A to create a skill capturing that pattern
4. Review for conciseness
5. Test with Claude B on similar tasks
6. Iterate based on observation

**Iterating on existing skills**:
1. Use skill in real workflows with Claude B
2. Observe behavior, note struggles
3. Return to Claude A with specifics
4. Apply refinements, test again
5. Repeat

### Observe How Claude Navigates Skills

Watch for:
- **Unexpected exploration paths**: Structure might not be intuitive
- **Missed connections**: Links might need to be more explicit
- **Overreliance on certain sections**: Consider moving content to SKILL.md
- **Ignored content**: Might be unnecessary or poorly signaled

## Advanced: Skills with Executable Code

### Solve, Don't Punt

Handle error conditions rather than punting to Claude.

**Good**:
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

**Bad**:
```python
def process_file(path):
    return open(path).read()  # Just fail and let Claude figure it out
```

### Justify Configuration Parameters

No "voodoo constants":

**Good**:
```python
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

**Bad**:
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### Provide Utility Scripts

Benefits of pre-made scripts:
- More reliable than generated code
- Save tokens (no code in context)
- Save time (no generation required)
- Ensure consistency

Make clear whether Claude should:
- **Execute the script** (most common): "Run `analyze_form.py` to extract fields"
- **Read it as reference** (for complex logic): "See `analyze_form.py` for the algorithm"

### Create Verifiable Intermediate Outputs

For complex tasks, use plan-validate-execute pattern:

1. Analyze → **Create plan file** → **Validate plan** → Execute → Verify

Make validation scripts verbose with specific error messages:
```
Field 'signature_date' not found.
Available fields: customer_name, order_total, signature_date_signed
```

## Quality Checklist

### Core Quality
- [ ] Description is specific and includes key terms
- [ ] Description includes both what and when
- [ ] Description is third person
- [ ] SKILL.md body is under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts solve problems rather than punt
- [ ] Error handling is explicit and helpful
- [ ] No unexplained constants
- [ ] Required packages listed
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths
- [ ] Validation steps for critical operations
- [ ] Feedback loops for quality-critical tasks

### Testing
- [ ] At least three evaluations created
- [ ] Tested with all target models
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated
