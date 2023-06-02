from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    FormView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from .models import (
    User,
    MacroElements,
    Reports,
    Photos,
    Exercises,
    PlanExercises,
    PracticalTips
)
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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import user_required, trainer_required
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.db.models.query import QuerySet
from typing import List, Optional, Dict, Type


class LoginView(FormView):
    """
    The view that allows the user to log in, checks that the logged in user is a superuser
    or client and on this basis, it redirects user to the proper dashboard.
    """
    template_name: str = 'management_app/login.html'
    form_class: Type[LoginUserForm] = LoginUserForm

    def form_valid(self, form: LoginUserForm) -> HttpResponse:
        cleaned_data: dict[str, str] = form.cleaned_data
        username: str = cleaned_data['username']
        password: str = cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponse('Błędne dane logowania.')

    def get_success_url(self) -> str:
        user_is_trainer: bool = self.request.user.is_trainer
        if user_is_trainer is True:
            return reverse_lazy('dashboard-trainer')
        else:
            return reverse_lazy('dashboard-user')


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    """
    The view that allows the user to log out and redirects to the login view.
    """
    url: str = reverse_lazy('login')

    def get(self, request, *args, **kwargs) -> View:
        logout(request)
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class DashboardTrainerView(ListView):
    """
    The view shows the dashboard for the superuser with the menu available.
    """
    template_name: str = 'management_app/dashboard_trainer.html'
    queryset: QuerySet[User] = User.objects.filter(is_trainer=True)


@method_decorator([login_required, user_required], name='dispatch')
class DashboardUserView(ListView):
    """
    The view shows the dashboard for the client with the menu available.
    """
    template_name: str = 'management_app/dashboard_user.html'
    queryset: QuerySet[User] = User.objects.filter(is_trainer=False).order_by('first_name')


@method_decorator([login_required, trainer_required], name='dispatch')
class UserListView(ListView):
    """
    The view shows the superuser a list of clients.
    """
    template_name: str = 'management_app/user_list.html'
    context_object_name: str = 'users'

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_trainer=False).order_by('first_name')


@method_decorator([login_required, user_required], name='dispatch')
class PracticalTipsUserView(ListView):
    """
    The view shows the client a list of practical tips.
    """
    model: Type[PracticalTips] = PracticalTips
    template_name: str = 'management_app/practical_tips_user.html'
    context_object_name: str = 'tips'


@method_decorator([login_required, trainer_required], name='dispatch')
class PracticalTipsTrainerView(ListView):
    """
    The view shows the superuser a list of practical tips.
    """
    model: Type[PracticalTips] = PracticalTips
    template_name: str = 'management_app/practical_tips_trainer.html'
    context_object_name: str = 'tips'


@method_decorator([login_required, trainer_required], name='dispatch')
class AddPracticalTipView(CreateView):
    """
    The view allows the superuser to add a new tip to the list of practical tips.
    """
    model: Type[PracticalTips] = PracticalTips
    template_name: str = 'management_app/add_practical_tip.html'
    form_class: Type[PracticalTipForm] = PracticalTipForm
    success_url: str = reverse_lazy('practical-tips-trainer')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class UpdatePracticalTipView(UpdateView):
    """
    The view allows the superuser to update the selected tip.
    """
    model: Type[PracticalTips] = PracticalTips
    template_name: str = 'management_app/update_practical_tip.html'
    form_class: Type[PracticalTipForm] = PracticalTipForm
    success_url: str = reverse_lazy('practical-tips-trainer')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class DeletePracticalTipView(DeleteView):
    """
    The view allows the superuser to delete the selected tip.
    """
    model: Type[PracticalTips] = PracticalTips
    template_name: str = 'management_app/delete_practical_tip.html'
    success_url: str = reverse_lazy('practical-tips-trainer')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class ExercisesListView(ListView):
    """
    The view shows the superuser a list of all available exercises.
    """
    model: Type[Exercises] = Exercises
    template_name: str = 'management_app/exercises_list.html'
    context_object_name: str = 'exercises'


