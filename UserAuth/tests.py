from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from UserAuth.models import CustomUser
from django.contrib.messages import get_messages
from django.conf import settings
from django.contrib.sessions.models import Session



# Create your tests here.
# class AuthTest(TestCase):
#     def test_user_registration(self):
        response = self.client.get('/login',follow=True)
        self.assertEqual(response.status_code, 200)


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.registration_url = reverse('register')
        self.valid_data = {
            # 'username': 'testuser',
            'email': 'agboemmanuel002@gmail.com',
            'password1': 'scarface22',
            'password2': 'scarface22',
        }
        self.invalid_data = {
            'email': 'invalid_email',  # Invalid: Invalid email format
            'password1': 'scar',  # Invalid: Short password
            'password2': 'scars',  # Invalid: Passwords don't match
        }

    def test_registration_view(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserAuth/register.html')

    def test_registration_with_valid_data(self):
        response = self.client.post(self.registration_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(CustomUser.objects.filter(email='agboemmanuel002@gmail.com').exists())  
        self.assertEqual(len(get_messages(response.wsgi_request)), 0)  

    # def test_registration_with_invalid_data(self):
    #     response = self.client.post(self.registration_url, data=self.invalid_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
    #     self.assertFormError(response, 'form', 'password1', 'Ensure this value has at least 8 characters (it has 5).')
    #     self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

    from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginLogoutTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='agboemmanuel002@gmail.com', password='scarface11')

    def test_login_view_exists(self):
        response = self.client.get(reverse('login'))  
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        data = {
            'email': 'agboemmanuel002@gmail.com',
            'password': 'scarface11',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # 302 indicates a successful login and redirection
        self.assertRedirects(response, reverse('home'))  
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # def test_login_with_invalid_credentials(self):
    #     data = {
    #         'email': 'scar@gmail.com',
    #         'password': 'scarface23',  # Invalid password
    #     }
    #     response = self.client.post(reverse('login'), data)
    #     self.assertEqual(response.status_code, 200)  # Login page should be re-rendered
    #     self.assertFormError(response, 'form', None, 'Please enter a correct username and password.')  # Checking for form validation error
    #     self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view_exists(self):
        response = self.client.get(reverse('logout'))  
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirection after logout
        self.assertRedirects(response, reverse('login'))  # Redirects to the login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
        
class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.home_url = reverse('home')  
        self.login_url = reverse('login')  
        self.email = 'agboemmanuel002@gmail.com'
        self.password = 'scarface11'
        self.user = CustomUser.objects.create_user(email=self.email, password=self.password)

    def test_authenticated_user_can_access_home_page(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)  # Expect a successful response

    def test_unauthenticated_user_redirected_to_login_page(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.home_url}")




class SecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register') 
        self.home_url = reverse('home')  

    def test_session_fixation_attack(self):
        # Register a user
        response = self.client.post(self.register_url, {'email': 'agboemmanul002@gmail.com', 'password1': 'scarface11', 'password2': 'scarface11'})
        
        # Get the user's session ID
        session_key = self.client.session.session_key
        
        # Log out the user
        self.client.logout()
        
        # Attempt to access the home page with the captured session ID
        response = self.client.get(self.home_url, {'session_key': session_key})
        
        # Ensure that the user is redirected or not authorized
        self.assertNotEqual(response.status_code, 200)  # Expect a redirect or 403 Forbidden
        
        
class SecurityTestCaseCSRF(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  
        self.home_url = reverse('home')  

    def test_csrf_attack(self):
        # Register a user to have a valid session
        self.client.post(self.register_url, {'email': 'agboemmanuel002@gmail.com', 'password1': 'scarface11', 'password2': 'scarface11'})
        
        # Craft a malicious POST request
        csrf_attack_data = {'email': 'agbo@gmail.com', 'password': 'scarface22'}
        
        # Attempt to modify user data with the malicious POST request
        response = self.client.post(self.home_url, csrf_attack_data)
        
        # Ensure that the attack was unsuccessful (user data is not changed)
        self.assertNotEqual(CustomUser.objects.filter(email='agboemmanuel002@gmail.com').count(), 1)