from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    FormView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from .models import User, MacroElements, Reports, Photos, Exercises, PlanExercises, PracticalTips
from .forms import (
    LoginUserForm,
    PlanExercisesForm,
    ExercisesForm,
    PracticalTipForm,
    MacroElementsForm,
    ReportPhotosMultiForm,
)
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import user_required, trainer_required
import datetime
from django.core.exceptions import ObjectDoesNotExist


class LoginView(FormView):
    '''
    The view that allows the user to log in, checks that the logged in user is a superuser
    or ordinary user, on this basis, it redirects the user to the proper dashboard.
    '''
    template_name = 'management_app/login_user.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponse('Błędne dane logowania.')

    def get_success_url(self):
        user_is_trainer = self.request.user.is_trainer
        if user_is_trainer is True:
            return reverse_lazy('dashboard-trainer')
        else:
            return reverse_lazy('dashboard-user')


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    '''
    The view that allows the user to log out and redirects the login view.
    '''
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class DashboardTrainerView(ListView):
    '''
    The view shows the dashboard for the superuser with the menu available.
    '''
    template_name = 'management_app/dashboard_trainer.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_trainer=True)

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        user = User.objects.get(id=current_user.id)

        ctx = {
            'user': current_user,
        }
        return ctx


@method_decorator([login_required, user_required], name='dispatch')
class DashboardUserView(ListView):
    '''
    The view shows the dashboard for the ordinary user with the menu available.
    '''
    template_name = 'management_app/dashboard_user.html'

    def get_queryset(self):
        return User.objects.filter(is_trainer=False).order_by('first_name')


@method_decorator([login_required, trainer_required], name='dispatch')
class UserListView(ListView):
    '''
    The view shows the dashboard for the ordinary user with the menu available.
    '''
    template_name = 'management_app/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_trainer=False).order_by('first_name')



@method_decorator([login_required, user_required], name='dispatch')
class PracticalTipsUserView(ListView):
    model = PracticalTips
    template_name = 'management_app/practical_tips_user.html'
    context_object_name = 'tips'


@method_decorator([login_required, trainer_required], name='dispatch')
class PracticalTipsTrainerView(ListView):
    model = PracticalTips
    template_name = 'management_app/practical_tips_trainer.html'
    context_object_name = 'tips'


@method_decorator([login_required, trainer_required], name='dispatch')
class AddPracticalTipView(CreateView):
    model = PracticalTips
    template_name = 'management_app/add_practical_tip.html'
    form_class = PracticalTipForm
    success_url = reverse_lazy('practical-tips-trainer')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(AddPracticalTipView, self).post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class UpdatePracticalTipView(UpdateView):
    model = PracticalTips
    template_name = 'management_app/update_practical_tip.html'
    form_class = PracticalTipForm
    success_url = reverse_lazy('practical-tips-trainer')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(UpdatePracticalTipView, self).post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class DeletePracticalTipView(DeleteView):
    model = PracticalTips
    template_name = 'management_app/delete_practical_tip.html'
    success_url = reverse_lazy('practical-tips-trainer')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(DeletePracticalTipView, self).post(request, *args, **kwargs)


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
    form_class = ExercisesForm
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