@method_decorator([login_required, trainer_required], name='dispatch')
class AddExerciseView(CreateView):
    """
    The view allows the superuser to add a new exercise to the list of all available exercises.
    """
    template_name: str = 'management_app/add_exercise.html'
    form_class: Type[ExercisesForm] = ExercisesForm
    success_url: str = reverse_lazy('exercises-list')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class UpdateExerciseView(UpdateView):
    """
    The view allows the superuser to update the selected exercise.
    """
    model: Type[Exercises] = Exercises
    template_name: str = 'management_app/update_exercise.html'
    form_class: Type[ExercisesForm] = ExercisesForm
    success_url: str = reverse_lazy('exercises-list')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class DeleteExerciseView(DeleteView):
    """
    The view allows the superuser to delete the selected exercise.
    """
    model: Type[Exercises] = Exercises
    template_name: str = 'management_app/delete_exercise.html'
    success_url: str = reverse_lazy('exercises-list')
    cancel_text: str = 'cancel'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, user_required], name='dispatch')
class PlanUserView(ListView):
    """
    The view shows the client his exercise plan.
    """
    model: Type[PlanExercises] = PlanExercises
    template_name: str = 'management_app/plan_user.html'

    def get_context_data(self, **kwargs) -> Dict[str, Optional[List[int]]]:
        current_user = self.request.user

        plans: Optional[List[PlanExercises]] = PlanExercises.objects.filter(user=current_user.pk)
        get_trainings: List[int] = []
        if not plans:
            plans = None
        else:
            for plan in plans:
                if not (plan.training_number in get_trainings):
                    get_trainings.append(plan.training_number)

        context: Dict[str, Optional[List[int]]] = {
            'trainings': get_trainings,
            'plans': plans
        }
        return context


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanForUserView(ListView):
    """
    The view shows the superuser an exercise plan for the selected client.
    """
    model: Type[PlanExercises] = PlanExercises
    template_name: str = 'management_app/plan_trainer_view.html'

    def get_context_data(self, **kwargs) -> Dict[str, Optional[List[int]]]:
        current_user_id: int = self.kwargs['user_id']
        current_user: User = User.objects.get(id=current_user_id)

        plans: Optional[List[PlanExercises]] = PlanExercises.objects.filter(user=current_user_id)
        get_trainings: List[int]  = [1, 2, 3, 4]
        if not plans:
            plans = None

        context: Dict[str, Optional[List[int]]] = {
            'user': current_user,
            'trainings': get_trainings,
            'plans': plans
        }
        return context


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanUpdateExerciseView(UpdateView):
    """
    The view allows the superuser to update an exercise to the selected
    training from plan of the selected client.
    """
    model: Type[PlanExercises] = PlanExercises
    template_name: str = 'management_app/plan_update_exercise.html'
    form_class: Type[PlanExercisesForm] = PlanExercisesForm
    pk_url_kwarg: str = 'plan_pk'
    cancel_text: str = 'cancel'

    def get_initial(self, queryset=None) -> Dict[str, any]:
        current_user_id: int = self.kwargs['user_id']
        current_training: int = self.kwargs['training_number']
        current_exercise_id: int = self.kwargs['exercise_id']

        initial: Dict[str, any]  = super(PlanUpdateExerciseView, self).get_initial()
        plan: Optional[List[PlanExercises]] = PlanExercises.objects.filter(
            user=current_user_id).filter(
            training_number=current_training).filter(
            exercise=current_exercise_id
        )
        initial['exercise'] = plan[0].exercise.name
        initial['series'] = plan[0].series
        initial['repeat'] = plan[0].repeat
        initial['TUT'] = plan[0].TUT
        return initial

    def get_context_data(self, **kwargs) -> Dict[str, int]:
        context: dict = super().get_context_data(**kwargs)
        current_training: int = self.kwargs['training_number']
        context['training_number'] = current_training
        return context

    def get_success_url(self, *args, **kwargs) -> str:
        current_user_id: int = self.kwargs['user_id']
        return reverse('plan-for-user', args=[current_user_id])

    def form_valid(self, form, **kwargs) -> HttpResponseRedirect:
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanDeleteExerciseView(DeleteView):
    """
    The view allows the superuser to delete an exercise to the selected
    training from plan of the selected client.
    """
    model: Type[PlanExercises] = PlanExercises
    template_name: str = 'management_app/plan_delete_exercise.html'
    cancel_text: str = 'cancel'

    def get_success_url(self) -> str:
        current_user_id: int = self.kwargs['user_id']
        return reverse_lazy('plan-for-user', kwargs={'user_id': current_user_id})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class PlanAddExerciseView(CreateView):
    """
    The view allows the superuser to add a new exercise to the selected
    training from plan of the selected client.
    """
    model: Type[PlanExercises] = PlanExercises
    template_name: str = 'management_app/plan_add_exercise.html'
    form_class: Type[PlanExercisesForm] = PlanExercisesForm
    cancel_text: str = 'cancel'

    def get_success_url(self) -> str:
        current_user_id: int = self.kwargs['user_id']
        return reverse_lazy('plan-for-user', kwargs={'user_id': current_user_id})

    def get_context_data(self, **kwargs) -> Dict[str, int]:
        context: dict = super().get_context_data(**kwargs)
        current_training: int = self.kwargs['training_number']
        context['training_number'] = current_training
        return context

    def form_valid(self, form, **kwargs) -> HttpResponseRedirect:
        current_user_id: int = self.kwargs['user_id']
        training_number_id: int = self.kwargs['training_number']
        user: User = User.objects.get(id=current_user_id)
        form.instance.user = user
        form.instance.training_number = training_number_id
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, user_required], name='dispatch')
class MacroElementsUserView(ListView):
    """
    The view shows the client his macro elements.
    """
    model: Type[MacroElements] = MacroElements
    template_name: str = 'management_app/macro_elements_user.html'

    def get_queryset(self) -> MacroElements:
        current_user_id: int = self.request.user.id
        try:
            macro_elements: Optional[MacroElements] = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macro_elements = None
        return macro_elements

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.request.user.id
        try:
            macros: Optional[MacroElements] = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macros = None
        context: Dict[str, any] = {
            'macros': macros,
        }
        return context


