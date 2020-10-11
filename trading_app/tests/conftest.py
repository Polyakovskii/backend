import uuid
import pytest
from django.urls import reverse
from trading_app.models import Item

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def authorized_client(create_user, api_client, test_password):
    url = reverse('get-token')
    user = create_user()
    password = test_password
    response = api_client.post(url, {'username': user.username, 'password': password}, format='json')
    token = 'jwt ' + response.data['token']
    api_client.force_authenticate(user=user, token=token)
    return api_client

