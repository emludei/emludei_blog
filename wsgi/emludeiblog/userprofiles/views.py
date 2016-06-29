from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegistrationForm
from .models import User


def thanks(request):
    return render(request, 'userprofiles/thanks.html')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'userprofiles/profile.html', {'user': user})


def activate(request, activation_key):
    template_name = 'userprofiles/activate_profile.html'

    if activation_key != User.ACTIVATED:
        user = get_object_or_404(User, activation_key=activation_key)

        if not user.activation_key_expired():
            user.activate_user()

            return render(request, template_name, {'message': 'Profile successfully activated.'})

    return render(request, template_name, {'message': 'Activation key is expired.'})


class Registration(FormView):
    template_name = 'userprofiles/registration.html'
    success_url = reverse_lazy('profiles:thanks')
    form_class = RegistrationForm

    def form_valid(self, form):
        User.create_inactive_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )

        return super(Registration, self).form_valid(form)


class Login(View):
    template_name = 'userprofiles/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        redirect_url = request.POST.get('next', None)

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(redirect_url) if redirect_url else redirect('/')
            else:
                return render(request, self.template_name, {'error': 'Profile is not activated.'})

        return render(request, self.template_name, {'error': 'Username or password you entered is not correct'})
