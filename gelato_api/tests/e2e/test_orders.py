from pytest import mark, fixture
from rest_framework.test import APIClient
from gelato_api.models import User, Order
from gelato_api.serializers import OrderSerializer

@fixture
def data():
    class Data():
        normal_user = User.objects.create_user(email="normal@user.com", password="12345", first_name="Normal", last_name="User")
        staff_user = User.objects.create_user(email="staff@user.com", password="12345", first_name="Staff", last_name="User", is_staff = True)
        superuser = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")
        class Request():
            user = User.objects.filter(email="super@user.com").first()
        order1 = OrderSerializer(context = {"request": Request()}, data = {"comment": "1x Ice Cream 700ml", "delivery": False, "location": "location_test"})
        order1.is_valid()
        order1.save()
        order2 = OrderSerializer(context = {"request": Request()}, data = {"comment": "2x Ice Cream 700ml", "delivery": False, "location": "location_test2"})
        order2.is_valid()
        order2.save()
    return Data()

# GET ------------------------------------------------------------------
@mark.django_db
def test_GET_all_orders_successful(data):
    expected_data = []
    for i in [data.order1, data.order2]:
        expected_data.append(i.data)
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.get("/api/v1/orders/")
    assert response.status_code == 200
    assert response.json()["results"] == expected_data

@mark.django_db
def test_GET_specific_order_successful(data):
    expected_data = data.order1.data
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.get("/api/v1/orders/1/")
    assert response.status_code == 200
    assert response.json() == expected_data
# DELETE ------------------------------------------------------------------
@mark.django_db
def test_DELETE_specific_order_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.superuser)
    response = client.delete("/api/v1/orders/1/")
    assert response.status_code == 204
# POST ------------------------------------------------------------------
@mark.django_db
def test_POST_order_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.normal_user)
    response = client.post("/api/v1/orders/", data = data.order1.data, format = "json")
    order = OrderSerializer(Order.objects.filter(id = 3).first())
    expected_data = order.data
    assert response.status_code == 201
    assert response.json() == expected_data

@mark.parametrize("field", ["comment", "delivery", "location"])
@mark.django_db
def test_POST_order_failed_required_field(field, data):
    expected_data = data.order1.data
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.normal_user)
    response = client.post("/api/v1/orders/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PUT ------------------------------------------------------------------
@mark.django_db
def test_PUT_order_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/orders/1/", data = data.order1.data, format = "json")
    order = OrderSerializer(Order.objects.filter(id = 1).first())
    expected_data = order.data
    assert response.status_code == 200
    assert response.json() == expected_data

@mark.parametrize("field", ["comment", "delivery", "location"])
@mark.django_db
def test_PUT_order_failed_required_field(field, data):
    expected_data = data.order1.data
    del(expected_data[field])
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.put("/api/v1/orders/1/", data = expected_data, format = "json")
    assert response.status_code == 400
    assert list(response.json().keys()) == [field]
# PATCH ------------------------------------------------------------------
@mark.django_db
def test_PATCH_successful(data):
    client = APIClient()
    client.force_authenticate(user = data.staff_user)
    response = client.patch("/api/v1/orders/1/", data = data.order1.data, format = "json")
    order = OrderSerializer(Order.objects.filter(id = 1).first())
    expected_data = order.data
    assert response.status_code == 200
    assert response.json() == expected_data