from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm, ProfileForm


# Create your views here.

class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch function is a method that gets called when the view is requested. It's responsible for returning
        an HttpResponse object, or raising an exception such as Http404 or PermissionDenied. The dispatch function
        takes in request and args/kwargs parameters, which are passed to it by Django.

        :param self: Represent the instance of the object itself
        :param request: Pass the request object to the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A redirect to the main view if a user is logged in
        :doc-author: Trelent
        """
        if request.user.is_authenticated:
            return redirect(to="quoteapp:main")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        The get function is used to display an empty form.
        The get function is called when the user navigates to the URL of this view,
        which in our case will be /contact/.

        :param self: Represent the instance of the object
        :param request: Pass the request object to the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: An instance of the form_class
        :doc-author: Trelent
        """
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        The post function is called when the user submits a form.
        The function checks if the form is valid, and if it is, saves it to the database.
        If not, an error message will be displayed on screen.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A redirect to the login page
        :doc-author: Trelent
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Your account successfully created: {username}")
            return redirect(to="users:login")

        return render(request, self.template_name, {"form": form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


@login_required
def profile(request):
    """
    The profile function is used to render the profile.html template
        when a user visits the /profile/ url.

    :param request: Get the current request
    :return: A rendered template
    :doc-author: Trelent
    """
    return render(request, 'users/profile.html')


@login_required
def profile(request):
    """
    The profile function is used to update the user's profile. It takes a request as an argument and returns a render
    of the users/profile.html template with the profile_form variable passed in.

    :param request: Get the request object
    :return: A profile form
    :doc-author: Trelent
    """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})
