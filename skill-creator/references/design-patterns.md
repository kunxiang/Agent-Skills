# Skill Design Patterns

## Pattern 1: High-Level Guide with References

Best for skills with multiple detailed topics.

```
my-skill/
├── SKILL.md              # Overview + navigation
└── references/
    ├── topic-a.md        # Detailed topic A
    ├── topic-b.md        # Detailed topic B
    └── topic-c.md        # Detailed topic C
```

**SKILL.md Structure:**
```markdown
# My Skill

## Quick Reference
[Essential tables]

## Core Workflow
[Main instructions]

## Detailed Topics
- **Topic A**: See [references/topic-a.md](references/topic-a.md)
- **Topic B**: See [references/topic-b.md](references/topic-b.md)
- **Topic C**: See [references/topic-c.md](references/topic-c.md)
```

## Pattern 2: Domain-Specific Organization

Best for skills covering multiple domains/departments.

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md        # Finance team schemas
    ├── sales.md          # Sales team schemas
    ├── product.md        # Product team schemas
    └── marketing.md      # Marketing team schemas
```

**SKILL.md:**
```markdown
# BigQuery Skill

## Quick Start
[Common queries]

## Domain References
- **Finance queries**: See [references/finance.md](references/finance.md)
- **Sales queries**: See [references/sales.md](references/sales.md)
- **Product queries**: See [references/product.md](references/product.md)
- **Marketing queries**: See [references/marketing.md](references/marketing.md)
```

## Pattern 3: Conditional Details

Best when users need different levels of detail.

```
document-skill/
├── SKILL.md
├── ADVANCED.md
└── OOXML.md
```

**SKILL.md:**
```markdown
# Document Processing

## Basic Operations
For simple edits, modify XML directly:
[Basic examples]

## Advanced Operations
**For tracked changes**: See [ADVANCED.md](ADVANCED.md)
**For OOXML internals**: See [OOXML.md](OOXML.md)
```

## Pattern 4: Script-Heavy Skill

Best when automation is the primary value.

```
automation-skill/
├── SKILL.md
├── scripts/
│   ├── validate.py
│   ├── process.py
│   └── export.py
└── references/
    └── api-docs.md
```

**SKILL.md:**
```markdown
# Automation Skill

## Available Scripts

### Validation
\`\`\`bash
python scripts/validate.py input.txt
\`\`\`

### Processing
\`\`\`bash
python scripts/process.py --input data.csv --output result.json
\`\`\`

### Export
\`\`\`bash
python scripts/export.py --format xlsx
\`\`\`

## API Reference
For detailed API documentation, see [references/api-docs.md](references/api-docs.md)
```

## Pattern 5: Template-Based Skill

Best for generating standardized outputs.

```
template-skill/
├── SKILL.md
└── assets/
    ├── templates/
    │   ├── basic.md
    │   ├── detailed.md
    │   └── executive.md
    └── boilerplate/
        └── project-structure/
```

**SKILL.md:**
```markdown
# Template Skill

## Available Templates

| Template | Use Case | Location |
|----------|----------|----------|
| Basic | Quick documents | `assets/templates/basic.md` |
| Detailed | Full documentation | `assets/templates/detailed.md` |
| Executive | Summary reports | `assets/templates/executive.md` |

## Usage
1. Copy the appropriate template
2. Fill in the placeholders
3. Customize as needed

## Project Boilerplate
For new projects, copy from `assets/boilerplate/project-structure/`
```

## Pattern 6: Workflow Skill

Best for multi-step processes.

```
deployment-skill/
├── SKILL.md
├── scripts/
│   ├── pre-check.sh
│   ├── deploy.sh
│   └── rollback.sh
└── references/
    ├── environments.md
    └── troubleshooting.md
```

**SKILL.md:**
```markdown
# Deployment Skill

## Workflow

### Step 1: Pre-deployment Check
\`\`\`bash
./scripts/pre-check.sh
\`\`\`

### Step 2: Deploy
\`\`\`bash
./scripts/deploy.sh --env staging
\`\`\`

### Step 3: Verify
[Verification instructions]

### Rollback (if needed)
\`\`\`bash
./scripts/rollback.sh --version previous
\`\`\`

## References
- **Environment configs**: [references/environments.md](references/environments.md)
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
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

\`\`\`pseudocode
1. Load data from source
2. Validate schema
3. Transform fields:
   - Normalize dates to ISO format
   - Convert currencies to USD
4. Output to destination
\`\`\`
```

### Low Freedom (Exact Scripts)
Use when operations are fragile and need precision.

```markdown
## PDF Form Filling

\`\`\`python
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
\`\`\`
```

## Anti-Patterns

### 1. Nested References (Bad)
```
skill/
├── SKILL.md → references/a.md → references/deep/b.md → ...
```
Keep references one level deep from SKILL.md.

### 2. Duplicated Content (Bad)
Don't repeat the same information in SKILL.md and references.

### 3. Monolithic SKILL.md (Bad)
Don't put everything in SKILL.md. Split into references.

### 4. Too Many Entry Points (Bad)
Don't have multiple reference files that could all be starting points.

### 5. Missing Quick Reference (Bad)
Always include essential information directly in SKILL.md.
