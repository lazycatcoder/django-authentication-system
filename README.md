<div align="center">
  <h1>Django authentication-system</h1>
</div>

<div align="justify">

   This repository contains code for an **authentication system** built using Django. The system allows users to sign up, log in, log out, and reset their passwords. It also includes an account activation feature via email confirmation.

   Key Features:
   -   User registration with email verification
   -   Login and logout functionality
   -   Password reset via email
   -   Account activation through email confirmation
   -   User interface templates for registration, login, password reset, and account activation

   The project utilizes Django's built-in authentication system, including user models, login views, password reset functionality, and token generation. It incorporates email sending capabilities for account verification and password reset. The code is structured into views and templates for seamless integration into a Django project.

   *Technologies used: Django, HTML, CSS, JavaScript.*

</div>

<br>

<div align="center">

# Settings
✨ To use it, you need to complete the following steps:

<br>


<div align="left">

1. Clone this repository

   ```
      git clone https://github.com/lazycatcoder/django-authentication-system.git
   ```

2. Open a terminal and navigate to the project **'authentication-system-django'** folder

   ```
      cd path/.../authentication-system-django
   ```

3. Create a virtual environment in the **'authentication-system-django'** folder
   
   ```
      python -m venv venv
   ```

4. Activate the virtual environment

   ```
      source venv/bin/activate   # MacOS/Linux 

      venv\Scripts\activate      # Windows
   ```

5. Install the following dependencies

   ```
      pip install Django==4.2.1
      pip install six==1.16.0
   ```

6. Use the console to navigate to the **'authentication-system-django\lss'** folder

   ```
      cd lss
   ```

7. Make migration

   ```
      python manage.py makemigrations
      python manage.py migrate
   ```

8. Сollect static files
   
   ```
      python manage.py collectstatic
   ```

9. Navigate to folder **'authentication-system-django\lss\lss'**
and open the **settings.py** file.

   The next step is to fill in some data in **settings.py**:
   
* Generating a new *SECRET_KEY* in **Django**

   ```
      python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

   This command will execute a Python script that imports the *get_random_secret_key()* function and calls it to generate a new key. The result will be printed in the terminal.

   When you get the new key, copy it and paste it into **settings.py** instead of *SECRET_KEY = ' '*'

10. Navigate to the **'authentication-system-django\lss\lss'** folder, open the **info.py** file and paste your *Email* and *App password*

   ```
      EMAIL_HOST_USER = 'youremail@gmail.com'
      EMAIL_HOST_PASSWORD = 'yourpassword'
      DEFAULT_FROM_EMAIL = 'youremail@gmail.com'
   ```

   You can get the *app password* in your Google account:
   https://myaccount.google.com/apppasswords

11. Use the console to navigate to the **'authentication-system-django\lss'** folder and run the server 

   ```
      python manage.py runserver
   ```

12. Open a browser and enter the following address to launch the project http://127.0.0.1:8000/ 🚀 

</div>


<br>