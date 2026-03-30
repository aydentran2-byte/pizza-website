# Data Flow and Context Diagram Notes

## Context Diagram Summary
**External Entities:**
- Visitor/User
- Administrator
- SQLite Database

**Main System:**
- Bonnyrigg Pizza Blog Website

## Main Data Flows
1. User sends registration/login data to the website.
2. Website validates and stores/retrieves user data from the SQLite database.
3. User requests recipe pages.
4. Website retrieves recipe and comment data from the database.
5. Logged-in users submit comments.
6. Admin submits new recipe data or delete commands.
7. Website updates database records and sends updated pages back to the browser.

## Simple DFD Text Version
User -> Website: search, login, comment, recipe request
Website -> Database: read/write users, recipes, comments
Database -> Website: results returned
Website -> User: rendered pages and feedback messages
Admin -> Website: add/delete recipe actions
