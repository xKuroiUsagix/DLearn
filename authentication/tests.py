from urllib import response
from django.test import TestCase
from django.contrib import auth
from http import HTTPStatus

from .errors import ErrorMessages
from .models import CustomUser


class RegistrationFormTests(TestCase):
    def setUp(self):
        self.good_data = {
            'email': 'testmail@mail.com',
            'password': 'goodpassword20',
            'confirm_password': 'goodpassword20',
            'first_name': 'firstname',
            'last_name': 'lastname'
        }
        self.path = '/auth/register/'
        self.form = 'form'
        
    def test_password_validation_error(self):
        data = self.good_data.copy()
        data['password'], data['confirm_password'] = 'weakpass', 'weakpass'
        response = self.client.post(self.path, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            self.form,
            'password',
            [str(ErrorMessages.PASSWORD_VALIDATION_ERROR)]
        )
    
    def test_confirm_password_error(self):
        data = self.good_data.copy()
        data['password'], data['confirm_password'] = 'strongpass10', 'not_same_password'
        response = self.client.post(self.path, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            self.form,
            'password',
            [str(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)]
        )
    
    def test_user_already_exists(self):
        CustomUser.objects.create_user(
            email='testmail@mail.com',
            password='password1'
        )
        data = self.good_data.copy()
        data['email'] = 'testmail@mail.com'
        response = self.client.post(self.path, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            self.form,
            'email',
            ['Custom user with this Email already exists.']
        )


class RegisterViewTests(TestCase):
    def setUp(self):
        self.path = '/auth/register/'
        self.template_name = 'authentication/register.html'
    
    def test_register_get(self):
        response = self.client.get(self.path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
    
    def test_register_post(self):
        email = 'goodmail10@mail.com'
        data = {
            'email': email,
            'password': 'goodpass10',
            'confirm_password': 'goodpass10',
            'first_name': 'firstname',
            'last_name': 'lastname'
        }
        homepage_url = '/'
        response = self.client.post(self.path, data=data)
        created_user = CustomUser.objects.get(email=email)
        
        self.assertIsNotNone(created_user)
        self.assertRedirects(response, homepage_url)
        self.assertTrue(created_user.is_authenticated)


class LoginFormTests(TestCase):
    def setUp(self):
        email = 'testmail@mail.com'
        password = 'goodpassword20'
        new_user_data = {
            'email': email,
            'password': password,
            'confirm_password': password,
            'first_name': 'firstname',
            'last_name': 'lastname'
        }
        CustomUser.objects.create_user(**new_user_data)
        
        self.good_data = {
            'email': email,
            'password': password
        }
        self.path = '/auth/login/'
        self.form = 'login_form'
    
    def test_user_login(self):
        response = self.client.post(self.path, self.good_data)
        redirect_url = '/'
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)
    
    def test_user_wrong_password(self):
        data = self.good_data.copy()
        data['password'] = 'badpassword'
        response = self.client.post(self.path, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            self.form,
            'email',
            [str(ErrorMessages.USER_NOT_FOUND_ERROR)]
        )
    
    def test_user_wrong_email(self):
        data = self.good_data.copy()
        data['email'] = 'nosuchuser@badmail.com'
        response = self.client.post(self.path, data=data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            self.form,
            'email',
            [str(ErrorMessages.USER_NOT_FOUND_ERROR)]
        )


class LoginViewTests(TestCase):
    def setUp(self):
        self.path = '/auth/login/'
        self.template_name = 'homepage/index.html'
    
    def test_login_get(self):
        response = self.client.get(self.path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
    
    def test_login_post(self):
        email = 'testmail@mail.com'
        password = 'goodpassword20'
        homepage_url = '/'
        new_user_data = {
            'email': email,
            'password': password,
            'confirm_password': password,
            'first_name': 'firstname',
            'last_name': 'lastname'
        }
        user = CustomUser.objects.create_user(**new_user_data)
        
        login_data = {
            'email': email,
            'password': password
        }
        response = self.client.post(self.path, data=login_data)
        
        self.assertRedirects(response, homepage_url)
        self.assertTrue(user.is_authenticated)


class LogoutViewTests(TestCase):
    def setUp(self):
        self.path = '/auth/logout/'
        self.login_path = '/auth/login/'
        self.homepage_url = '/'
    
    def test_user_logout(self):
        email = 'testmail@mail.com'
        password = 'goodpassword20'
        new_user_data = {
            'email': email,
            'password': password,
            'confirm_password': password,
            'first_name': 'firstname',
            'last_name': 'lastname'
        }
        user = CustomUser.objects.create_user(**new_user_data)
        
        self.client.post(self.login_path, 
                         data={
                             'email': email,
                             'password': password
                         })
        response = self.client.get(self.path)
        
        self.assertRedirects(response, self.homepage_url)
        self.assertTrue(user.is_authenticated)
