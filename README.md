Project Documentation
1. After setting up your virtual environment.

2. Run the command "pip install -r requirements.txt " to install the necessary libraries.

3. create a database in your php admin with the name "auth_project", or you uncomment django default database in the    settings.py file

4. Then run "python manage.py runserver"


############

TESTING

For the testing run the following command 

//Write unit tests to verify that user registration works correctly. Ensure that the registration view validates input data and creates new user accounts.

-----Run "python manage.py test UserAuth.tests.RegistrationTestCase" command

//Write tests for the user login and logout views to ensure that users can log in and out successfully.

-----Run "python manage.py test UserAuth.tests.LoginLogoutTestCase" command

//Implement tests to confirm that only authenticated users can access the task management views. Unauthorized users should be redirected to the login page.

-----Run "python manage.py test UserAuth.tests.AuthenticationTestCase" Command

//Implement tests to validate the security of the authentication system. Test for potential security vulnerabilities like session fixation and CSRF attacks.

-----Run "python manage.py test UserAuth.tests.SecurityTestCase" command and 
"python manage.py test UserAuth.tests.SecurityTestCaseCSRF" command

OR RUN A GENERAL TEST USING "python manage.py test UserAuth.tests test" command