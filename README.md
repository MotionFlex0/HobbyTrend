# Web_Project_Groupwork
Admin interface credentials
* Username: admin
* Password: test123

Test account credentials
* Username: user1 or user4
* Password: complexpassword

## We can start working on the stuff below (design using bootstrap and jquery etc.)

###### Currently 2 apps
* core - contains the core site. primarily the home.html(homepage).

* accounts - This extends the current functionally provided by the auth module (in this case, I have added a signup view). It also contains the custom user class (it has the specification items. dob, list of hobbies. it is only missing profile picture)

## Templates

templates/base.html - This file contains the header and footer, which should appear on all pages.

template/core/home.html - This file is the homepage. I have added some examples on how to check if a user is logged in and how to get their data. It appears you to go to _/_

templates/registration/login.html - This file is what will appear when the user goes to _/accounts/login_.

templates/registration/signup.html - This file is what will appear when the user goes to _/accounts/signup_.

## Paths
* _/_
* _/accounts/signup_
* _/accounts/login_
* _/accounts/logout_


## Other notes/updates
* The user model is pretty much done. The only thing that is missing the profile picture.
* Add new hobbies through the admin panel. It's the easiest way.
* The register page works so add users through that, or use the admin panel + changepassword command.
* I have reordered a few things to make it clearer. As well as added some examples to help.
* If you want to stop a view from being accessed if  the user isn't authenticated, import login_required then use the @login_required decorator.
```python   
    from django.contrib.auth.decorators import login_required

    @login_required
    def secret_view():
```
They will be redirected to the login page, then it will send them back
