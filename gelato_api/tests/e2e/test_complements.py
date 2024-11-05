from pytest import mark, fixture
from rest_framework.test import APIClient
from gelato_api.models import Category, User, Complement
from gelato_api.serializers import ComplementSerializer

@fixture
def data():
    class Data():
        normal_user = User.objects.create_user(email="normal@user.com", password="12345", first_name="Normal", last_name="User")
        staff_user = User.objects.create_user(email="staff@user.com", password="12345", first_name="Staff", last_name="User", is_staff = True)
        superuser = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")
        category = Category.objects.create(name = "Ice Cream")
        class Request():
            user = User.objects.filter(email="super@user.com").first()
        complement1 = ComplementSerializer(context = {"request": Request()}, data = {"name": "candy", "categories": [category.id]})
        complement1.is_valid()
        complement1.save()
        complement2 = ComplementSerializer(context = {"request": Request()}, data = {"name": "candy2", "categories": [category.id]})
        complement2.is_valid()
        complement2.save()
    return Data()

# GET ------------------------------------------------------------------
@mark.django_db
def test_GET_all_complements_successful(data):
    expected_data = []
    for i in [data.complement1, data.complement2]:
        expected_data.append(i.data)
    client = APIClient()
    response = client.get("/api/v1/complements/")
    assert response.status_code == 200
    assert response.json()["results"] == expected_data

@mark.django_db
def test_GET_specific_complement_successful(data):
    expected_data = data.complement1.data
    client = APIClient()
    response = client.get("/api/v1/complements/1/")
    assert response.status_code == 200
    assert response.json() == expected_data
# DELETE ------------------------------------------------------------------
@mark.django_db
def test_DELETE_specific_complement_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.delete("/api/v1/complements/1/")
    assert response.status_code == 204
# POST ------------------------------------------------------------------
@mark.django_db
def test_POST_complement_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.post("/api/v1/complements/", data = {"name": "candy3", "categories": [data.category.id]}, format = "json")
    complement = ComplementSerializer(Complement.objects.filter(name = "candy3").first())
    expected_data = complement.data
    assert response.status_code == 201
    assert response.json() == expected_data

@mark.parametrize("field", ["name", "categories"])
@mark.django_db
def test_POST_complement_failed_required_field(field, data):
    expected_data = {
        "name": "candy3",
        "categories": [1]
    }
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.post("/api/v1/complements/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PUT ------------------------------------------------------------------
@mark.django_db
def test_PUT_complement_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/complements/1/", data = {"name": "candy3", "categories": [data.category.id]}, format = "json")
    complement = ComplementSerializer(Complement.objects.filter(name = "candy3").first())
    expected_data = complement.data
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.parametrize("field", ["name", "categories"])
@mark.django_db
def test_PUT_complement_failed_required_field(field, data):
    expected_data = {
        "name": "candy3",
        "categories": [1]
    }
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/complements/1/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PATCH ------------------------------------------------------------------
@mark.django_db
def test_PATCH_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.patch("/api/v1/complements/1/", data = {"name": "candy3"}, format = "json")
    complement = ComplementSerializer(Complement.objects.filter(name = "candy3").first())
    expected_data = complement.data
    assert response.status_code == 200
    assert response.json() == expected_data