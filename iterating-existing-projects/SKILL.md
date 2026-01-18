---
name: iterating-existing-projects
description: "Modifies and iterates on existing projects while maintaining their established architecture, coding standards, and design patterns. Use when user wants to update features, fix bugs, refactor code, or add new functionality to an existing project without breaking established conventions."
---

# Iterating Existing Projects

## Core Principle

**NEVER make assumptions** about project structure. **ALWAYS analyze first**, then modify according to discovered patterns.

## Phase 1: Project Discovery (MANDATORY)

Before ANY modification, execute this discovery sequence:

### 1.1 Locate Project Context

```bash
# Find project configuration files
find . -maxdepth 3 -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" | head -20
```

### 1.2 Check for Skill Documentation

**Critical**: Check if project was created with a skill:

1. Look for `.claude/` directory:
   ```bash
   ls -la .claude/
   ```

2. Search for skill references:
   ```bash
   grep -r "skill\|SKILL" . --include="*.md" | head -10
   ```

3. Check for CLAUDE.md or similar AI instructions:
   ```bash
   find . -name "*CLAUDE*" -o -name "*AI*" -o -name "*INSTRUCTIONS*" | head -10
   ```

### 1.3 Analyze Project Structure

Read these files in order of priority:

| Priority | File Pattern | Purpose |
|----------|-------------|---------|
| 1 | `CLAUDE.md`, `AI.md` | AI-specific instructions |
| 2 | `README.md` | Project overview |
| 3 | `ARCHITECTURE.md` | System design |
| 4 | `CONTRIBUTING.md` | Development guidelines |
| 5 | `package.json`, `pyproject.toml`, etc. | Tech stack |

## Phase 2: Pattern Recognition

### 2.1 Identify Architecture Pattern

Analyze existing code to determine:

```bash
# For JavaScript/TypeScript
find src -name "*.ts" -o -name "*.js" | head -5 | xargs head -50

# For Python
find . -name "*.py" | head -5 | xargs head -50
```

Common patterns to identify:

| Pattern | Indicators |
|---------|-----------|
| **MVC** | `models/`, `views/`, `controllers/` |
| **Clean Architecture** | `domain/`, `application/`, `infrastructure/` |
| **Layered** | `presentation/`, `business/`, `data/` |
| **Component-based** | `components/`, similar file structures |
| **Module-based** | `modules/`, self-contained features |

### 2.2 Extract Coding Standards

Analyze 3-5 existing files to determine:

- **Naming conventions**: camelCase, snake_case, PascalCase
- **File organization**: exports pattern, import order
- **Comment style**: JSDoc, docstrings, inline
- **Error handling**: try-catch, error boundaries, Result types
- **State management**: Redux, Context, Zustand, Pinia
- **Testing patterns**: unit, integration, E2E

## Phase 3: Modification Strategy

### 3.1 Create Modification Plan

Before coding, create a structured plan:

```markdown
## Modification Plan

### Current State
- Architecture: [identified pattern]
- Key Dependencies: [list]
- Affected Components: [list]

### Proposed Changes
1. [Change 1]: Impact on [components]
2. [Change 2]: Impact on [components]

### Risk Assessment
- Breaking changes: [list]
- Required migrations: [list]
```

### 3.2 Follow Existing Patterns

**Golden Rule**: New code should be indistinguishable from existing code.

#### Example Pattern Matching

If existing code uses:
```javascript
// Existing pattern
export const useUserData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  // ...
  return { data, loading, refetch };
};
```

Your new code MUST follow:
```javascript
// Your new feature - same pattern
export const useProductData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  // ...
  return { data, loading, refetch };
};
```

## Phase 4: Implementation Rules

### 4.1 File Placement

Analyze existing structure, then place files accordingly:

```bash
# Analyze structure
tree -d -L 3 src/

# Find similar files
find . -name "*similar_feature*" -type f
```

### 4.2 Import/Export Patterns

Match existing patterns exactly:

| Pattern | Example |
|---------|---------|
| Named exports | `export { Component }` |
| Default exports | `export default Component` |
| Barrel exports | `index.ts` with re-exports |
| Direct imports | Import from specific files |

### 4.3 Dependencies

**NEVER** add new dependencies without checking:

1. Can existing dependencies solve this?
2. Is there an established pattern for this need?
3. Does project have dependency guidelines?

## Phase 5: Validation

### 5.1 Pre-commit Checks

```bash
# Run existing test suite
npm test || yarn test || pytest

# Check linting
npm run lint || yarn lint || pylint .

# Type checking
npm run type-check || yarn type-check || mypy .
```

### 5.2 Pattern Compliance Checklist

- [ ] Naming follows project convention
- [ ] File structure matches existing patterns
- [ ] Import/export style is consistent
- [ ] Error handling matches project style
- [ ] Comments follow project format
- [ ] Tests follow existing patterns

## Common Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Adding new architecture | Breaks consistency | Follow existing architecture |
| Changing code style | Creates inconsistency | Match existing style exactly |
| New dependency for solved problem | Bloat | Use existing solutions |
| Different error handling | Inconsistent UX | Follow established patterns |
| New file organization | Confuses structure | Match existing organization |

## Special Cases

### When Project Has No Clear Pattern

If analysis reveals inconsistent patterns:

1. **Document findings**:
   ```markdown
   ## Inconsistency Report
   - Pattern A used in: [files]
   - Pattern B used in: [files]
   - Recommendation: [which to follow]
   ```

2. **Follow most recent pattern** (check git history)

3. **Ask user** for clarification

### When Original Skill Exists

If project was created with a skill:

1. **Read the original skill**:
   ```bash
   cat .claude/skills/[skill-name]/SKILL.md
   ```

2. **Follow skill guidelines** for new features

3. **Maintain skill conventions** throughout

## Quick Reference Tables

### Language-Specific Patterns

| Language | Config Files | Build Tool | Test Framework |
|----------|-------------|------------|----------------|
| JavaScript | package.json | npm/yarn/pnpm | jest/mocha/vitest |
| TypeScript | tsconfig.json | tsc + bundler | jest/vitest |
| Python | pyproject.toml/setup.py | pip/poetry | pytest/unittest |
| Java | pom.xml/build.gradle | maven/gradle | junit |
| Go | go.mod | go build | go test |

### Framework-Specific Patterns

| Framework | Structure Pattern | State Management | Routing |
|-----------|------------------|------------------|---------|
| React | components/ | Context/Redux/Zustand | React Router |
| Vue | components/views/ | Vuex/Pinia | Vue Router |
| Angular | modules/ | Services/NgRx | Angular Router |
| Next.js | pages/ or app/ | Built-in/Redux | File-based |

## Error Recovery

If modification breaks something:

1. **Immediate rollback**:
   ```bash
   git diff  # Review changes
   git checkout -- [broken-file]  # Revert file
   ```

2. **Analyze what went wrong**

3. **Adjust approach** based on failure

4. **Document for future reference**

## References

For detailed patterns and examples:
- [references/pattern-library.md](references/pattern-library.md) - Common patterns catalog
- [references/migration-strategies.md](references/migration-strategies.md) - Safe migration approaches
- [references/testing-patterns.md](references/testing-patterns.md) - Test writing guidelines