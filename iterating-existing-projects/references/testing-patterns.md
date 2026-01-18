# Testing Patterns for Project Iteration

## Core Testing Principles

1. **Match existing test style exactly**
2. **Maintain same test coverage level**
3. **Follow established test file organization**
4. **Use same assertion patterns**

## Test File Organization Patterns

### 1. Colocated Tests

**Pattern**: Tests next to source files

```
src/
├── components/
│   ├── Button.js
│   ├── Button.test.js     # Test next to source
│   ├── Input.js
│   └── Input.test.js
```

**Your iteration must**:
- Place test files next to source files
- Use same naming convention (`.test.js` or `.spec.js`)

### 2. Separate Test Directory

**Pattern**: Tests in dedicated directory

```
project/
├── src/
│   └── components/
│       └── Button.js
└── tests/
    └── components/
        └── Button.test.js  # Mirror structure
```

**Your iteration must**:
- Mirror source structure in test directory
- Maintain same path relationships

### 3. Integration Test Structure

**Pattern**: Feature-based test organization

```
tests/
├── unit/
│   └── components/
├── integration/
│   └── features/
└── e2e/
    └── scenarios/
```

## Test Framework Patterns

### 1. Jest Patterns

**Existing pattern**:
```javascript
// Group related tests
describe('UserService', () => {
  // Setup and teardown
  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  // Nested describes for methods
  describe('getUser', () => {
    it('should return user when exists', async () => {
      const user = await userService.getUser('123');
      expect(user).toMatchSnapshot();
    });

    it('should throw when user not found', async () => {
      await expect(userService.getUser('invalid'))
        .rejects.toThrow('User not found');
    });
  });
});
```

**Your iteration pattern**:
```javascript
// Follow EXACT same structure
describe('ProductService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  describe('getProduct', () => {
    it('should return product when exists', async () => {
      const product = await productService.getProduct('456');
      expect(product).toMatchSnapshot();
    });

    it('should throw when product not found', async () => {
      await expect(productService.getProduct('invalid'))
        .rejects.toThrow('Product not found');
    });
  });
});
```

### 2. Mocha/Chai Patterns

**Existing pattern**:
```javascript
const { expect } = require('chai');
const sinon = require('sinon');

describe('AuthController', function() {
  let sandbox;

  beforeEach(function() {
    sandbox = sinon.createSandbox();
  });

  afterEach(function() {
    sandbox.restore();
  });

  context('when user is authenticated', function() {
    it('should return user data', async function() {
      const result = await authController.getProfile(mockReq, mockRes);
      expect(result).to.have.property('id');
      expect(result.email).to.equal('test@example.com');
    });
  });
});
```

**Your iteration pattern**:
```javascript
// Match Mocha style exactly
describe('PaymentController', function() {
  let sandbox;

  beforeEach(function() {
    sandbox = sinon.createSandbox();
  });

  afterEach(function() {
    sandbox.restore();
  });

  context('when payment is valid', function() {
    it('should process payment', async function() {
      const result = await paymentController.process(mockReq, mockRes);
      expect(result).to.have.property('transactionId');
      expect(result.status).to.equal('success');
    });
  });
});
```

## Mock and Stub Patterns

### 1. Jest Mocking

**Existing pattern**:
```javascript
// Manual mock in __mocks__
jest.mock('../api/client');

// Inline mock
jest.mock('../config', () => ({
  apiUrl: 'http://test.api',
  timeout: 1000
}));

// Spy pattern
const fetchSpy = jest.spyOn(api, 'fetch');
fetchSpy.mockResolvedValue({ data: 'test' });
```

**Your iteration must use same approach**:
```javascript
// If project uses __mocks__, create one
jest.mock('../new-api/client');

// Match inline mock style
jest.mock('../new-config', () => ({
  serviceUrl: 'http://test.service',
  retries: 3
}));

// Match spy pattern
const sendSpy = jest.spyOn(newApi, 'send');
sendSpy.mockResolvedValue({ data: 'test' });
```

### 2. Sinon Patterns

**Existing pattern**:
```javascript
// Stub pattern
const fetchStub = sandbox.stub(apiClient, 'fetch');
fetchStub.withArgs('users').returns(Promise.resolve(users));

// Spy pattern
const saveSpy = sandbox.spy(database, 'save');

// Mock with expectations
const mock = sandbox.mock(service);
mock.expects('process').once().withArgs(data);
```

**Your iteration pattern**:
```javascript
// Match stubbing style
const sendStub = sandbox.stub(newClient, 'send');
sendStub.withArgs('products').returns(Promise.resolve(products));

// Match spy usage
const updateSpy = sandbox.spy(database, 'update');

// Match mock expectations
const mock = sandbox.mock(newService);
mock.expects('handle').once().withArgs(newData);
```

