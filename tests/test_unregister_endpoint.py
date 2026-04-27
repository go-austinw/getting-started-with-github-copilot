from src import app as app_module


def test_unregister_removes_participant(client):
    email = app_module.activities["Chess Club"]["participants"][0]

    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/participants?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_member(client):
    response = client.delete("/activities/Chess%20Club/participants?email=ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_requires_email_query_param(client):
    response = client.delete("/activities/Chess%20Club/participants")

    assert response.status_code == 422
