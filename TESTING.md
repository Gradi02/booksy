"""
Running the Test Suite
======================

## Backend Tests (pytest)

Prerequisites:
- Python 3.8+
- pytest and httpx installed (see requirements.txt)

Running tests:
```bash
cd backend
pip install -r requirements.txt
pytest tests/test_critical_logic.py -v

# Run specific test class
pytest tests/test_critical_logic.py::TestDeviceRentalLogic -v

# Run specific test
pytest tests/test_critical_logic.py::TestDeviceRentalLogic::test_user_can_rent_available_device -v

# With coverage report
pytest tests/test_critical_logic.py --cov=. --cov-report=html
```

Test Structure:
- conftest.py: Fixtures for database, users, tokens, devices
- test_critical_logic.py: 25+ tests across 5 test classes

Test Coverage:
- ✅ Device rental business logic (success/fail/race conditions)
- ✅ Authentication (401 responses)
- ✅ Authorization (403 responses)
- ✅ User management (creation, updates, duplicates)
- ✅ Transaction safety (concurrent operations)
- ✅ Error handling (404, 409, 500)


## Frontend Tests (vitest)

Prerequisites:
- Node.js 16+
- npm dependencies installed (see package.json)

Installing dependencies:
```bash
cd frontend
npm install
```

Running tests:
```bash
# Run all tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage report
npm run test:coverage

# Run specific test file
npm run test App.spec.js

# Watch mode (rerun on file changes)
npm run test -- --watch
```

Test Structure:
- vitest.config.js: Environment setup
- App.spec.js: 15+ tests for UI logic and API interactions
- structure.spec.js: Test suite validation

Test Coverage:
- ✅ Device rental UI state (button visibility)
- ✅ Rent action triggers (API calls)
- ✅ Role-based visibility (admin only controls)
- ✅ Session persistence (localStorage)
- ✅ Error handling (rent failures, API errors)


## Key Test Scenarios

### Backend - Critical Business Logic

1. User Rental Flow
   - Regular user CANNOT change device status (403)
   - Admin user CAN change device to "In Use" (200)
   - Cannot rent "Repair" or "In Use" devices
   - Race condition: Two admins cannot rent same device twice

2. Authentication
   - Missing token → 401
   - Invalid token → 401
   - Expired token → 401

3. Authorization
   - Regular user on admin endpoint → 403
   - Admin on any endpoint → Success

4. User Management
   - Cannot create duplicate username (409)
   - Cannot update to duplicate username (409)
   - Admin can change other users' admin status
   - Users cannot delete their own account (400)

5. Transaction Safety
   - Concurrent device updates serialize
   - Concurrent user creation with same username fails atomically
   - Database state stays consistent after failed operations

### Frontend - Critical UI Logic

1. Device Status Display
   - Repair status → Rent button hidden
   - In Use status → Rent button hidden
   - Available status → Rent button visible

2. Rent Action
   - Clicking rent → PUT /devices/{id} with status="In Use"
   - Rent failure → Error message displayed
   - Rent success → UI updates to show device as rented

3. Role-Based UI
   - Admin sees "Mark as Repaired" button
   - Regular user doesn't see "Mark as Repaired" button
   - Admin sees "Users" menu
   - Regular user doesn't see "Users" menu

4. Session Persistence
   - Token saved to localStorage after login
   - Token restored on page reload
   - Logout clears localStorage
   - Invalid session token clears auth state


## Mocking Strategy

### Frontend
- global.fetch mocked using vi.fn()
- No actual HTTP requests made during tests
- All API responses are controlled
- Enables testing without backend server


## CI/CD Integration

These tests can be integrated into GitHub Actions:
```yaml
- name: Run Backend Tests
  run: cd backend && pytest tests/ -v

- name: Run Frontend Tests
  run: cd frontend && npm run test
```

## Notes

- Backend tests use in-memory SQLite for speed (no file I/O)
- Frontend tests use happy-dom for lightweight DOM simulation
- All fixtures are isolated per test (transaction rollback)
- Tests are independent - can run in any order
