# Example task analysis output
# This shows what the system generates for a complex task

## Original Task
"Build a full-stack e-commerce web application with user authentication, product catalog, shopping cart, and payment processing"

## Generated Subtasks

### 1. Setup Development Environment ⚙️
- **Priority:** High
- **Complexity:** Simple  
- **Time:** 4 hours
- **Description:** Configure development tools, IDE, version control, and project structure

### 2. Design System Architecture 🏗️
- **Priority:** High
- **Complexity:** Complex
- **Time:** 1-2 days
- **Dependencies:** Setup Development Environment
- **Description:** Plan database schema, API structure, frontend architecture, and deployment strategy

### 3. Implement User Authentication 🔐
- **Priority:** High
- **Complexity:** Moderate
- **Time:** 3-4 days
- **Dependencies:** Design System Architecture
- **Description:** Build user registration, login, password reset, and session management

### 4. Build Product Catalog System 📦
- **Priority:** High
- **Complexity:** Complex
- **Time:** 5-7 days
- **Dependencies:** Design System Architecture, User Authentication
- **Description:** Create product models, admin interface, search/filter functionality, and product detail pages

### 5. Develop Shopping Cart & Checkout 🛒
- **Priority:** High
- **Complexity:** Complex
- **Time:** 4-6 days
- **Dependencies:** Product Catalog System, User Authentication
- **Description:** Implement cart functionality, checkout process, and order management

### 6. Integrate Payment Processing 💳
- **Priority:** High
- **Complexity:** Very Complex
- **Time:** 3-5 days
- **Dependencies:** Shopping Cart & Checkout
- **Description:** Integrate payment gateway (Stripe/PayPal), handle transactions, and implement security measures

### 7. Testing & Quality Assurance 🧪
- **Priority:** Medium
- **Complexity:** Moderate
- **Time:** 3-4 days
- **Dependencies:** All previous tasks
- **Description:** Write unit tests, integration tests, and perform user acceptance testing

## Code Organization Recommendations

### File Structure
```
e-commerce-app/
├── backend/
│   ├── src/
│   │   ├── models/          # Data models
│   │   ├── controllers/     # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── middleware/      # Authentication, validation
│   │   └── utils/           # Helper functions
│   ├── tests/
│   └── config/
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API calls
│   │   ├── utils/           # Helper functions
│   │   └── styles/          # CSS/styling
│   └── public/
└── docs/                    # Documentation
```

### Recommended Technologies
- **Backend:** Node.js/Express or Python/FastAPI
- **Frontend:** React or Vue.js
- **Database:** PostgreSQL or MongoDB
- **Authentication:** JWT tokens
- **Payment:** Stripe or PayPal SDK
- **Testing:** Jest, Cypress
- **Deployment:** Docker, AWS/Vercel