@method_decorator([login_required, trainer_required], name='dispatch')
class MacroElementsTrainerView(ListView):
    """
    The view shows the superuser macro elements for the selected client.
    """
    model: Type[MacroElements] = MacroElements
    template_name: str = 'management_app/macro_elements_trainer.html'

    def get_queryset(self, **kwargs) -> MacroElements:
        current_user_id: int = self.kwargs['user_id']
        try:
            macro_elements: Optional[MacroElements] = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macro_elements = None
        return macro_elements

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.kwargs['user_id']
        current_user: User = User.objects.get(id=current_user_id)
        try:
            macros: Optional[MacroElements] = MacroElements.objects.get(user=current_user_id)
        except ObjectDoesNotExist:
            macros = None
        context: Dict[str, any] = {
            'user': current_user,
            'macros': macros,
        }
        return context


@method_decorator([login_required, trainer_required], name='dispatch')
class UpdateMacroElementsView(UpdateView):
    """
    The view allows the superuser update macro elements for the selected client.
    """
    model: Type[MacroElements] = MacroElements
    template_name: str = 'management_app/update_macro_elements.html'
    form_class: Type[MacroElementsForm] = MacroElementsForm
    pk_url_kwarg: int = 'macro_pk'
    cancel_text: str = 'cancel'

    def get_success_url(self, *args, **kwargs) -> str:
        current_user_id: int = self.kwargs['user_id']
        return reverse('macro-elements-trainer', args=[current_user_id])

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, any] = super().get_context_data(**kwargs)
        current_user_id: int = self.kwargs['user_id']
        user: User = User.objects.get(id=current_user_id)
        context['user'] = user
        return context

    def form_valid(self, form, **kwargs) -> HttpResponseRedirect:
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class CreateMacroElementsView(CreateView):
    """
    The view allows the superuser create macro elements for the selected client.
    """
    model: Type[MacroElements] = MacroElements
    template_name: str = 'management_app/create_macro_elements.html'
    form_class: Type[MacroElementsForm] = MacroElementsForm
    cancel_text: str = 'cancel'

    def form_valid(self, form, **kwargs) -> HttpResponseRedirect:
        current_user_id: int = self.kwargs['user_id']
        user: User = User.objects.get(id=current_user_id)
        form.instance.user = user
        form.save()
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs) -> str:
        current_user_id: int = self.kwargs['user_id']
        return reverse('macro-elements-trainer', args=[current_user_id])

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