@method_decorator([login_required, user_required], name='dispatch')
class PlanUserView(ListView):
    model = PlanExercises
    template_name = 'management_app/plan_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_user = self.request.user
        # Call the base implementation first to get a context

        plans = PlanExercises.objects.filter(user=current_user.id)
        get_trainings = []
        if not plans:
            plans = None
        else:
            for plan in plans:
                if not (plan.training_number in get_trainings):
                    get_trainings.append(plan.training_number)
        ctx = {
            'trainings': get_trainings,
            'plans': plans
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanForUserView(ListView):
    model = PlanExercises
    template_name = 'management_app/plan_trainer_view.html'

    def get_context_data(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        current_user = User.objects.get(id=current_user_id)
        plans = PlanExercises.objects.filter(user=current_user_id)
        get_trainings = [1, 2, 3, 4]
        if not plans:
            plans = None
        #     for plan in plans:
        #         if not (plan.training_number in get_trainings):
        #             get_trainings.append(plan.training_number)
        ctx = {
            'user': current_user,
            'trainings': get_trainings,
            'plans': plans
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanCreateExerciseView(CreateView):
    model = PlanExercises
    template_name = 'management_app/plan_create_form.html'


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanUpdateExerciseView(UpdateView):
    model = PlanExercises
    template_name = 'management_app/plan_update_exercise.html'
    form_class = PlanExercisesForm
    pk_url_kwarg = 'plan_pk'

    def get_initial(self, queryset=None):
        current_user_id = self.kwargs['user_id']
        current_training = self.kwargs['training_number']
        current_exercise_id = self.kwargs['exercise_id']
        initial = super(PlanUpdateExerciseView, self).get_initial()
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_training = self.kwargs['training_number']
        ctx['training_number'] = current_training
        return ctx

    def get_success_url(self, *args, **kwargs):
        current_user_id = self.kwargs['user_id']
        return reverse('plan-for-user', args=[current_user_id])

    def form_valid(self, form, **kwargs):
        form.save()
        return super(PlanUpdateExerciseView, self).form_valid(form)


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanDeleteExerciseView(DeleteView):
    model = PlanExercises
    template_name = 'management_app/plan_delete_exercise.html'

    def get_success_url(self):
        current_user_id = self.kwargs['user_id']
        return reverse_lazy('plan-for-user', kwargs={'user_id': current_user_id})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(PlanDeleteExerciseView, self).post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanAddExerciseView(CreateView):
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
            return super(PlanAddExerciseView, self).post(request, *args, **kwargs)

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
        return super(PlanAddExerciseView, self).form_valid(form)


# DLA USER'A:
@method_decorator([login_required, user_required], name='dispatch')
class MacroElementsUserView(ListView):
    model = MacroElements
    template_name = 'management_app/macro_elements_user.html'

    def get_queryset(self):
        current_user_id = self.request.user.id
        try:
            macro_elements = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macro_elements = None
        return macro_elements

    def get_context_data(self, **kwargs):
        current_user_id = self.request.user.id
        try:
            macros = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macros = None
        ctx = {
            'macros': macros,
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class MacroElementsTrainerView(ListView):
    model = MacroElements
    template_name = 'management_app/macro_elements_trainer.html'

    def get_queryset(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        try:
            macro_elements = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macro_elements = None
        return macro_elements

    def get_context_data(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        current_user = User.objects.get(id=current_user_id)
        try:
            macros = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macros = None
        ctx = {
            'user': current_user,
            'macros': macros,
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class UpdateMacroElementsView(UpdateView):
    model = MacroElements
    template_name = 'management_app/update_macro_elements.html'
    form_class = MacroElementsForm
    pk_url_kwarg = 'macro_pk'

    def get_success_url(self, *args, **kwargs):
        current_user_id = self.kwargs['user_id']
        return reverse('macro-elements-trainer', args=[current_user_id])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_user_id = self.kwargs['user_id']
        user = User.objects.get(id=current_user_id)
        ctx['user'] = user
        return ctx

    def form_valid(self, form, **kwargs):
        form.save()
        return super(UpdateMacroElementsView, self).form_valid(form)


class CreateMacroElementsView(CreateView):
    model = MacroElements
    template_name = 'management_app/create_macro_elements.html'
    form_class = MacroElementsForm

    def form_valid(self, form, **kwargs):
        current_user_id = self.kwargs['user_id']
        user = User.objects.get(id=current_user_id)
        form.instance.user = user
        form.save()
        return super(CreateMacroElementsView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        current_user_id = self.kwargs['user_id']
        return reverse('macro-elements-trainer', args=[current_user_id])

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(CreateMacroElementsView, self).post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class ReportListTrainerView(ListView):
    model = Reports
    template_name = 'management_app/report_list_trainer.html'

    def get_queryset(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        reports = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        return reports

    def get_context_data(self, **kwargs):
        current_user_id = self.kwargs['user_id']
        user = User.objects.get(id=current_user_id)
        reports = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        ctx = {
            'user': user,
            'reports': reports,
        }
        return ctx


@method_decorator([login_required, trainer_required], name='dispatch')
class ReportDetailsTrainerView(ListView):
    model = Reports
    template_name = 'management_app/report_details_trainer.html'

    def get_queryset(self, **kwargs):
        current_report_id = self.kwargs['report_pk']
        return Reports.objects.filter(pk=current_report_id)

    def get_context_data(self, **kwargs):
        # current_user_id = self.kwargs['user_id']
        current_user_id = 2
        current_report_id = self.kwargs['report_pk']
        user = User.objects.get(id=current_user_id)
        report = Reports.objects.get(pk=current_report_id)
        photos = Photos.objects.get(report=current_report_id)

        ctx = {
            'user': user,
            'report': report,
            'photos': photos,
        }
        return ctx


@method_decorator([login_required, user_required], name='dispatch')
class ReportListUserView(ListView):
    model = Reports
    template_name = 'management_app/report_list_user.html'

    def get_queryset(self, **kwargs):
        current_user_id = self.request.user.id
        reports = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        return reports

    def get_context_data(self, **kwargs):
        current_user_id = self.request.user.id
        user = User.objects.get(id=current_user_id)
        reports = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        ctx = {
            'user': user,
            'reports': reports,
        }
        return ctx


@method_decorator([login_required, user_required], name='dispatch')
class ReportDetailsUserView(ListView):
    model = Reports
    template_name = 'management_app/report_details_user.html'

    def get_queryset(self, **kwargs):
        current_report_id = self.kwargs['report_pk']
        return Reports.objects.filter(pk=current_report_id)

    def get_context_data(self, **kwargs):
        current_user_id = self.request.user.id
        current_report_id = self.kwargs['report_pk']
        user = User.objects.get(id=current_user_id)
        report = Reports.objects.get(pk=current_report_id)
        photos = Photos.objects.get(report=current_report_id)

        ctx = {
            'user': user,
            'report': report,
            'photos': photos,
        }
        return ctx


@method_decorator([login_required, user_required], name='dispatch')
class CreateReportUserView(CreateView):
    template_name = 'management_app/create_report.html'
    form_class = ReportPhotosMultiForm
    success_url = reverse_lazy('report-list-user')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = datetime.date.today()
        ctx['date'] = today
        return ctx

    def form_valid(self, form, **kwargs):
        current_user_id = self.request.user.id
        user = User.objects.get(id=current_user_id)
        form['report'].instance.user = user
        report = form['report'].save()
        photos = form['photos'].save(commit=False)
        photos.report = report
        photos.save()

        return super(CreateReportUserView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url())
        else:
            return super(CreateReportUserView, self).post(request, *args, **kwargs)
