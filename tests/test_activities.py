import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        ARRANGE: No setup needed
        ACT: Call GET /activities
        ASSERT: Response contains all activities with correct structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) > 0
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        ARRANGE: No setup needed
        ACT: Call GET /activities
        ASSERT: Each activity has required fields
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_shows_participant_count(self, client, reset_activities):
        """
        ARRANGE: No setup needed
        ACT: Call GET /activities
        ASSERT: Participant lists have expected count
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        assert len(activities["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
