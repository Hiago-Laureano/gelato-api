from pytest import mark, fixture
from rest_framework.test import APIClient
from gelato_api.models import User
from datetime import datetime

@fixture
def data():
    class Data():
        normal_user = User.objects.create_user(email="normal@user.com", password="12345", first_name="Normal", last_name="User")
        staff_user = User.objects.create_user(email="staff@user.com", password="12345", first_name="Staff", last_name="User", is_staff = True)
        superuser = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")

    return Data()

# GET ------------------------------------------------------------------
@mark.django_db
def test_GET_all_users_successful(data):
    expected_data = []
    for i in [data.normal_user, data.staff_user, data.superuser]:
        expected_data.append({
            "id": i.id,
            "email": i.email,
            "first_name": i.first_name,
            "last_name": i.last_name,
            "is_staff": i.is_staff,
            "is_active": i.is_active,
            "is_superuser": i.is_superuser,
            "last_login_date": i.last_login_date,
            "joined": i.joined
        })
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json()["results"] == expected_data

@mark.django_db
def test_GET_specific_user_with_superuser_successful(data):
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.get("/api/v1/users/1/")
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.django_db
def test_GET_specific_user_with_user_owner_successful(data):
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    client = APIClient()
    client.force_authenticate(user = data.normal_user)
    response = client.get("/api/v1/users/1/")
    assert response.status_code == 200
    assert response.json() == expected_data
# DELETE ------------------------------------------------------------------
@mark.django_db
def test_DELETE_specific_user_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.delete("/api/v1/users/1/")
    assert response.status_code == 204
# POST ------------------------------------------------------------------
@mark.django_db
def test_POST_user_successful(data):
    client = APIClient()
    response = client.post("/api/v1/users/", data = {"email": "new@test.com", "password": "12345"}, format = "json")
    user = User.objects.filter(email = "new@test.com").first()
    expected_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "last_login_date": user.last_login_date,
        "joined": user.joined
    }
    assert response.status_code == 201
    assert response.json() == expected_data

@mark.parametrize("field", ["email", "password"])
@mark.django_db
def test_POST_user_failed_required_field(field, data):
    expected_data = {
        "email": "name@test.com",
        "password": "12345"
    }
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.post("/api/v1/users/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PUT ------------------------------------------------------------------
@mark.django_db
def test_PUT_user_with_superuser_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.put("/api/v1/users/1/", data = {"email": "new@test.com", "password": "123456"}, format = "json")
    data.normal_user = User.objects.filter(email = "new@test.com").first()
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.django_db
def test_PUT_user_with_user_owner_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.normal_user)
    response = client.put("/api/v1/users/1/", data = {"email": "new@test.com", "password": "123456"}, format = "json")
    data.normal_user = User.objects.filter(email = "new@test.com").first()
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.parametrize("field", ["email", "password"])
@mark.django_db
def test_PUT_user_failed_required_field(field, data):
    expected_data = {
        "email": "name@test.com",
        "password": "12345"
    }
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.put("/api/v1/users/1/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PATCH ------------------------------------------------------------------
@mark.django_db
def test_PATCH_user_with_superuser_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.patch("/api/v1/users/1/", data = {"password": "123456"}, format = "json")
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.django_db
def test_PATCH_user_with_user_owner_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.normal_user)
    response = client.patch("/api/v1/users/1/", data = {"password": "123456"}, format = "json")
    expected_data = {
        "id": data.normal_user.id,
        "email": data.normal_user.email,
        "first_name": data.normal_user.first_name,
        "last_name": data.normal_user.last_name,
        "is_staff": data.normal_user.is_staff,
        "is_active": data.normal_user.is_active,
        "is_superuser": data.normal_user.is_superuser,
        "last_login_date": data.normal_user.last_login_date,
        "joined": data.normal_user.joined
    }
    assert response.status_code == 200
    assert response.json() == expected_data