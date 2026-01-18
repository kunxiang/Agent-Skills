# CLAUDE.md - AI Assistant Guidelines

## Project Overview
[Brief description of your project]

## Architecture
- **Pattern**: [MVC/Clean Architecture/Component-Based/etc.]
- **Key Technologies**: [List main tech stack]
- **Original Skill Used**: [skill-name if applicable]

## Coding Standards

### File Naming
- Use [camelCase/PascalCase/kebab-case/snake_case]
- Components: [naming pattern]
- Tests: [test file pattern]

### Code Style
- **Indentation**: [spaces/tabs, how many]
- **Quotes**: [single/double]
- **Semicolons**: [yes/no]
- **Line Length**: [80/100/120 chars]

### Import Order
1. External packages
2. Internal modules
3. Local components
4. Styles

## Project Structure
```
src/
├── [explain main directories]
└── [and their purposes]
```

## Modification Rules

### DO's
- ✅ Follow existing patterns exactly
- ✅ Read similar files before creating new ones
- ✅ Run tests before committing
- ✅ Match existing error handling patterns

### DON'Ts
- ❌ Add new architectural patterns
- ❌ Change code formatting
- ❌ Add dependencies without discussion
- ❌ Reorganize file structure

## Common Patterns

### API Endpoints
```javascript
// Always follow this pattern for new endpoints
router.get('/resource/:id', authenticate, validate, controller.method);
```

### Component Structure
```javascript
// New components must follow this structure
export const Component = () => {
  // hooks
  // state
  // effects
  // handlers
  // render
};
```

### State Management
[Describe how state should be managed]

## Testing Requirements
- Minimum coverage: [X%]
- Test framework: [Jest/Mocha/etc.]
- Test pattern: [describe pattern]

## Before Making Changes
1. Run `[command]` to analyze project
2. Read existing similar features
3. Check test coverage
4. Verify build passes

## Deployment Notes
[Any special deployment considerations]