from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, ListView, RedirectView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises, PracticalTips
from .forms import LoginUserForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import user_required, trainer_required


def logged_in(request):
    return HttpResponse('zalogowales sie')


class LoginUserView(FormView):
    template_name = 'management_app/login_user.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('logged_in')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response
        else:
            return HttpResponse('Błędne dane logowania.')

        # return response


# tylko dla TRENERA
@method_decorator([login_required, trainer_required], name='dispatch')
class UserListView(ListView):
    template_name = 'management_app/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_trainer=False).order_by('first_name')


# dla OBU STRON:
@method_decorator(login_required, name='dispatch')
class PracticalTipsView(ListView):
    model = PracticalTips
    template_name = 'management_app/practical_tips.html'
    context_object_name = 'tips'


# tylko dla TRENERA:
@method_decorator([login_required, trainer_required], name='dispatch')
class ExercisesListView(ListView):
    model = Exercises
    template_name = 'management_app/exercises_list.html'
    context_object_name = 'exercises'


# tylko dla TRENERA:
@method_decorator([login_required, trainer_required], name='dispatch')
class AddExerciseView(CreateView):
    model = Exercises
    template_name = 'management_app/add_exercise_form.html'
    fields = ['name', 'description', 'url']
    success_url = reverse_lazy('exercises-list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(AddExerciseView, self).post(request, *args, **kwargs)


# tylko dla TRENERA:
@method_decorator([login_required, trainer_required], name='dispatch')
class DeleteExerciseView(DeleteView):
    model = Exercises
    template_name = 'management_app/delete_exercise.html'
    success_url = reverse_lazy('exercises-list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(DeleteExerciseView, self).post(request, *args, **kwargs)


# tylko dla TRENERA:
@method_decorator([login_required, trainer_required], name='dispatch')
class UpdateExerciseView(UpdateView):
    model = Exercises
    template_name = 'management_app/update_exercise.html'
    fields = ['name', 'description', 'url']
    success_url = reverse_lazy('exercises-list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(UpdateExerciseView, self).post(request, *args, **kwargs)


# class MacroElementsView(ListView)