## Assertion Patterns

### 1. Snapshot Testing

**If project uses snapshots**:
```javascript
// Existing pattern
expect(component).toMatchSnapshot();
expect(api.transformResponse(data)).toMatchSnapshot('response-transform');
```

**Your iteration**:
```javascript
// Also use snapshots
expect(newComponent).toMatchSnapshot();
expect(newApi.transformData(data)).toMatchSnapshot('data-transform');
```

### 2. Custom Matchers

**If project has custom matchers**:
```javascript
// Project's custom matcher
expect.extend({
  toBeValidUser(received) {
    const pass = received.id && received.email;
    return { pass, message: () => 'Expected valid user' };
  }
});
```

**Create similar for your feature**:
```javascript
expect.extend({
  toBeValidProduct(received) {
    const pass = received.id && received.price >= 0;
    return { pass, message: () => 'Expected valid product' };
  }
});
```

## React Testing Patterns

### 1. Testing Library Pattern

**Existing pattern**:
```javascript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form with data', async () => {
  const handleSubmit = jest.fn();
  render(<Form onSubmit={handleSubmit} />);

  await userEvent.type(screen.getByLabelText('Name'), 'John');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));

  await waitFor(() => {
    expect(handleSubmit).toHaveBeenCalledWith({ name: 'John' });
  });
});
```

**Your iteration pattern**:
```javascript
// Match testing approach exactly
test('creates new item', async () => {
  const handleCreate = jest.fn();
  render(<CreateForm onCreate={handleCreate} />);

  await userEvent.type(screen.getByLabelText('Title'), 'New Item');
  await userEvent.click(screen.getByRole('button', { name: 'Create' }));

  await waitFor(() => {
    expect(handleCreate).toHaveBeenCalledWith({ title: 'New Item' });
  });
});
```

### 2. Enzyme Pattern (if used)

**Existing pattern**:
```javascript
import { shallow, mount } from 'enzyme';

describe('Component', () => {
  it('renders correctly', () => {
    const wrapper = shallow(<Component prop="value" />);
    expect(wrapper.find('.className')).toHaveLength(1);
    expect(wrapper.prop('data-id')).toBe('123');
  });
});
```

**Your iteration pattern**:
```javascript
// Match Enzyme usage
describe('NewComponent', () => {
  it('renders correctly', () => {
    const wrapper = shallow(<NewComponent prop="value" />);
    expect(wrapper.find('.newClass')).toHaveLength(1);
    expect(wrapper.prop('data-type')).toBe('new');
  });
});
```

## API Testing Patterns

### 1. Supertest Pattern

**Existing pattern**:
```javascript
const request = require('supertest');
const app = require('../app');

describe('GET /api/users', () => {
  it('responds with json', async () => {
    const response = await request(app)
      .get('/api/users')
      .set('Authorization', 'Bearer token')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(response.body).toHaveProperty('users');
  });
});
```

**Your iteration pattern**:
```javascript
describe('GET /api/products', () => {
  it('responds with json', async () => {
    const response = await request(app)
      .get('/api/products')
      .set('Authorization', 'Bearer token')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(response.body).toHaveProperty('products');
  });
});
```

## Test Data Patterns

### 1. Fixtures

**If project uses fixtures**:
```javascript
// fixtures/users.js
module.exports = {
  validUser: {
    id: '123',
    name: 'Test User',
    email: 'test@example.com'
  },
  invalidUser: {
    name: '',
    email: 'invalid'
  }
};
```

**Create similar fixtures**:
```javascript
// fixtures/products.js
module.exports = {
  validProduct: {
    id: '456',
    name: 'Test Product',
    price: 99.99
  },
  invalidProduct: {
    name: '',
    price: -1
  }
};
```

### 2. Factory Pattern

**If project uses factories**:
```javascript
// factories/userFactory.js
const createUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  name: faker.name.fullName(),
  email: faker.internet.email(),
  ...overrides
});
```

**Create similar factory**:
```javascript
// factories/productFactory.js
const createProduct = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  name: faker.commerce.productName(),
  price: faker.commerce.price(),
  ...overrides
});
```

## Coverage Patterns

### 1. Coverage Requirements

Check existing coverage:
```bash
# Look for coverage config
cat package.json | grep -A5 "jest"
cat .nycrc
cat jest.config.js
```

**Match coverage thresholds**:
```javascript
// If project requires 80% coverage
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

### 2. Coverage Exclusions

**Check what's excluded**:
```javascript
// jest.config.js
coveragePathIgnorePatterns: [
  '/node_modules/',
  '/test/',
  '.stories.js'
]
```

**Follow same exclusions for new code**