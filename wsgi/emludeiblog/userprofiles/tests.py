import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse


from . import forms
from .models import User


class UserModelTest(TestCase):
    def test_create_inactive_user(self):
        User.create_inactive_user(username='testuser', password='testpass', email='test')
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)

    def test_delete_expired_users(self):
        date = timezone.now() - datetime.timedelta(30)

        user = User(username='test', email='test', date_joined=date, is_active=False)
        user.set_password('test')
        user.save()
        User.delete_expired_profiles()

        self.assertEqual(User.objects.all().count(), 0)

    def test_activate_user(self):
        User.create_inactive_user(username='test', password='test', email='test')
        user = User.objects.get(username='test')
        user.activate_user()

        self.assertTrue(user.is_active)

    def test_activation_key_expired(self):
        date = timezone.now() - datetime.timedelta(30)

        user = User(username='test', email='test', date_joined=date, is_active=False)
        user.set_password('test')
        user.save()

        self.assertTrue(user.activation_key_expired())


class TestForms(TestCase):
    def test_profile_creation_form(self):
        data = {
            'username': 'test',
            'password1': 'test',
            'password2': 'qwe'
        }

        form = forms.ProfileCreationForm(data=data, )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'], ['Too simple password.'])

        data = {
            'username': 'test',
            'password1': 'asdasdasd676776$^&%asd9ada98d7asd^&^%SD',
            'password2': '123'
        }

        form = forms.ProfileCreationForm(data=data)

        self.assertEqual(form.errors['password2'], ["The two password fields didn't match."])

    def test_registration_form(self):
        data = {
            'username': 'test',
            'email': 'test',
            'password1': 'asd56%^%A^D%A%&SD%&A%D&%S&ADASDAS&66sdasda78',
            'password2': 'asd56%^%A^D%A%&SD%&A%D&%S&ADASDAS&66sdasda78'
        }

        form = forms.RegistrationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

        data['email'] = 'test@test.test'

        form = forms.RegistrationForm(data=data)

        self.assertTrue(form.is_valid())

        form.save()

        new_form = forms.RegistrationForm(data=data)

        self.assertFalse(new_form.is_valid())
        self.assertEqual(new_form.errors['email'], ['Email (test@test.test) already in use.'])

    def test_user_password_change_form(self):
        user = User.objects.create_user(username='test', email='test@test.test', password='test')

        data = {
            'old_password': 'test',
            'new_password1': 'test1',
            'new_password2': 'test1'
        }

        form = forms.UserPasswordChangeForm(user=user, data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password1'], ['Too simple password.'])

        data['new_password1'] = 'ahsdjagdja6776757asdas%^&ASD'

        form = forms.UserPasswordChangeForm(user, data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ["The two password fields didn't match."])

        data['new_password2'] = data['new_password1']

        form = forms.UserPasswordChangeForm(user=user, data=data)

        self.assertTrue(form.is_valid())

    def test_user_password_set_form(self):
        user = User.objects.create_user(username='test', email='test@test.test', password='test')

        data = {
            'new_password1': 'test',
            'new_password2': 'test'
        }

        form = forms.UserPasswordSetForm(user=user, data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password1'], ['Too simple password.'])

        data['new_password1'] = 'asdJKHASUIDH&*6*&68&^*DYBy8b&Y*CAYS'

        form = forms.UserPasswordSetForm(user=user, data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ["The two password fields didn't match."])

        data['new_password2'] = data['new_password1']

        form = forms.UserPasswordSetForm(user=user, data=data)

        self.assertTrue(form.is_valid())

    def test_user_password_reset_form(self):
        data = {
            'email': 'test'
        }

        form = forms.UserPasswordResetForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

        data['email'] = 'asd@asd.asd'

        form = forms.UserPasswordResetForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['User with such e-mail address not exist.'])

        User.objects.create_user(username='test', email='asd@asd.asd', password='test')

        form = forms.UserPasswordResetForm(data=data)

        self.assertTrue(form.is_valid())


class TestViews(TestCase):
    def test_activate_view(self):
        User.create_inactive_user(username='test', email='test@test.test', password='test')

        user = User.objects.get(username='test')

        response = self.client.get(reverse('profiles:activate', args=(user.activation_key,)))

        self.assertContains(response, 'Profile successfully activated.')

        response = self.client.get(reverse('profiles:activate', args=(user.activation_key,)))

        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('profiles:activate', args=('ACTIVATED',)))

        self.assertContains(response, 'Activation key is expired.')

    def test_registration_view(self):
        data = {
            'username': 'test',
            'email': 'test@test.test',
            'password1': 'test',
            'password2': 'test'
        }

        response = self.client.post(reverse('profiles:registration'), data=data)
        self.assertContains(response, 'Too simple password.')

        data['password1'] = 'jasdgajsd^&%sJAsgjad67a'

        response = self.client.post(reverse('profiles:registration'), data=data)

        self.assertContains(response, "The two password fields didn")

        data['password2'] = data['password1']

        response = self.client.post(reverse('profiles:registration'), data=data)

        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        data = {
            'username': 'test',
            'email': 'test',
            'password': 'test'
        }

        user = User.objects.create_user(**data)

        response = self.client.get(reverse('profiles:login'))

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('profiles:login'),
            data={'username': data['username'], 'password': 'sadsad'}
        )

        self.assertContains(response, 'Username or password you entered is not correct')

        response = self.client.post(reverse('profiles:login'), data=data)

        self.assertEqual(response.status_code, 302)

        user.delete()

        User.create_inactive_user(**data)

        response = self.client.post(reverse('profiles:login'), data=data)

        self.assertContains(response, 'Profile is not activated.')
