import src.app as app_module


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert set(payload.keys()) == set(app_module.activities.keys())

    sample_activity = payload["Chess Club"]
    assert set(sample_activity.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_signup_adds_student_to_activity(client, activity_segment):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{activity_segment(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in app_module.activities[activity_name]["participants"]


def test_unregister_removes_student_from_activity(client, activity_segment):
    activity_name = "Debate Team"
    email = "noah@mergington.edu"

    response = client.post(
        f"/activities/{activity_segment(activity_name)}/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in app_module.activities[activity_name]["participants"]
