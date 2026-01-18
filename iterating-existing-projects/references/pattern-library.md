# Pattern Library for Project Iteration

## Architectural Patterns

### 1. MVC (Model-View-Controller)

**Structure**:
```
src/
├── models/
│   ├── User.js
│   └── Product.js
├── views/
│   ├── UserView.js
│   └── ProductView.js
└── controllers/
    ├── UserController.js
    └── ProductController.js
```

**Iteration Rules**:
- New models go in `models/`
- Controllers handle business logic
- Views handle presentation
- Never mix concerns

### 2. Clean Architecture

**Structure**:
```
src/
├── domain/
│   ├── entities/
│   └── value-objects/
├── application/
│   ├── use-cases/
│   └── services/
├── infrastructure/
│   ├── repositories/
│   └── external-services/
└── presentation/
    ├── controllers/
    └── views/
```

**Iteration Rules**:
- Domain layer has no dependencies
- Application orchestrates domain
- Infrastructure implements interfaces
- Dependency flow: Presentation → Application → Domain

### 3. Component-Based (React/Vue)

**Structure**:
```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── Button.module.css
│   │   └── Input/
│   └── features/
│       ├── UserProfile/
│       └── ProductList/
├── hooks/
├── utils/
└── services/
```

**Iteration Rules**:
- Each component in its own folder
- Co-locate tests and styles
- Shared components in `common/`
- Feature-specific in `features/`

## Code Style Patterns

### 1. Functional Programming Style

**Original Pattern**:
```javascript
// Immutable operations
const addItem = (list, item) => [...list, item];
const removeItem = (list, id) => list.filter(item => item.id !== id);

// Composition
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);
```

**Your Iteration Must Follow**:
```javascript
// Same immutable pattern
const updateItem = (list, id, updates) =>
  list.map(item => item.id === id ? {...item, ...updates} : item);

// Same composition style
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);
```

### 2. Object-Oriented Style

**Original Pattern**:
```python
class Repository:
    def __init__(self, db):
        self._db = db

    def find_by_id(self, id: str):
        return self._db.query(...)

    def save(self, entity):
        return self._db.persist(...)
```

**Your Iteration Must Follow**:
```python
class UserRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def find_by_email(self, email: str):
        return self._db.query(...)

    def find_active_users(self):
        return self._db.query(...)
```

## State Management Patterns

### 1. Redux Pattern

**Original Pattern**:
```javascript
// Action types
const ADD_TODO = 'ADD_TODO';

// Action creators
const addTodo = (text) => ({
  type: ADD_TODO,
  payload: { text }
});

// Reducer
const todosReducer = (state = [], action) => {
  switch (action.type) {
    case ADD_TODO:
      return [...state, action.payload];
    default:
      return state;
  }
};
```

**Your Iteration Must Follow**:
```javascript
// Same pattern for new feature
const UPDATE_TODO = 'UPDATE_TODO';

const updateTodo = (id, updates) => ({
  type: UPDATE_TODO,
  payload: { id, updates }
});

// Extend existing reducer
case UPDATE_TODO:
  return state.map(todo =>
    todo.id === action.payload.id
      ? {...todo, ...action.payload.updates}
      : todo
  );
```

### 2. React Context Pattern

**Original Pattern**:
```javascript
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
```

**Your Iteration Must Follow**:
```javascript
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

## Testing Patterns

### 1. Jest/React Testing Library

**Original Pattern**:
```javascript
describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

**Your Iteration Must Follow**:
```javascript
describe('Input', () => {
  it('should render with placeholder', () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('should call onChange when typed', () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'test' } });
    expect(handleChange).toHaveBeenCalled();
  });
});
```

### 2. Pytest Pattern

**Original Pattern**:
```python
import pytest
from app.models import User

class TestUser:
    @pytest.fixture
    def user(self):
        return User(name="Test User", email="test@example.com")

    def test_user_creation(self, user):
        assert user.name == "Test User"
        assert user.email == "test@example.com"

    def test_user_validation(self):
        with pytest.raises(ValueError):
            User(name="", email="invalid")
```

**Your Iteration Must Follow**:
```python
import pytest
from app.models import Product

class TestProduct:
    @pytest.fixture
    def product(self):
        return Product(name="Test Product", price=99.99)

    def test_product_creation(self, product):
        assert product.name == "Test Product"
        assert product.price == 99.99

    def test_product_validation(self):
        with pytest.raises(ValueError):
            Product(name="", price=-10)
```

## API Design Patterns

### 1. RESTful Pattern

**Original Pattern**:
```javascript
// Express.js routes
router.get('/users', getAllUsers);
router.get('/users/:id', getUserById);
router.post('/users', createUser);
router.put('/users/:id', updateUser);
router.delete('/users/:id', deleteUser);
```

**Your Iteration Must Follow**:
```javascript
// Same RESTful pattern
router.get('/products', getAllProducts);
router.get('/products/:id', getProductById);
router.post('/products', createProduct);
router.put('/products/:id', updateProduct);
router.delete('/products/:id', deleteProduct);
```

### 2. GraphQL Pattern

**Original Pattern**:
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}
```

**Your Iteration Must Follow**:
```graphql
type Product {
  id: ID!
  name: String!
  price: Float!
  reviews: [Review!]!
}

type Query {
  product(id: ID!): Product
  products(limit: Int, offset: Int): [Product!]!
}

type Mutation {
  createProduct(input: CreateProductInput!): Product!
  updateProduct(id: ID!, input: UpdateProductInput!): Product!
}
```

## Database Patterns

### 1. Repository Pattern

**Original Pattern**:
```typescript
interface Repository<T> {
  find(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(entity: T): Promise<T>;
  update(id: string, entity: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  async find(id: string): Promise<User | null> {
    const result = await db.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0] || null;
  }
  // ... other methods
}
```

**Your Iteration Must Follow**:
```typescript
class ProductRepository implements Repository<Product> {
  async find(id: string): Promise<Product | null> {
    const result = await db.query('SELECT * FROM products WHERE id = $1', [id]);
    return result.rows[0] || null;
  }
  // ... other methods following same pattern
}
```

### 2. Active Record Pattern

**Original Pattern**:
```ruby
class User < ApplicationRecord
  validates :email, presence: true, uniqueness: true
  has_many :posts

  def full_name
    "#{first_name} #{last_name}"
  end

  scope :active, -> { where(active: true) }
end
```

**Your Iteration Must Follow**:
```ruby
class Product < ApplicationRecord
  validates :name, presence: true
  has_many :reviews

  def display_price
    "$#{price}"
  end

  scope :available, -> { where(available: true) }
end
```