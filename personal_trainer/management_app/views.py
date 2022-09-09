from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, ListView, RedirectView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises
from .forms import LoginUserForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy


def tekst(request):
    a = 'zalogowany'
    return HttpResponse(a)


class LoginUserView(FormView):
    template_name = 'management_app/login_user.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        email = cd['email']
        password = cd['password']
        user = authenticate(email=email, password=password)
        login(self.request, user)

        return response


# widok tylko dla trenerki:
class UserListView(ListView):
    template_name = 'management_app/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_trainer=False).order_by('first_name')
