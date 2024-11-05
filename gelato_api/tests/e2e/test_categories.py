from pytest import mark, fixture
from rest_framework.test import APIClient
from gelato_api.models import Category, User
from datetime import datetime

@fixture
def data():
    class Data():
        normal_user = User.objects.create_user(email="normal@user.com", password="12345", first_name="Normal", last_name="User")
        staff_user = User.objects.create_user(email="staff@user.com", password="12345", first_name="Staff", last_name="User", is_staff = True)
        superuser = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")
        category1 = Category.objects.create(name = "Ice Cream")
        category2 = Category.objects.create(name = "Cake")

    return Data()

# GET ------------------------------------------------------------------
@mark.django_db
def test_GET_all_categories_successful(data):
    expected_data = []
    for i in [data.category1, data.category2]:
        expected_data.append({"id": i.id, "name": i.name, "created": i.created})
    client = APIClient()
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert response.json()["results"] == expected_data

@mark.django_db
def test_GET_specific_category_successful(data):
    expected_data = {"id": data.category1.id, "name": data.category1.name, "created": data.category1.created}
    client = APIClient()
    response = client.get("/api/v1/categories/1/")
    assert response.status_code == 200
    assert response.json() == expected_data
# DELETE ------------------------------------------------------------------
@mark.django_db
def test_DELETE_specific_category_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.delete("/api/v1/categories/1/")
    assert response.status_code == 204
# POST ------------------------------------------------------------------
@mark.django_db
def test_POST_category_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.post("/api/v1/categories/", data = {"name": "Cookie"}, format = "json")
    expected_data = {"id": 3, "name": "Cookie", "created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    assert response.status_code == 201
    assert response.json() == expected_data

@mark.django_db
def test_POST_category_failed_required_name(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.post("/api/v1/categories/", data = {}, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == ["name"]
# PUT ------------------------------------------------------------------
@mark.django_db
def test_PUT_category_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/categories/1/", data = {"name": "New Ice Cream"}, format = "json")
    expected_data = {"id": data.category1.id, "name": "New Ice Cream", "created": data.category1.created}
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.django_db
def test_PUT_category_failed_required_name(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/categories/1/", data = {}, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == ["name"]
# PATCH ------------------------------------------------------------------
@mark.django_db
def test_PATCH_category_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.patch("/api/v1/categories/1/", data = {"name": "New Ice Cream"}, format = "json")
    expected_data = {"id": data.category1.id, "name": "New Ice Cream", "created": data.category1.created}
    assert response.status_code == 200
    assert response.json() == expected_data