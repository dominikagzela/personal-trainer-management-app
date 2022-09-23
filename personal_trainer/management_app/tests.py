import pytest
from .models import (
    User,
    MacroElements,
    Reports,
    Photos,
    Exercises,
    PlanExercises,
    PracticalTips,
)


@pytest.mark.django_db
def test_login_user(client):
    '''
    The test of user login.
    '''
    client.login(username='trainer', password='testtest12')
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_user(client):
    '''
    The test of user logout.
    '''
    client.login(username='trainer', password='testtest12')
    response = client.get('/logout/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_trainer(client):
    '''
    The test of displaying dashboard trainer.
    '''
    response = client.get('/dashboard_trainer/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_practical_tip(client, tip):
    '''
    The test of adding new practical tip.
    '''
    response = client.post('/add_practical_tip/')
    assert response.status_code == 302
    assert PracticalTips.objects.get(tip='testowy')


@pytest.mark.django_db
def test_macro_elements_for_user(client, user, macro_elements):
    '''
    The test of displaying details of macro elements for selected client.
    '''
    response = client.get(f'/macro_elements_trainer/{user.id}/')
    assert response.status_code == 302
    assert User.objects.get(username='usertest')
    assert MacroElements.objects.get(user=user, fat=30)


# @pytest.mark.django_db
# def test_user_list(client, users):
#     response = client.get('/user_list/')
#     users = User.objects.all().order_by('first_name')
#     i = 0
#     for user in response.context['users']:
#         assert user == users[0]
#         i += 1
