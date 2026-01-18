# Migration Strategies for Safe Project Iteration

## Core Principles

1. **Never break existing functionality**
2. **Always provide backwards compatibility**
3. **Migrate incrementally, not all at once**
4. **Test each step before proceeding**

## Database Migration Strategies

### 1. Expand-Contract Pattern

When modifying database schema:

**Phase 1: Expand**
```sql
-- Add new column alongside old
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Copy data
UPDATE users SET email_address = email;
```

**Phase 2: Migrate**
```javascript
// Update application to use new column
const user = {
  // Old: email: row.email
  email: row.email_address || row.email, // Support both
};
```

**Phase 3: Contract**
```sql
-- After all code updated and deployed
ALTER TABLE users DROP COLUMN email;
```

### 2. Parallel Run Pattern

Run old and new systems in parallel:

```javascript
class PaymentService {
  async processPayment(data) {
    // Run both systems
    const [oldResult, newResult] = await Promise.all([
      this.oldPaymentSystem.process(data),
      this.newPaymentSystem.process(data)
    ]);

    // Compare results
    if (oldResult.amount !== newResult.amount) {
      logger.error('Payment mismatch', { oldResult, newResult });
    }

    // Use old system as source of truth initially
    return oldResult;
  }
}
```

## API Migration Strategies

### 1. Versioning Strategy

**Add version to existing API**:
```javascript
// Old endpoint (maintain)
app.get('/api/users', getUsersV1);

// New endpoint
app.get('/api/v2/users', getUsersV2);

// Redirect with deprecation notice
app.get('/api/users', (req, res) => {
  res.header('X-API-Deprecation-Warning', 'Please migrate to /api/v2/users');
  return getUsersV1(req, res);
});
```

### 2. Field Evolution Pattern

**Adding fields**:
```javascript
// Safe: Adding optional field
const userSchema = {
  id: required(),
  name: required(),
  email: required(),
  phone: optional(), // NEW: Safe to add
};
```

**Removing fields**:
```javascript
// Step 1: Mark as deprecated
const response = {
  id: user.id,
  name: user.name,
  email: user.email,
  phone: user.phone, // @deprecated Use contactNumber instead
  contactNumber: user.phone, // New field
};

// Step 2: After migration period, remove old field
```

## Code Refactoring Strategies

### 1. Strangler Fig Pattern

Gradually replace legacy system:

```javascript
class UserService {
  async getUser(id) {
    // Feature flag to control rollout
    if (featureFlags.useNewUserService) {
      try {
        return await this.newUserService.getUser(id);
      } catch (error) {
        logger.error('New service failed, falling back', error);
        return await this.legacyUserService.getUser(id);
      }
    }
    return await this.legacyUserService.getUser(id);
  }
}
```

### 2. Branch by Abstraction

**Step 1: Create abstraction**:
```javascript
// Create interface
class PaymentProcessor {
  async process(payment) {
    throw new Error('Must implement process method');
  }
}

// Wrap existing implementation
class LegacyPaymentProcessor extends PaymentProcessor {
  async process(payment) {
    return legacyPaymentAPI.submit(payment);
  }
}
```

**Step 2: Use abstraction everywhere**:
```javascript
// Replace direct calls
// OLD: legacyPaymentAPI.submit(payment)
// NEW:
const processor = new LegacyPaymentProcessor();
await processor.process(payment);
```

**Step 3: Swap implementation**:
```javascript
class ModernPaymentProcessor extends PaymentProcessor {
  async process(payment) {
    return modernPaymentAPI.process(payment);
  }
}

// Just change instantiation
const processor = new ModernPaymentProcessor();
```

## State Migration Strategies

### 1. Redux State Migration

**Migrating state shape**:
```javascript
// Migration middleware
const stateMigration = store => next => action => {
  if (action.type === 'PERSIST/REHYDRATE') {
    const state = action.payload;

    // Migrate v1 to v2
    if (state && state._version === 1) {
      action.payload = {
        ...state,
        _version: 2,
        // Transform old structure to new
        users: state.userList ? {
          byId: state.userList.reduce((acc, user) => ({
            ...acc,
            [user.id]: user
          }), {}),
          allIds: state.userList.map(u => u.id)
        } : { byId: {}, allIds: [] }
      };
      delete action.payload.userList;
    }
  }
  return next(action);
};
```

### 2. Local Storage Migration

```javascript
class StorageManager {
  static migrate() {
    const version = localStorage.getItem('schema_version') || '1';

    switch(version) {
      case '1':
        this.migrateV1toV2();
        // fall through
      case '2':
        this.migrateV2toV3();
        // fall through
      case '3':
        // Current version
        break;
    }

    localStorage.setItem('schema_version', '3');
  }

  static migrateV1toV2() {
    const oldData = localStorage.getItem('user_preferences');
    if (oldData) {
      const parsed = JSON.parse(oldData);
      const newFormat = {
        theme: parsed.darkMode ? 'dark' : 'light',
        ...parsed
      };
      delete newFormat.darkMode;
      localStorage.setItem('user_preferences', JSON.stringify(newFormat));
    }
  }
}
```

