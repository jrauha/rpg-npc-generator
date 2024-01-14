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

      if (response.status === 201) {
        window.location.href = response.headers.get("Location");
        return;
      }
      throw new Error("Something went wrong.");
    } catch (error) {
      displayError(
        "<strong>Error!</strong> Something went wrong. Please try again later."
      );
    } finally {
      $submitButton.disabled = false;
      $submitButton.classList.remove("is-loading");
    }
  });
});
