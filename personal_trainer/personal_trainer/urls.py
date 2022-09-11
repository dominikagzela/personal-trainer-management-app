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
    LoginUserView,
    UserListView,
    PracticalTipsView,
    ExercisesListView,
    AddExerciseView,
    DeleteExerciseView,
    UpdateExerciseView,
    # MacroElementsView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logged_in', logged_in, name='logged_in'),
    path('', LoginUserView.as_view(), name='login-user'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('practical_tips/', PracticalTipsView.as_view(), name='practical-tips'),
    path('exercises_list/', ExercisesListView.as_view(), name='exercises-list'),
    path('add_exercise/', AddExerciseView.as_view(), name='add-exercise'),
    path('delete_exercise/<int:pk>/', DeleteExerciseView.as_view(), name='delete-exercise'),
    path('update_exercise/<int:pk>/', UpdateExerciseView.as_view(), name='update-exercise'),
    # path('macro_elements/', MacroElementsView.as_view(), name='macro-elements'),
]
