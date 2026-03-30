# High-Level Design

## Purpose
The purpose of the Bonnyrigg Pizza Blog is to provide a user-friendly and visually appealing website where users can browse pizza recipes, search and filter content, register accounts, post comments, and allow an administrator to manage recipe posts.

## Main Components
1. **Frontend**
   - HTML templates create the layout and structure.
   - CSS provides a responsive and appealing food-themed design.
   - JavaScript supports small interactive actions such as delete confirmation.

2. **Backend**
   - Flask controls routing and server-side logic.
   - Flask-Login manages user authentication and session handling.
   - SQLAlchemy connects the Flask app to the SQLite database.

3. **Database**
   - `User` table stores account details and admin roles.
   - `Recipe` table stores pizza content and filter information.
   - `Comment` table stores community interaction data.

## Class Interaction Summary
- A `User` can create many `Comment` entries.
- A `Recipe` can have many `Comment` entries.
- An `Admin User` can add and delete recipes through the dashboard.

## Design Strengths
- modular and maintainable structure
- secure login system
- clear separation of concerns
- responsive and professional UI
- suitable for further extension
