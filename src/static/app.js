document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const confirmationSnackbar = document.getElementById("confirmation-snackbar");
  const snackbarMessage = document.getElementById("snackbar-message");
  const snackbarCancel = document.getElementById("snackbar-cancel");
  const snackbarConfirm = document.getElementById("snackbar-confirm");

  let pendingRemoval = null;

  function showConfirmationSnackbar(activity, email) {
    pendingRemoval = { activity, email };
    snackbarMessage.textContent = `Remove ${email} from ${activity}?`;
    confirmationSnackbar.classList.add("open");
    confirmationSnackbar.classList.remove("closing", "hidden");
  }

  function hideConfirmationSnackbar() {
    confirmationSnackbar.classList.add("closing");
    setTimeout(() => {
      confirmationSnackbar.classList.add("hidden");
      confirmationSnackbar.classList.remove("open", "closing");
      pendingRemoval = null;
    }, 300);
  }

  snackbarCancel.addEventListener("click", hideConfirmationSnackbar);

  snackbarConfirm.addEventListener("click", async () => {
    if (!pendingRemoval) return;

    const { activity, email } = pendingRemoval;
    hideConfirmationSnackbar();

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/participants?email=${encodeURIComponent(email)}`,
        { method: "DELETE" }
      );
      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "Unable to remove participant";
        messageDiv.className = "error";
      }
    } catch (error) {
      messageDiv.textContent = "Failed to unregister participant.";
      messageDiv.className = "error";
      console.error("Error removing participant:", error);
    }

    messageDiv.classList.remove("hidden");
    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  });

  // Function to fetch activities from API

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and dropdown options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        const participantList = details.participants.length
          ? `<ul class="participant-list">${details.participants.map((email) => `<li><span class="participant-email">${email}</span><button type="button" class="participant-remove" data-activity="${encodeURIComponent(name)}" data-email="${encodeURIComponent(email)}" aria-label="Remove ${email}">&times;</button></li>`).join("")}</ul>`
          : `<p class="no-participants">No sign-ups yet. Be the first!</p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants">
            <p class="participants-title">Participants</p>
            ${participantList}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        activityCard.querySelectorAll(".participant-remove").forEach((button) => {
          button.addEventListener("click", (event) => {
            event.preventDefault();

            const activity = decodeURIComponent(button.dataset.activity);
            const email = decodeURIComponent(button.dataset.email);
            showConfirmationSnackbar(activity, email);
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
