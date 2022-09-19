"""personal_trainer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from management_app.views import (
    LoginView,
    LogoutView,
    DashboardTrainerView,
    DashboardUserView,
    UserListView,
    PracticalTipsUserView,
    PracticalTipsTrainerView,
    AddPracticalTipView,
    UpdatePracticalTipView,
    DeletePracticalTipView,
    ExercisesListView,
    AddExerciseView,
    DeleteExerciseView,
    UpdateExerciseView,
    PlanUserView,
    PlanTrainerView,
    PlanCreateExercise,
    PlanUpdateExercise,
    PlanDeleteExercise,
    PlanAddExercise,
    MacroElementsUserView,
    MacroElementsTrainerView,
    UpdateMacroElementsView,
    ReportListTrainerView,
    ReportDetailsTrainerView,
    ReportListUserView,
    ReportDetailsUserView,
    CreateReportUserView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # for both:
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # for trainer:
    path('dashboard_trainer/', DashboardTrainerView.as_view(), name='dashboard-trainer'),
    path('practical_tips_trainer/', PracticalTipsTrainerView.as_view(), name='practical-tips-trainer'),
    path('add_practical_tip/', AddPracticalTipView.as_view(),
         name='add-practical-tip'),
    path('update_practical_tip/<int:pk>/', UpdatePracticalTipView.as_view(),
         name='update-practical-tip'),
    path('delete_practical_tip/<int:pk>/', DeletePracticalTipView.as_view(),
         name='delete-practical-tip'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('exercises_list/', ExercisesListView.as_view(), name='exercises-list'),
    path('add_exercise/', AddExerciseView.as_view(), name='add-exercise'),
    path('update_exercise/<int:pk>/', UpdateExerciseView.as_view(), name='update-exercise'),
    path('delete_exercise/<int:pk>/', DeleteExerciseView.as_view(), name='delete-exercise'),
    path('plan_for_user/<int:user_id>/', PlanTrainerView.as_view(), name='plan-for-user'),
    path('plan_create_for_user/<int:user_id>/', PlanCreateExercise.as_view(), name='plan-create-for-user'),
    path('plan_update_exercise/<int:user_id>/<int:training_number>/<int:exercise_id>/<int:plan_pk>/',
         PlanUpdateExercise.as_view(), name='plan-update-exercise'),
    path('plan_delete_exercise/<int:user_id>/<int:pk>/', PlanDeleteExercise.as_view(),
         name='plan-delete-exercise'),
    path('plan_add_exercise/<int:user_id>/<int:training_number>/', PlanAddExercise.as_view(),
         name='plan-add-exercise'),
    path('macro_elements_trainer/<int:user_id>/', MacroElementsTrainerView.as_view(),
         name='macro-elements-trainer'),
    path('update_macro_elements/<int:user_id>/<int:macro_pk>/', UpdateMacroElementsView.as_view(),
         name='update-macro-elements'),
    path('report_list_trainer/<int:user_id>/', ReportListTrainerView.as_view(),
         name='report-list-trainer'),
    path('report_details_trainer/<int:user_id>/<int:report_pk>/', ReportDetailsTrainerView.as_view(),
         name='report-details-trainer'),

    # for users:
    path('dashboard_user/', DashboardUserView.as_view(), name='dashboard-user'),
    path('macro_elements_user/', MacroElementsUserView.as_view(), name='macro-elements-user'),
    path('plan_user/', PlanUserView.as_view(), name='plan-user'),
    path('practical_tips_user/', PracticalTipsUserView.as_view(), name='practical-tips-user'),
    path('report_list_user/', ReportListUserView.as_view(),
         name='report-list-user'),
    path('report_details_user/<int:report_pk>/', ReportDetailsUserView.as_view(),
         name='report-details-user'),
    path('create_report_user/', CreateReportUserView.as_view(),
         name='create-report-user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