@method_decorator([login_required, trainer_required], name='dispatch')
class ReportListTrainerView(ListView):
    """
    The view shows the superuser a list of reports for the selected client.
    """
    model: Type[Reports] = Reports
    template_name: str = 'management_app/report_list_trainer.html'

    def get_queryset(self, **kwargs) -> Optional[List[Reports]]:
        current_user_id: int = self.kwargs['user_id']
        reports: Optional[List[Reports]] = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        return reports

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.kwargs['user_id']
        user: User = User.objects.get(id=current_user_id)
        reports: Optional[Reports] = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        context: Dict[str, any] = {
            'user': user,
            'reports': reports,
        }
        return context


@method_decorator([login_required, trainer_required], name='dispatch')
class ReportDetailsTrainerView(ListView):
    """
    The view shows the superuser details of selected report for the selected client.
    """
    model: Type[Reports] = Reports
    template_name: str = 'management_app/report_details_trainer.html'

    def get_queryset(self, **kwargs) -> Reports:
        current_report_id: int = self.kwargs['report_pk']
        return Reports.objects.filter(pk=current_report_id)

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.kwargs['user_id']
        current_report_id: int = self.kwargs['report_pk']
        user: User = User.objects.get(id=current_user_id)
        report: Reports = Reports.objects.get(pk=current_report_id)
        photos: Photos = Photos.objects.get(report=current_report_id)

        context: Dict[str, any] = {
            'user': user,
            'report': report,
            'photos': photos,
        }
        return context


@method_decorator([login_required, user_required], name='dispatch')
class ReportListUserView(ListView):
    """
    The view shows the client a list of his reports.
    """
    model: Type[Reports] = Reports
    template_name: str = 'management_app/report_list_user.html'

    def get_queryset(self, **kwargs) -> Optional[Reports]:
        current_user_id: int = self.request.user.id
        reports: Optional[Reports] = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        return reports

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.request.user.id
        user: User = User.objects.get(id=current_user_id)
        reports: Optional[Reports] = Reports.objects.filter(user=current_user_id)
        if not reports:
            reports = None
        context: Dict[str, any] = {
            'user': user,
            'reports': reports,
        }
        return context


@method_decorator([login_required, user_required], name='dispatch')
class ReportDetailsUserView(ListView):
    """
    The view shows the client details of his selected report.
    """
    model: Type[Reports] = Reports
    template_name: str = 'management_app/report_details_user.html'

    def get_queryset(self, **kwargs) -> Reports:
        current_report_id: int = self.kwargs['report_pk']
        return Reports.objects.filter(pk=current_report_id)

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        current_user_id: int = self.request.user.id
        current_report_id: int = self.kwargs['report_pk']
        user: User = User.objects.get(id=current_user_id)
        report: Reports = Reports.objects.get(pk=current_report_id)
        photos: Photos = Photos.objects.get(report=current_report_id)

        context: Dict[str, any] = {
            'user': user,
            'report': report,
            'photos': photos,
        }
        return context


@method_decorator([login_required, user_required], name='dispatch')
class CreateReportUserView(CreateView):
    """
    The view allows the client to create new report to the list of his reports.
    """
    template_name: str = 'management_app/create_report.html'
    form_class: Type[ReportPhotosMultiForm] = ReportPhotosMultiForm
    success_url: str = reverse_lazy('report-list-user')
    cancel_text: str = 'cancel'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, any] = super().get_context_data(**kwargs)
        today: datetime.date = datetime.date.today()
        context['date'] = today
        return context

    def form_valid(self, form, **kwargs) -> HttpResponseRedirect:
        current_user_id: int = self.request.user.id
        user: User = User.objects.get(id=current_user_id)
        form['report'].instance.user = user
        report = form['report'].save()
        photos = form['photos'].save(commit=False)
        photos.report = report
        photos.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if self.cancel_text in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)
