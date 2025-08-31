
from app.models import Group

def test_get_group_by_uni_id(client, sc_with_multiple_groups, auth):
    scenario = sc_with_multiple_groups
    university1 = scenario["university1"]
    group_from_university1 = scenario["groups_from_university1"]
    user, password = scenario["user"]
    auth.login_via_endpoint(client, email=user.email, password=password)
    endpoint_path = "/api/group/"
    response = client.get(endpoint_path)
    assert response.status_code == 200
    response_data = response.json()

    assert len(response_data) == len(group_from_university1)
    assert all(item["university_id"] == university1.id for item in response_data)


def test_create_group(client, sc_with_multiple_groups, auth):
    scenario = sc_with_multiple_groups
    user, password = scenario["user"]
    auth.login_via_endpoint(client, email=user.email, password=password)
    endpoint_path = "/api/group/"
    create_group_data = {
        "group_name": "Test added group",
    }
    response = client.post(endpoint_path, json=create_group_data)
    assert response.status_code == 201
    
    get_groups_by_uni_id_response = client.get(endpoint_path)
    assert get_groups_by_uni_id_response.status_code == 200
    response_get_groups_data = get_groups_by_uni_id_response.json()
    assert any(item["group_name"] == create_group_data["group_name"] for item in response_get_groups_data)  # check if at least one group with the same name exists


def test_delete_group(client, sc_with_multiple_groups, auth):
    scenario = sc_with_multiple_groups
    user, password = scenario["user"]
    auth.login_via_endpoint(client, email=user.email, password=password)
    groups = scenario["groups_from_university1"]
    endpoint_path = "/api/group/"
    response = client.delete(f"{endpoint_path}{groups[1].id}/") #Tutaj jest błąd (grupa ma zależności)
    assert response.status_code == 204
    #check if the group0 was actually deleted
    get_groups_by_uni_id_response = client.get(endpoint_path)
    assert get_groups_by_uni_id_response.status_code == 200
    response_get_groups_data = get_groups_by_uni_id_response.json()
    assert not any(d["id"] == groups[1].id for d in response_get_groups_data)  # check if at least one group with the same id exists
    

