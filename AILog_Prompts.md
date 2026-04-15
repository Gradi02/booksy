# AILog - Prompt History

## Prompt 1: Initial Fullstack Setup

Create a fullstack application with the following setup:

Architecture:
- monorepo with /backend and /frontend folders

Backend:
- Python with FastAPI
- SQLite database using SQLAlchemy
- include models based on seed.json structure
- CRUD endpoints for one main entity (based on seed data)
- JWT authentication using OAuth2 password flow (FastAPI standard)
- create a default admin user:
  - username: admin
  - password: admin123

Database:
- initialize SQLite DB on startup
- load data from backend/seed.json automatically

Frontend:
- Vue 3 with Vite
- simple table view displaying all records from backend
- basic login form (JWT auth)
- no styling needed, focus on functionality

AILog:
- create a file AILog.md in root
- include:
  - section "Prompt History"
  - section "AI Generated Code Notes"
  - section "Audit" (empty placeholder)
- this is a static file, not part of app logic

General:
- keep it minimal and runnable
- include instructions to run both frontend and backend



## Prompt 2: Fixing Initial Fullstack Setup and Adding missing files

- Add a .gitignore file to this project
- Make @AILog.md cleaner - dont change the content of it but divide it into 2 files so first can hold full prompts history and second one will have only short notes and audit with links to the first prompts file.
- Investigate why backend is not launching and telling that "ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])"



## Prompt 3: Fix Frontend CORS Error

when loging, it throws "POST http://127.0.0.1:8000/token net::ERR_FAILED 200 (OK)
login	@	App.vue:20" but post methog of loging in backend seems good "http 200".



## Prompt 4: Full CRUD, Backend Restructuring, Smart Dashboard, and Status Enum

Requirements:
- Add full CRUD for hardware management: Add new items, delete old ones, and toggle the "Repair" status
- Make file structure in backend cleaner and separate login and devices logic (preparing for users managing and Docker)
- Smart Dashboard: A list of hardware showing Name, Brand, Purchase Date, and Status (Available, In Use, Repair -> via enum). Must support sorting and filtering.
- Update AILog.md and AILog prompts history



## Prompt 5: prompt prepared with chatGPT to provide a visuals similar to wireframe.

Build a responsive frontend layout based on the provided screenshot of a “Hardware Manager” dashboard.

General Requirements:

* Use modern UI practices (clean spacing, soft shadows, rounded corners).
* Use a component-based approach (React preferred, but plain HTML/CSS is acceptable if not specified).
* Style with Tailwind CSS (preferred) or clean CSS.
* The layout should be responsive (desktop-first, but adaptable to smaller screens).

Layout Structure:

1. Sidebar (Left)

* Fixed vertical sidebar
* Contains:

  * Title: Hardware Manager (with icon)
  * Navigation items:

    * Hardware List (active state)
    * My Rentals
    * Admin Panel
  * Bottom section:

    * Logout button (with red accent)
* Sidebar should have:

  * Light background
  * Active item highlighted with subtle background
  * Icons next to each menu item

2. Main Content Area

Header:

* Page title: Hardware List
* Search bar:

  * Placeholder: “Ask AI…”
  * Rounded input with subtle border
  * Icon inside input (left)
  * Small sparkle icon on the right

Table / List:

* Create a card-style container with a table inside.

Columns:

* Device Name
* Brand
* Date Added
* Status
* Action

Table Details:

Each row should include:

* Device name (e.g., "MacBook Pro 16”)
* Brand (Apple, Dell, etc.)
* Date (YYYY-MM-DD format)
* Status badge:

  * Available → dark badge
  * Rented → gray badge
  * In Repair → red badge
* Action button:

  * "Rent" button
  * Disabled (grayed out) if not available

Styling Guidelines:

* Use rounded corners (lg or xl)
* Subtle shadows for containers
* Consistent spacing (padding/margin)
* Badge styles:

  * Pill-shaped
  * Small font
* Buttons:

  * Rounded
  * Dark primary for active
  * Gray for disabled

Bonus (optional):

* Add hover states for rows and buttons
* Add basic state handling (e.g., disabled Rent button when status ≠ Available)

Deliverables:

* Clean, readable code
* Reusable components (Sidebar, Table, Badge, Button)
* Ready to plug into an existing frontend



## Prompt 6:
I would like to deplot this project in vercel (frontend) and render (backend). Because of render not stable container I will need an auto healing system - if backend is waking up, setup default seeded database based on seed.json. The rest of tech stack dont need any changes I think. Tell me more about current situation and what I will need to do to aim this purpose?
### and 
prepare the project for deploy based on previous answer.
