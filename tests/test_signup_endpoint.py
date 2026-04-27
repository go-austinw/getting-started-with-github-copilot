from src import app as app_module


def test_signup_adds_new_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_registration(client):
    existing_email = app_module.activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_requires_email_query_param(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_signup_currently_allows_exceeding_capacity(client):
    activity = app_module.activities["Chess Club"]
    capacity = activity["max_participants"]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(capacity)]

    extra_email = "overflow.student@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={extra_email}")

    assert response.status_code == 200
    assert extra_email in app_module.activities["Chess Club"]["participants"]
    assert len(app_module.activities["Chess Club"]["participants"]) == capacity + 1
