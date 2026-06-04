def test_signup_unknown_activity_returns_404(client, activity_segment):
    response = client.post(
        f"/activities/{activity_segment('Unknown Club')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_student_returns_400(client, activity_segment):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_segment(activity_name)}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_unregister_unknown_activity_returns_404(client, activity_segment):
    response = client.post(
        f"/activities/{activity_segment('Unknown Club')}/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_participant_returns_400(client, activity_segment):
    activity_name = "Science Club"
    email = "not.registered@mergington.edu"

    response = client.post(
        f"/activities/{activity_segment(activity_name)}/unregister",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not registered for this activity"
    }
