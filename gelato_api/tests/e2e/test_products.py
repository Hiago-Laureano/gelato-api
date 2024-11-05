from pytest import mark, fixture
from rest_framework.test import APIClient
from gelato_api.models import User, Product, Category
from gelato_api.serializers import ProductSerializer, ComplementSerializer

@fixture
def data():
    class Data():
        normal_user = User.objects.create_user(email="normal@user.com", password="12345", first_name="Normal", last_name="User")
        staff_user = User.objects.create_user(email="staff@user.com", password="12345", first_name="Staff", last_name="User", is_staff = True)
        superuser = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")
        class Request():
            user = User.objects.filter(email="super@user.com").first()
        category = Category.objects.create(name = "Ice Cream")
        product1 = ProductSerializer(context = {"request": Request()}, data = {"name": "item1", "price": 12.34, "description": "description test", "max_complements": 3, "category": category.id})
        product1.is_valid()
        product1.save()
        product2 = ProductSerializer(context = {"request": Request()}, data = {"name": "item2", "price": 13.54, "description": "description test", "max_complements": 3, "category": category.id})
        product2.is_valid()
        product2.save()
        complement1 = ComplementSerializer(context = {"request": Request()}, data = {"name": "candy", "categories": [category.id]})
        complement1.is_valid()
        complement1.save()
        complement2 = ComplementSerializer(context = {"request": Request()}, data = {"name": "candy2", "categories": [category.id]})
        complement2.is_valid()
        complement2.save()
    return Data()

# GET ------------------------------------------------------------------
@mark.django_db
def test_GET_all_products_successful(data):
    expected_data = []
    for i in [data.product1, data.product2]:
        expected_data.append(i.data)
    client = APIClient()
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert response.json()["results"] == expected_data

@mark.django_db
def test_GET_specific_product_successful(data):
    expected_data = data.product1.data
    client = APIClient()
    response = client.get("/api/v1/products/1/")
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.django_db
def test_GET_complements_from_specific_product_successful(data):
    expected_data = [data.complement1.data, data.complement2.data]
    client = APIClient()
    response = client.get("/api/v1/products/1/complements/")
    assert response.status_code == 200
    assert response.json() == expected_data
# DELETE ------------------------------------------------------------------
@mark.django_db
def test_DELETE_specific_product_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.delete("/api/v1/products/1/")
    assert response.status_code == 204
# POST ------------------------------------------------------------------
@mark.django_db
def test_POST_product_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    expected_data = data.product1.data
    expected_data["name"] = "item3"
    response = client.post("/api/v1/products/", data = expected_data, format = "json")
    product = ProductSerializer(Product.objects.filter(id = 3).first())
    expected_data = product.data
    assert response.status_code == 201
    assert response.json() == expected_data

@mark.parametrize("field", ["name", "price", "description", "max_complements", "category"])
@mark.django_db
def test_POST_product_failed_required_field(field, data):
    expected_data = data.product1.data
    expected_data["name"] = "item3"
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.post("/api/v1/products/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PUT ------------------------------------------------------------------
@mark.django_db
def test_PUT_product_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/products/1/", data = data.product1.data, format = "json")
    product = ProductSerializer(Product.objects.filter(id = 1).first())
    expected_data = product.data
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.parametrize("field", ["name", "price", "description", "max_complements", "category"])
@mark.django_db
def test_PUT_product_failed_required_field(field, data):
    expected_data = data.product1.data
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/products/1/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PATCH ------------------------------------------------------------------
@mark.django_db
def test_PATCH_product_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.patch("/api/v1/products/1/", data = data.product1.data, format = "json")
    product = ProductSerializer(Product.objects.filter(id = 1).first())
    expected_data = product.data
    assert response.status_code == 200
    assert response.json() == expected_data