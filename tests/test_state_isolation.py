def test_state_mutation_is_local_to_test(client):
    response = client.post("/activities/Chess%20Club/signup?email=isolation.check@mergington.edu")

    assert response.status_code == 200



def test_state_resets_between_tests(client):
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]

    assert "isolation.check@mergington.edu" not in participants
