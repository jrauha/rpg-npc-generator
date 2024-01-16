document.addEventListener("DOMContentLoaded", () => {
  const $form = document.getElementById("character-form");
  const $submitButton = $form.querySelector('button[type="submit"]');

  const displayError = (message) => {
    // Remove any previous error messages
    const existing = document.getElementById("generate-error-message");
    if (existing) {
      existing.remove();
    }

    const notification = document.createElement("div");
    notification.id = "generate-error-message";
    notification.classList.add("notification", "is-danger", "mt-3");
    notification.innerHTML = message;
    $form.append(notification);
  };

  const maxPollCount = 20;

  $form.addEventListener("submit", async (event) => {
    event.preventDefault();

    $submitButton.classList.add("is-loading");
    $submitButton.disabled = true;

    try {
      const response = await fetch($form.action, {
        method: "POST",
        body: new FormData($form),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await response.json();

      const taskEndpoint = `/generate/${data.task_id}`;
      let pollCount = 0;

      const poll = async () => {
        const taskResponse = await fetch(taskEndpoint);
        const taskData = await taskResponse.json();

        if (taskData.ready) {
          if (taskData.successful) {
            window.location.href = `/generate?character_id=${taskData.value}`;
            return;
          }
          throw new Error("Character generation task failed");
        }

        pollCount++;
        if (pollCount >= maxPollCount) {
          throw new Error("Character generation task took too long");
        }

        // Retry after 3 seconds if the task is still in progress
        setTimeout(poll, 3000);
      };
      poll();
    } catch (error) {
      console.error(error);
      $submitButton.disabled = false;
      $submitButton.classList.remove("is-loading");
      displayError(
        "<strong>Error!</strong> Something went wrong. Please try again later."
      );
    }
  });
});