## Dependency Migration Strategies

### 1. Adapter Pattern

When replacing libraries:

```javascript
// Adapter for old library API
class MomentAdapter {
  constructor(date) {
    this.dayjs = dayjs(date);
  }

  format(pattern) {
    // Map moment patterns to dayjs
    const dayjsPattern = pattern
      .replace('YYYY', 'YYYY')
      .replace('DD', 'DD')
      .replace('MM', 'MM');
    return this.dayjs.format(dayjsPattern);
  }

  add(amount, unit) {
    this.dayjs = this.dayjs.add(amount, unit);
    return this;
  }
}

// Global replacement
if (typeof window !== 'undefined') {
  window.moment = (date) => new MomentAdapter(date);
}
```

### 2. Gradual Dependency Update

```javascript
// package.json
{
  "dependencies": {
    "lodash": "^3.10.0",      // Old version
    "lodash-es": "^4.17.0"    // New version with different name
  }
}

// Gradual migration
import { debounce as debounceV3 } from 'lodash';
import { debounce as debounceV4 } from 'lodash-es';

// Use based on feature flag
const debounce = featureFlags.useLodashV4 ? debounceV4 : debounceV3;
```

## Testing During Migration

### 1. Parallel Testing

```javascript
describe('User Service Migration', () => {
  it('should return same results from old and new implementation', async () => {
    const testUsers = generateTestUsers(100);

    for (const user of testUsers) {
      const oldResult = await oldUserService.process(user);
      const newResult = await newUserService.process(user);

      expect(newResult).toEqual(oldResult);
    }
  });
});
```

### 2. Contract Testing

```javascript
// Define contract
const userContract = {
  id: expect.any(String),
  name: expect.any(String),
  email: expect.stringMatching(/^\S+@\S+$/),
  createdAt: expect.any(Date)
};

// Test both implementations
describe('User API Contract', () => {
  test.each([
    ['Legacy API', legacyAPI],
    ['New API', newAPI]
  ])('%s should match contract', async (name, api) => {
    const result = await api.getUser('123');
    expect(result).toMatchObject(userContract);
  });
});
```

## Rollback Strategies

### 1. Feature Flag Rollback

```javascript
class FeatureManager {
  static async revertFeature(featureName) {
    // Log the rollback
    logger.warn(`Rolling back feature: ${featureName}`);

    // Disable feature flag
    await featureFlags.disable(featureName);

    // Clear any cached data
    await cache.clear(`feature:${featureName}:*`);

    // Notify monitoring
    await metrics.increment('feature.rollback', { feature: featureName });
  }
}
```

### 2. Database Rollback

```javascript
// Keep rollback scripts ready
class MigrationManager {
  async rollback(version) {
    const rollbackScripts = {
      'v2.0.0': async () => {
        await db.query('ALTER TABLE users DROP COLUMN IF EXISTS new_field');
        await db.query('UPDATE schema_version SET version = "1.9.0"');
      },
      'v1.9.0': async () => {
        // Previous rollback
      }
    };

    if (rollbackScripts[version]) {
      await rollbackScripts[version]();
      logger.info(`Rolled back to ${version}`);
    }
  }
}
```

## Monitoring During Migration

### 1. Dual Metrics

```javascript
class MigrationMonitor {
  static trackPerformance(operation, version) {
    const startTime = Date.now();

    return {
      complete: (success = true) => {
        const duration = Date.now() - startTime;
        metrics.histogram('migration.performance', duration, {
          operation,
          version,
          success
        });

        // Alert if new version is slower
        if (version === 'new' && duration > this.oldVersionBaseline * 1.2) {
          alerting.warn('New version performance degradation', {
            operation,
            duration,
            baseline: this.oldVersionBaseline
          });
        }
      }
    };
  }
}
```

### 2. Error Rate Monitoring

```javascript
class ErrorMonitor {
  static async checkMigrationHealth(featureName) {
    const oldErrors = await metrics.getErrorRate(`${featureName}.old`);
    const newErrors = await metrics.getErrorRate(`${featureName}.new`);

    if (newErrors > oldErrors * 1.5) {
      logger.error('High error rate in new implementation', {
        feature: featureName,
        oldRate: oldErrors,
        newRate: newErrors
      });

      // Auto-rollback if configured
      if (config.autoRollback) {
        await FeatureManager.revertFeature(featureName);
      }
    }
  }
}
```