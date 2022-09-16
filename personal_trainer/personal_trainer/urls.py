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
from management_app.views import (
    logged_in,
    LoginView,
    LogoutView,
    UserListView,
    PracticalTipsView,
    ExercisesListView,
    AddExerciseView,
    DeleteExerciseView,
    UpdateExerciseView,
    MacroElementsUserView,
    PlanUserView,
    PlanTrainerView,
    PlanCreateExercise,
    PlanUpdateExercise,
    PlanDeleteExercise,
    PlanAddExercise,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # for both:
    path('logged_in', logged_in, name='logged_in'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('practical_tips/', PracticalTipsView.as_view(), name='practical-tips'),

    # for trainer:
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('exercises_list/', ExercisesListView.as_view(), name='exercises-list'),
    path('add_exercise/', AddExerciseView.as_view(), name='add-exercise'),
    path('update_exercise/<int:pk>/', UpdateExerciseView.as_view(), name='update-exercise'),
    path('delete_exercise/<int:pk>/', DeleteExerciseView.as_view(), name='delete-exercise'),
    path('plan_for_user/<int:user_id>/', PlanTrainerView.as_view(), name='plan-for-user'),
    path('plan_create_for_user/<int:user_id>/', PlanCreateExercise.as_view(), name='plan-create-for-user'),
    path('plan_update_exercise/<int:user_id>/<int:training_number>/<int:exercise_id>/<int:plan_pk>/',
         PlanUpdateExercise.as_view(), name='plan-update-exercise'),
    path('plan_delete_exercise/<int:user_id>/<int:pk>/', PlanDeleteExercise.as_view(), name='plan-delete-exercise'),
    path('plan_add_exercise/<int:user_id>/<int:training_number>/', PlanAddExercise.as_view(), name='plan-add-exercise'),


    # for users:
    path('macro_elements_user/', MacroElementsUserView.as_view(), name='macro-elements-user'),
    path('plan_user/', PlanUserView.as_view(), name='plan-user'),
]
