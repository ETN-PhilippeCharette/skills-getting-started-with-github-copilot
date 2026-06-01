import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants endpoint"""

    def test_remove_participant_successfully(self, client, reset_activities):
        """
        ARRANGE: Participant exists in activity
        ACT: Call DELETE /activities/{activity}/participants
        ASSERT: Participant is removed and response is success
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    def test_remove_participant_updates_list(self, client, reset_activities):
        """
        ARRANGE: Participant exists in activity
        ACT: Call DELETE then GET /activities
        ASSERT: Participant no longer in participant list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        delete_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert delete_response.status_code == 200
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_nonexistent_participant_returns_404(self, client, reset_activities):
        """
        ARRANGE: Email not in activity
        ACT: Try to remove participant that doesn't exist
        ASSERT: Returns 404 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notexist@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_remove_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        ARRANGE: Activity doesn't exist
        ACT: Try to remove participant from nonexistent activity
        ASSERT: Returns 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_without_email_parameter_fails(self, client, reset_activities):
        """
        ARRANGE: No email parameter provided
        ACT: Call DELETE without email param
        ASSERT: Request fails with 422 validation error
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants")
        
        # Assert
        assert response.status_code == 422
