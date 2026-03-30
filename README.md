# Bonnyrigg Pizza Blog - Flask Project

This is a complete **Flask pizza blog website** designed to align closely with the uploaded Bonnyrigg High School HSC Software Engineering marking criteria. It includes:

- responsive homepage with featured recipes
- recipe pages with images, ingredients and instructions
- search and filter system
- user registration and login
- secure password hashing
- comment system
- admin dashboard for recipe management
- SQLite database
- input validation and error handling
- modular code structure with comments
- test file and supporting documentation

This project was created to reflect the requirements in the assessment notification, including recipe publishing, community interaction, performance, security, SQLite use, and a clean mobile-responsive layout. fileciteturn0file0L1-L999

## 1. Project Structure

```text
pizza_blog/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── recipes.html
│       ├── recipe_detail.html
│       ├── login.html
│       ├── register.html
│       ├── admin.html
│       └── error.html
├── docs/
│   ├── high_level_design.md
│   ├── pseudocode.md
│   ├── test_cases.md
│   └── data_flow_diagram.md
├── tests/
│   └── test_app.py
├── requirements.txt
├── run.py
└── README.md
```

## 2. How to Run the Project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the website

```bash
python run.py
```

Then open your browser and go to:

```text
http://127.0.0.1:5000
```

## 3. Demo Login

### Admin account
- Email: `admin@bonnyriggpizza.local`
- Password: `Admin123!`

### Standard user
- Email: `student@bonnyriggpizza.local`
- Password: `Student123!`

## 4. Security Features Included

- passwords are hashed using Werkzeug
- login sessions are handled with Flask-Login
- admin routes are protected
- form input is validated and length-limited
- invalid actions return flash messages instead of crashing
- 404 and 500 error pages are included
- SQLite keeps data persistent and easy to manage for school assessment

## 5. Marking Criteria Alignment

### Component A - Project Documentation
This project includes:
- modular code and consistent formatting
- meaningful variable and function names
- comments throughout code
- directory structure that is easy to explain
- supporting documentation files in the `docs` folder
- README deployment instructions

### Component B - Software Solution
This project includes:
- high-level structure using application factory and modules
- class models for User, Recipe and Comment
- input validation
- secure authentication
- secure session management
- graceful error handling
- SQLite implementation
- search, filtering and commenting functionality

### Component C - Presentation Support
This project helps justify the use of:
- HTML for page structure
- CSS for styling and responsive layout
- JavaScript for frontend interactivity
- Flask for backend routing
- SQLite/SQLAlchemy for data storage
- GitHub for version control
- VS Code or PyCharm for development
- Figma for wireframes if you create mock-ups separately

## 6. Suggested Improvements for Full Marks

To push this even closer to full marks, you can optionally add:
- your own screenshots of the website in the documentation
- a GitHub repository link
- a team responsibility table
- a Gantt chart and process diary
- a PowerPoint presentation
- a draw.io flowchart export as images
- social media share button integrations
- optional pizza video embeds

## 7. Copyright Acknowledgement

This project uses the Flask framework, Flask-SQLAlchemy, Flask-Login and general Python open-source libraries. Recipe text and code structure in this packaged example were generated for educational use. Any additional images, tutorials, AI assistance, and external resources used in your final school submission should be acknowledged in your appendix and reference list.
