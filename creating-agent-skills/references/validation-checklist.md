# Skill Validation Checklist

## Pre-Creation Checklist

- [ ] Ran Claude on representative tasks WITHOUT a skill
- [ ] Documented specific failures or missing context
- [ ] Created 3+ test scenarios that expose these gaps
- [ ] Confirmed skill is necessary (not over-engineering)

## Frontmatter Validation

### name Field
- [ ] Lowercase only
- [ ] Alphanumeric and hyphens only
- [ ] Max 64 characters
- [ ] Matches directory name
- [ ] No reserved words ("anthropic", "claude")
- [ ] Descriptive, not vague (`pdf-processing` not `helper`)

### description Field
- [ ] Non-empty
- [ ] Max 1024 characters
- [ ] **Written in third person** ("Processes files" not "I process files")
- [ ] Describes what skill does
- [ ] Includes trigger conditions ("Use when...")
- [ ] Contains keywords users would naturally say
- [ ] No "When to use" info buried in body

### Optional Fields (if used)
- [ ] `allowed-tools`: Valid tool names and patterns
- [ ] `model`: Valid model identifier
- [ ] `context`: Only "fork" is valid
- [ ] `agent`: Valid agent type (Explore, Plan, general-purpose)
- [ ] `user-invocable`: Boolean (true/false)
- [ ] `disable-model-invocation`: Boolean
- [ ] `hooks`: Valid hook structure

## Structure Validation

### Directory
- [ ] Skill directory name matches `name` in frontmatter
- [ ] Directory name is lowercase with hyphens only
- [ ] SKILL.md exists in root of skill directory
- [ ] No README.md, CHANGELOG.md, or auxiliary docs

### SKILL.md
- [ ] **File is under 500 lines**
- [ ] Has valid YAML frontmatter
- [ ] Body uses clear markdown formatting
- [ ] Uses imperative form ("Analyze", not "You should analyze")

### Resource Directories
- [ ] `references/` contains only text files loaded into context
- [ ] `scripts/` contains only executable code
- [ ] `assets/` contains templates/static files
- [ ] Clear distinction maintained between directories

## Content Validation

### Conciseness
- [ ] Only includes what Claude doesn't already know
- [ ] No over-explanation of common concepts
- [ ] Prefers examples over verbose text
- [ ] Each paragraph justifies its token cost

### Quick Reference
- [ ] Has essential lookup tables
- [ ] Provides immediate value without reading references
- [ ] Answers most common questions

### Instructions
- [ ] Uses imperative form
- [ ] Step-by-step where appropriate
- [ ] Concrete, not abstract
- [ ] Specific, actionable guidance

### Examples
- [ ] Has concrete usage examples
- [ ] Examples are minimal but complete
- [ ] Uses input/output pairs where helpful

### References
- [ ] Links to supporting files use relative paths
- [ ] **References are one level deep** (not nested)
- [ ] No duplicated content between SKILL.md and references
- [ ] Files over 100 lines have table of contents

## Progressive Disclosure Validation

- [ ] SKILL.md is self-contained for basic use
- [ ] Detailed information is in references/
- [ ] Scripts are executable, not documentation
- [ ] Assets are for output, not context
- [ ] Only essential content in SKILL.md

## Tool & Script Validation

### allowed-tools
- [ ] Appropriate restrictions for skill purpose
- [ ] Read-only skills restrict to Read, Grep, Glob
- [ ] No unnecessary tool permissions

### scripts/
- [ ] Scripts are executable
- [ ] Scripts have proper permissions
- [ ] Error handling is explicit and helpful
- [ ] No "magic numbers" without explanation
- [ ] Scripts solve problems, don't punt to Claude
- [ ] Clear whether to execute or read as reference

### Paths
- [ ] **All paths use forward slashes** (no Windows-style)
- [ ] Uses `{baseDir}` for skill-relative paths
- [ ] No hardcoded absolute paths

## Quality Validation

### Terminology
- [ ] Consistent terminology throughout
- [ ] No mixing of synonyms (pick one term, use it everywhere)

### Time Sensitivity
- [ ] No time-sensitive information
- [ ] Or uses "current" vs "old patterns" structure

### Options
- [ ] Provides default option, not multiple choices
- [ ] Escape hatches for special cases

### Workflows
- [ ] Complex workflows have clear steps
- [ ] Validation/verification steps included
- [ ] Feedback loops for quality-critical tasks

## Testing Validation

- [ ] At least 3 test scenarios created
- [ ] Tested with all target models (Haiku, Sonnet, Opus)
- [ ] Tested with real user requests
- [ ] Skill triggers correctly from description
- [ ] Produces expected outputs
- [ ] Handles edge cases
- [ ] Tool restrictions work correctly

## Security Validation

- [ ] No hardcoded credentials
- [ ] Scripts don't expose sensitive data
- [ ] Tool restrictions are appropriate
- [ ] No command injection vulnerabilities
- [ ] Skill from trusted source (if external)

## MCP Tool Validation (if applicable)

- [ ] Uses fully qualified names (`ServerName:tool_name`)
- [ ] Server names are correct
- [ ] Tool names exist on specified server

## Final Checklist

- [ ] All validation above passes
- [ ] Skill has been tested on real tasks
- [ ] Documentation matches implementation
- [ ] Iterated based on Claude's actual behavior
- [ ] Ready for distribution

## Quick Validation Commands

```bash
# Check SKILL.md line count (must be < 500)
wc -l SKILL.md

# Validate YAML frontmatter exists
head -50 SKILL.md | grep -c "^---"  # Should be 2

# Check name format in frontmatter
grep "^name:" SKILL.md

# Check description exists and length
grep "^description:" SKILL.md | wc -c  # Should be < 1024

# Check for auxiliary docs (should return nothing)
ls -la | grep -E "(README|CHANGELOG|INSTALLATION|QUICK_REFERENCE)"

# Check for Windows-style paths (should return nothing)
grep -r '\\' *.md references/*.md 2>/dev/null

# Check directory structure
find . -type f -name "*.md" | head -20

# List all reference files
ls -la references/ 2>/dev/null

# List all scripts
ls -la scripts/ 2>/dev/null

# Check for hardcoded paths
grep -r "/Users/" *.md references/*.md 2>/dev/null
grep -r "/home/" *.md references/*.md 2>/dev/null
```

## Evaluation Template

```json
{
  "skill": "your-skill-name",
  "test_scenarios": [
    {
      "query": "User request that should trigger skill",
      "expected_behavior": [
        "Skill should activate",
        "Should perform X action",
        "Should produce Y output"
      ]
    },
    {
      "query": "Another test scenario",
      "expected_behavior": [
        "Expected behavior 1",
        "Expected behavior 2"
      ]
    },
    {
      "query": "Edge case scenario",
      "expected_behavior": [
        "Should handle gracefully",
        "Should provide helpful error message"
      ]
    }
  ]
}
```
