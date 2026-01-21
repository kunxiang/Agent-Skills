# Iterating Existing Projects

> **Version**: 1.0
> **Created**: 2026-01-19
> **Purpose**: Modify and iterate on existing projects while maintaining established architecture and patterns

## 🎯 Core Principle

**STRICTLY MAINTAIN EXISTING PATTERNS** - This skill ensures all modifications respect and follow the established architecture, coding standards, and design patterns of the existing project.

## 📋 Mandatory Process

### Phase 1: Analysis (REQUIRED)

Before ANY modification:

1. **Read CLAUDE.md**
   ```bash
   # Check for project-specific instructions
   cat CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found"
   ```

2. **Analyze Existing Implementation**
   - Read ALL files that will be modified
   - Identify current patterns:
     - File structure
     - Naming conventions
     - Import patterns
     - Error handling approach
     - Testing patterns
   - Document findings

3. **Understand Dependencies**
   ```bash
   # For Python projects
   grep -r "from.*import" --include="*.py" | head -20

   # Check package.json for JS/TS
   cat package.json 2>/dev/null | grep -A20 dependencies
   ```

### Phase 2: Planning (REQUIRED)

Create a modification plan:

```markdown
## Current Implementation Analysis
- Architecture: [three-layer/MVC/etc.]
- Patterns used: [repository/service/etc.]
- Naming convention: [camelCase/snake_case]
- Error handling: [try-catch/result-types]

## Modification Plan
1. Files to modify: [list]
2. New files needed: [list with locations]
3. Pattern compliance check: ✅/❌
```

### Phase 3: Implementation Rules

#### ✅ MUST DO:
- **Preserve existing architecture** - Never change the fundamental structure
- **Follow naming conventions** - Match exactly what exists
- **Maintain import patterns** - Use same import style
- **Keep error handling consistent** - Don't introduce new patterns
- **Match code style** - Indentation, spacing, comments
- **Update related tests** - If tests exist, update them
- **Preserve file locations** - Don't reorganize without explicit request

#### ❌ MUST NOT:
- **No architectural changes** - Don't "improve" the architecture
- **No new patterns** - Don't introduce new design patterns
- **No style changes** - Don't reformat existing code
- **No unnecessary refactoring** - Only change what's needed
- **No new dependencies** - Without explicit approval
- **No file reorganization** - Unless specifically requested
- **No "optimizations"** - Unless specifically requested

### Phase 4: Validation (REQUIRED)

After modifications:

1. **Syntax Check**
   ```bash
   # Python
   python -m py_compile modified_file.py

   # JavaScript/TypeScript
   npx tsc --noEmit modified_file.ts
   ```

2. **Import Verification**
   ```bash
   # Test imports work
   python -c "import module_name"
   ```

3. **Run Existing Tests**
   ```bash
   # Run tests if they exist
   pytest tests/ || npm test || echo "No tests found"
   ```

4. **Application Start Check**
   ```bash
   # Ensure application still starts
   ./dev.sh restart || docker-compose up || npm start
   ```

## 🔍 Pattern Detection

### For Python/FastAPI Projects

Look for:
```python
# Router patterns
router = APIRouter(prefix="/api/v1/resource")

# Service patterns
class ResourceService:
    def __init__(self, repository: ResourceRepository):

# Repository patterns
class ResourceRepository:
    def __init__(self, session: Session):
```

Maintain these EXACTLY.

### For JavaScript/TypeScript Projects

Look for:
```javascript
// Component patterns
export const ComponentName = () => {

// Service patterns
export class ServiceName {

// API patterns
export const fetchResource = async () => {
```

### For Database Operations

Identify and maintain:
- ORM usage (SQLAlchemy/Prisma/TypeORM)
- Query patterns
- Transaction handling
- Migration approach

## 📝 Communication Template

When starting iteration:

```markdown
## 📊 Project Analysis Complete

### Current Architecture:
- Type: [identified architecture]
- Key patterns: [patterns found]
- Conventions: [naming, structure]

### Modification Scope:
- Files to modify: X
- Lines affected: ~Y
- Risk level: [Low/Medium/High]

### Compliance Check:
- ✅ Will follow existing patterns
- ✅ No new dependencies needed
- ✅ Maintains current architecture

Proceeding with modifications...
```

## 🚨 Warning Triggers

STOP and ask for confirmation if:
1. Modification requires architectural change
2. Need to add new dependency
3. Pattern doesn't exist for needed feature
4. Tests are failing after changes
5. Import errors occur

## 💡 Example Scenarios

### Scenario 1: Adding a new field to existing model

**Right approach:**
1. Check how other fields are defined
2. Match exact pattern (decorators, types, validation)
3. Update related schemas/DTOs if they exist
4. Update tests if they exist

**Wrong approach:**
- Introducing new validation library
- Changing field naming convention
- Reorganizing model file

### Scenario 2: Adding new endpoint to existing router

**Right approach:**
1. Study existing endpoints in same router
2. Match URL pattern, authentication, error handling
3. Use same response format
4. Follow existing documentation pattern

**Wrong approach:**
- Creating new router file
- Introducing different auth mechanism
- Using different response structure

## 🎯 Success Metrics

Task is successful when:
- ✅ All modifications follow existing patterns
- ✅ No architectural changes made
- ✅ Application runs without errors
- ✅ Existing tests still pass
- ✅ Code looks like it was written by same team
- ✅ No "improvements" beyond requested changes

## 🔄 Continuous Verification

Throughout the task:
1. After EACH file modification → verify imports
2. After EACH feature addition → test functionality
3. Before marking complete → run full validation

## 📚 Required Reading

Always read these files first if they exist:
1. `CLAUDE.md` or `AI_INSTRUCTIONS.md`
2. `README.md`
3. `CONTRIBUTING.md`
4. Architecture documentation in `docs/`
5. Existing test files

## 🛑 Final Checklist

Before completing:
- [ ] All changes follow existing patterns
- [ ] No new patterns introduced
- [ ] No unnecessary changes made
- [ ] Application starts successfully
- [ ] No new dependencies added
- [ ] Code style matches existing code
- [ ] Tests updated (if they exist)
- [ ] Documentation updated (if needed)