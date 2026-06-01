import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_adds_participant_successfully(self, client, reset_activities):
        """
        ARRANGE: Prepare new participant email
        ACT: Call POST /activities/{activity}/signup
        ASSERT: Participant is added and response is success
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_updates_participant_list(self, client, reset_activities):
        """
        ARRANGE: Prepare new participant email
        ACT: Call POST /activities/{activity}/signup then GET /activities
        ASSERT: Participant appears in activity participant list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newprogrammer@mergington.edu"
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert signup_response.status_code == 200
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_student_returns_400(self, client, reset_activities):
        """
        ARRANGE: Participant already in activity
        ACT: Try to sign up the same student again
        ASSERT: Returns 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        ARRANGE: Prepare email and nonexistent activity name
        ACT: Try to sign up for activity that doesn't exist
        ASSERT: Returns 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_without_email_parameter_fails(self, client, reset_activities):
        """
        ARRANGE: No email parameter provided
        ACT: Call POST without email param
        ASSERT: Request fails with 422 validation error
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code == 422
