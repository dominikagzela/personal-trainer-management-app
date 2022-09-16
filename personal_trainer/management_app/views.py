from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, CreateView, ListView, UpdateView, DeleteView, RedirectView
from django.core.exceptions import ObjectDoesNotExist
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises, PracticalTips
from .forms import LoginUserForm, PlanExercisesForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import user_required, trainer_required

from django.db.models import Subquery, OuterRef
from django.template import Library

register = Library()


def logged_in(request):
    return HttpResponse('zalogowales sie')


class LoginView(FormView):
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


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


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
    template_name = 'management_app/add_exercise.html'
    fields = ['name', 'description', 'url']
    success_url = reverse_lazy('exercises-list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(AddExerciseView, self).post(request, *args, **kwargs)


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


# DLA USER'A:
@method_decorator(login_required, name='dispatch')
class MacroElementsUserView(ListView):
    model = MacroElements
    template_name = 'management_app/macro_elements.html'
    context_object_name = 'macros'

    def get_queryset(self):
        current_user = self.request.user
        return MacroElements.objects.filter(user_id=current_user.id)


@method_decorator(login_required, name='dispatch')
class PlanUserView(ListView):
    model = PlanExercises
    template_name = 'management_app/plan_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_user = self.request.user
        # Call the base implementation first to get a context
        # ctx = super().get_context_data(**kwargs)

        plans = PlanExercises.objects.filter(user=current_user.id)
        get_trainings = []
        for plan in plans:
            if not (plan.training_number in get_trainings):
                get_trainings.append(plan.training_number)
        ctx = {
            'trainings': get_trainings,
            'plans': plans
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanTrainerView(ListView):
    model = PlanExercises
    template_name = 'management_app/plan_trainer_view.html'

    def get_context_data(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        current_user = User.objects.get(id=current_user_id)
        plans = PlanExercises.objects.filter(user=current_user_id)
        get_trainings = []
        for plan in plans:
            if not (plan.training_number in get_trainings):
                get_trainings.append(plan.training_number)
        ctx = {
            'user': current_user,
            'trainings': get_trainings,
            'plans': plans
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanCreateExercise(CreateView):
    model = PlanExercises
    template_name = 'management_app/plan_create_form.html'


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanUpdateExercise(UpdateView):
    form_class = PlanExercisesForm
    template_name = 'management_app/plan_update_exercise.html'
    model = PlanExercises
    pk_url_kwarg = 'plan_pk'

    def form_valid(self, form, **kwargs):
        form.save()
        return super(PlanUpdateExercise, self).form_valid(form)

    def get_initial(self, queryset=None):
        current_user_id = self.kwargs['user_id']
        current_training = self.kwargs['training_number']
        current_exercise_id = self.kwargs['exercise_id']
        initial = super(PlanUpdateExercise, self).get_initial()
        plan = PlanExercises.objects.filter(
            user=current_user_id).filter(
            training_number=current_training).filter(
            exercise=current_exercise_id
        )
        initial['exercise'] = plan[0].exercise.name
        initial['series'] = plan[0].series
        initial['repeat'] = plan[0].repeat
        initial['TUT'] = plan[0].TUT
        return initial

    def get_success_url(self, *args, **kwargs):
        current_user_id = self.kwargs['user_id']
        return reverse('plan-for-user', args=[current_user_id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_training = self.kwargs['training_number']
        ctx['training_number'] = current_training
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanDeleteExercise(DeleteView):
    model = PlanExercises
    template_name = 'management_app/plan_delete_exercise.html'

    def get_success_url(self):
        current_user_id = self.kwargs['user_id']
        return reverse_lazy('plan-for-user', kwargs={'user_id': current_user_id})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(PlanDeleteExercise, self).post(request, *args, **kwargs)


class PlanAddExercise(CreateView):
    model = PlanExercises
    template_name = 'management_app/plan_add_exercise.html'
    form_class = PlanExercisesForm

    def get_success_url(self):
        current_user_id = self.kwargs['user_id']
        return reverse_lazy('plan-for-user', kwargs={'user_id': current_user_id})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(PlanAddExercise, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_training = self.kwargs['training_number']
        ctx['training_number'] = current_training
        return ctx

    def form_valid(self, form, **kwargs):
        current_user_id = self.kwargs['user_id']
        training_number_id = self.kwargs['training_number']
        user = User.objects.get(id=current_user_id)
        form.instance.user = user
        form.instance.training_number = training_number_id
        form.save()
        return super(PlanAddExercise, self).form_valid(form)
