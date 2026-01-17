# Skill Design Patterns

## Basic Patterns

### Pattern 1: Script Automation

**Use case**: Complex operations requiring multiple commands or deterministic logic.

Offload computational tasks to Python/Bash scripts in `scripts/`. The skill prompt tells Claude to execute the script and process its output.

```markdown
## Analysis Workflow

Run scripts/analyzer.py on the target directory:
`python {baseDir}/scripts/analyzer.py --path "$USER_PATH"`

Parse the generated `report.json` and present findings to user.
```

**Required tools**: `Bash(python {baseDir}/scripts:*)`

### Pattern 2: Read - Process - Write

**Use case**: File transformation and data processing.

The simplest pattern — read input, transform following instructions, write output.

```markdown
## Processing Workflow
1. Read input file using Read tool
2. Parse content according to format
3. Transform data following specifications
4. Write output using Write tool
5. Report completion with summary
```

**Required tools**: `Read, Write`

### Pattern 3: Search - Analyze - Report

**Use case**: Codebase analysis and pattern detection.

Search codebase for patterns using Grep, read matching files for context, analyze findings, generate structured report.

```markdown
## Analysis Process
1. Use Grep to find relevant code patterns
2. Read each matched file
3. Analyze for vulnerabilities
4. Generate structured report
```

**Required tools**: `Grep, Read`

### Pattern 4: Command Chain Execution

**Use case**: Multi-step operations with dependencies.

Execute a sequence of commands where each step depends on the previous one's success.

```markdown
## Build Pipeline
Execute analysis pipeline:
npm install && npm run lint && npm test

Report results from each stage.
```

**Required tools**: `Bash(npm install:*), Bash(npm run:*), Bash(npm test:*)`

## Progressive Disclosure Patterns

### Pattern 5: High-Level Guide with References

**Use case**: Skills with multiple detailed topics.

```
my-skill/
├── SKILL.md              # Overview + navigation
└── references/
    ├── topic-a.md
    ├── topic-b.md
    └── topic-c.md
```

**SKILL.md**:
```markdown
# My Skill

## Quick Reference
[Essential tables]

## Core Workflow
[Main instructions]

## Detailed Topics
- **Topic A**: See [references/topic-a.md](references/topic-a.md)
- **Topic B**: See [references/topic-b.md](references/topic-b.md)
```

Claude loads reference files only when needed.

### Pattern 6: Domain-Specific Organization

**Use case**: Skills covering multiple domains/departments.

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md        # Finance team schemas
    ├── sales.md          # Sales team schemas
    └── product.md        # Product team schemas
```

**SKILL.md**:
```markdown
# BigQuery Skill

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features → See [reference/product.md](reference/product.md)

## Quick search
grep -i "revenue" reference/finance.md
```

When user asks about sales metrics, Claude only reads sales-related schemas.

### Pattern 7: Conditional Details

**Use case**: Users need different levels of detail.

```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when user needs those features.

## Advanced Patterns

### Pattern 8: Wizard-Style Multi-Step Workflows

**Use case**: Complex processes requiring user input at each step.

Break complex tasks into discrete steps with explicit user confirmation.

```markdown
## Workflow

### Step 1: Initial Setup
1. Ask user for project type
2. Validate prerequisites exist
3. Create base configuration

Wait for user confirmation before proceeding.

### Step 2: Configuration
1. Present configuration options
2. Ask user to choose settings
3. Generate config file

Wait for user confirmation before proceeding.

### Step 3: Initialization
1. Run initialization scripts
2. Verify setup successful
3. Report results
```

### Pattern 9: Template-Based Generation

**Use case**: Creating structured outputs from templates in `assets/`.

```markdown
## Generation Process
1. Read template from {baseDir}/assets/template.html
2. Parse user requirements
3. Fill template placeholders:
   - {{name}} → user-provided name
   - {{summary}} → generated summary
   - {{date}} → current date
4. Write filled template to output file
5. Report completion
```

### Pattern 10: Iterative Refinement

**Use case**: Processes requiring multiple passes with increasing depth.

```markdown
## Iterative Analysis

### Pass 1: Broad Scan
1. Search entire codebase for patterns
2. Identify high-level issues
3. Categorize findings

### Pass 2: Deep Analysis
For each high-level issue:
1. Read full file context
2. Analyze root cause
3. Determine severity

### Pass 3: Recommendation
For each finding:
1. Research best practices
2. Generate specific fix
3. Estimate effort

Present final report with all findings and recommendations.
```

### Pattern 11: Context Aggregation

**Use case**: Combining information from multiple sources.

```markdown
## Context Gathering
1. Read project README.md for overview
2. Analyze package.json for dependencies
3. Grep codebase for specific patterns
4. Check git history for recent changes
5. Synthesize findings into coherent summary
```

### Pattern 12: Plan-Validate-Execute

**Use case**: Complex, error-prone operations requiring verification.

```markdown
## Workflow

### Phase 1: Planning
1. Analyze requirements
2. Generate `changes.json` plan file
3. Do NOT apply any changes yet

### Phase 2: Validation
Run: `python scripts/validate_plan.py changes.json`

If validation fails:
- Review error messages
- Fix the plan
- Validate again

### Phase 3: Execution
Only after validation passes:
Run: `python scripts/apply_changes.py changes.json`

### Phase 4: Verification
Run: `python scripts/verify_output.py`
```

### Pattern 13: Feedback Loop

**Use case**: Quality-critical tasks requiring iterative improvement.

```markdown
## Document Editing Process
1. Make edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

## Template Patterns

### Pattern 14: Strict Template (Low Freedom)

**Use case**: API responses, data formats, compliance requirements.

```markdown
## Report Structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Pattern 15: Flexible Template (High Freedom)

**Use case**: When adaptation is useful.

```markdown
## Report Structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

### Pattern 16: Examples Pattern

**Use case**: Output quality depends on seeing examples.

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation

Follow this style: type(scope): brief description, then detailed explanation.
```

## Degrees of Freedom

### High Freedom (Text-Based)

Use when multiple approaches are valid.

```markdown
## Code Review Guidelines

When reviewing code, consider:
- Readability and maintainability
- Performance implications
- Security concerns
- Test coverage
```

### Medium Freedom (Pseudocode)

Use when a preferred pattern exists but variation is acceptable.

```markdown
## Data Processing Pattern

1. Load data from source
2. Validate schema
3. Transform fields:
   - Normalize dates to ISO format
   - Convert currencies to USD
4. Output to destination
```

### Low Freedom (Exact Scripts)

Use when operations are fragile and need precision.

```markdown
## PDF Form Filling

from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

writer.update_page_form_field_values(
    writer.pages[0],
    {"field_name": "value"}
)

with open("filled.pdf", "wb") as f:
    writer.write(f)
```

## Anti-Patterns to Avoid

### 1. Nested References (Bad)
```
skill/
├── SKILL.md → references/a.md → references/deep/b.md → ...
```
Keep references one level deep from SKILL.md.

### 2. Duplicated Content (Bad)
Don't repeat the same information in SKILL.md and references.

### 3. Monolithic SKILL.md (Bad)
Don't put everything in SKILL.md. Split into references when approaching 500 lines.

### 4. Too Many Entry Points (Bad)
Don't have multiple reference files that could all be starting points. Have one clear entry point (SKILL.md) that navigates to others.

### 5. Missing Quick Reference (Bad)
Always include essential information directly in SKILL.md for immediate value.

### 6. Multiple Options Without Default (Bad)
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF...
```

**Good**:
```markdown
Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image instead.
```
