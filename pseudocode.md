# Pseudocode

## Home Page
START
LOAD featured recipes from database
LOAD latest recipes from database
DISPLAY homepage
END

## Register User
START
GET username, email, password, confirm password
IF username too short OR email invalid OR password too short OR passwords do not match
    SHOW validation error
ELSE IF username or email already exists
    SHOW duplicate account error
ELSE
    HASH password
    SAVE new user to database
    REDIRECT to login
END IF
END

## Login User
START
GET email and password
FIND user by email
IF user exists AND password hash matches
    CREATE secure login session
    REDIRECT to home page
ELSE
    SHOW login error
END IF
END

## Add Comment
START
CHECK if user is logged in
IF not logged in
    REDIRECT to login
ELSE
    GET comment text
    VALIDATE comment length
    SAVE comment to database
    REDIRECT back to recipe page
END IF
END

## Admin Add Recipe
START
CHECK admin access
GET recipe form inputs
VALIDATE all fields
IF valid
    SAVE recipe to database
    SHOW success message
ELSE
    SHOW error message
END IF
END
