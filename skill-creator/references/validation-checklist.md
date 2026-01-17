# Skill Validation Checklist

## Pre-Creation Checklist

- [ ] Collected 3-5 concrete usage examples
- [ ] Identified what Claude doesn't already know
- [ ] Determined if skill is necessary (vs. simple prompt)
- [ ] Identified required tools and restrictions

## Structure Validation

### Directory
- [ ] Skill directory name matches `name` in frontmatter
- [ ] Directory name is lowercase with hyphens only
- [ ] SKILL.md exists in root of skill directory
- [ ] No README.md, CHANGELOG.md, or auxiliary docs

### SKILL.md
- [ ] File is under 500 lines
- [ ] Has valid YAML frontmatter
- [ ] Frontmatter has `name` field
- [ ] Frontmatter has `description` field
- [ ] Body uses clear markdown formatting

## Frontmatter Validation

### name Field
- [ ] Lowercase only
- [ ] Alphanumeric and hyphens only
- [ ] Max 64 characters
- [ ] Matches directory name

### description Field
- [ ] Max 1024 characters
- [ ] Describes what skill does
- [ ] Includes trigger conditions ("Use when...")
- [ ] Contains keywords users would naturally say
- [ ] No "When to use" info buried in body

### Optional Fields (if used)
- [ ] `allowed-tools`: Valid tool names
- [ ] `model`: Valid model identifier
- [ ] `context`: Only "fork" is valid
- [ ] `agent`: Valid agent type
- [ ] `user-invocable`: Boolean (true/false)
- [ ] `hooks`: Valid hook structure

## Content Validation

### Quick Reference
- [ ] Has essential lookup tables
- [ ] Provides immediate value without reading references
- [ ] Answers most common questions

### Instructions
- [ ] Uses imperative form ("Do X", not "You should do X")
- [ ] Step-by-step where appropriate
- [ ] Concrete, not abstract

### Examples
- [ ] Has concrete usage examples
- [ ] Examples are minimal but complete
- [ ] Covers common use cases

### References
- [ ] Links to supporting files use relative paths
- [ ] References are one level deep (not nested)
- [ ] No duplicated content between SKILL.md and references

## Progressive Disclosure Validation

- [ ] SKILL.md is self-contained for basic use
- [ ] Detailed information is in references/
- [ ] Scripts are executable, not documentation
- [ ] Assets are for output, not context

## Resource Validation

### references/
- [ ] Each file has clear purpose
- [ ] No duplication between files
- [ ] Formatted for easy reading
- [ ] Linked from SKILL.md

### scripts/
- [ ] Scripts are executable
- [ ] Scripts have proper permissions
- [ ] Scripts don't require installation
- [ ] Error handling is appropriate

### assets/
- [ ] Templates are ready to use
- [ ] Assets don't need modification
- [ ] Paths are documented in SKILL.md

## Quality Validation

### Conciseness
- [ ] Only includes what Claude doesn't know
- [ ] No over-explanation
- [ ] Prefers examples over verbose text

### Clarity
- [ ] Instructions are unambiguous
- [ ] No jargon without definition
- [ ] Structure is logical

### Completeness
- [ ] Covers all stated use cases
- [ ] No missing steps in workflows
- [ ] References actually exist

## Testing Validation

- [ ] Tested with real user requests
- [ ] Triggers correctly from description
- [ ] Produces expected outputs
- [ ] Handles edge cases
- [ ] Tool restrictions work correctly (if any)

## Security Validation

- [ ] No hardcoded credentials
- [ ] Scripts don't expose sensitive data
- [ ] Tool restrictions are appropriate
- [ ] No command injection vulnerabilities

## Final Checklist

- [ ] All validation above passes
- [ ] Skill has been tested on real tasks
- [ ] Documentation matches implementation
- [ ] Ready for distribution

## Quick Validation Commands

### Check SKILL.md line count
```bash
wc -l SKILL.md  # Should be < 500
```

### Validate YAML frontmatter
```bash
head -50 SKILL.md | grep -A 20 "^---"
```

### Check directory structure
```bash
find . -type f -name "*.md" | head -20
```

### Verify no auxiliary docs
```bash
ls -la | grep -E "(README|CHANGELOG|INSTALLATION|QUICK_REFERENCE)"
# Should return nothing
```
