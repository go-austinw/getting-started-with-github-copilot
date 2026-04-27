def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    expected_activities = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Band",
        "Debate Club",
        "Science Club",
    }
    assert expected_activities.issubset(set(data.keys()))

    for _, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
