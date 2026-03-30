# Test Cases

| Test ID | Requirement | Test Steps | Expected Result |
|---|---|---|---|
| TC01 | Homepage loads | Open the home page | Featured pizzas and latest recipes are displayed |
| TC02 | Register user | Enter valid username, email and matching password | User account is created successfully |
| TC03 | Validation works | Enter invalid email or short password | Error message appears |
| TC04 | Login works | Enter valid admin details | User logs in and session starts |
| TC05 | Search works | Search for 'pepperoni' | Matching recipe is shown |
| TC06 | Filter works | Select cuisine and difficulty | Only matching recipes are shown |
| TC07 | Comment system works | Log in and submit a valid comment | Comment appears on recipe page |
| TC08 | Admin creates recipe | Log in as admin and fill recipe form | New recipe appears in admin list and recipes page |
| TC09 | Admin delete works | Click delete on a recipe | Recipe is removed from database |
| TC10 | Error handling | Enter invalid URL | Custom 404 page appears |
