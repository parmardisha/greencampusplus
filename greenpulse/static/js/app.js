const categorySelect = document.querySelector("#category");
const activityForm = document.querySelector("#activity-form");
const formMessage = document.querySelector("#form-message");

function formatNumber(value) {
  return Number(value || 0).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatDate(value) {
  const date = new Date(value);
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(date);
}

async function request(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.error || "Something went wrong. Please try again.");
  }
  return response.status === 204 ? null : response.json();
}

function renderActivities(activities, categories) {
  const list = document.querySelector("#activity-list");
  document.querySelector("#recent-count").textContent =
    `${activities.length} ${activities.length === 1 ? "entry" : "entries"}`;

  if (activities.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon" aria-hidden="true">✳</span>
        <h3>Your story starts here</h3>
        <p>Log your first activity to see your impact take shape.</p>
      </div>`;
    return;
  }

  list.replaceChildren(
    ...activities.map((activity) => {
      const category = categories[activity.category];
      const item = document.createElement("div");
      item.className = "activity-item";

      const symbol = document.createElement("span");
      symbol.className = "activity-symbol";
      symbol.setAttribute("aria-hidden", "true");
      symbol.textContent = category.icon;

      const name = document.createElement("div");
      name.className = "activity-name";
      const title = document.createElement("strong");
      title.textContent = activity.description;
      const details = document.createElement("span");
      details.textContent =
        `${category.label} · ${formatNumber(activity.amount)} ${category.unit} · ${formatDate(activity.created_at)}`;
      name.append(title, details);

      const emissions = document.createElement("span");
      emissions.className = "activity-emissions";
      emissions.append(
        document.createTextNode(formatNumber(activity.emissions_kg)),
      );
      const unit = document.createElement("small");
      unit.textContent = " kg";
      emissions.append(unit);

      const remove = document.createElement("button");
      remove.className = "delete-button";
      remove.type = "button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Delete ${activity.description}`);
      remove.addEventListener("click", async () => {
        remove.disabled = true;
        try {
          await request(`/api/activities/${activity.id}`, { method: "DELETE" });
          await loadDashboard();
        } catch (error) {
          remove.disabled = false;
          showMessage(error.message);
        }
      });

      item.append(symbol, name, emissions, remove);
      return item;
    }),
  );
}

async function loadDashboard() {
  const data = await request("/api/dashboard");
  document.querySelector("#total-emissions").textContent =
    formatNumber(data.summary.total_kg);
  document.querySelector("#activity-count").textContent =
    data.summary.activity_count.toLocaleString();
  document.querySelector("#average-emissions").textContent =
    formatNumber(data.summary.average_kg);
  renderActivities(data.activities, data.categories);
}

function showMessage(message, success = false) {
  formMessage.textContent = message;
  formMessage.classList.toggle("success", success);
}

categorySelect.addEventListener("change", () => {
  const unit = categorySelect.selectedOptions[0].textContent.includes("Electricity") ||
    categorySelect.selectedOptions[0].textContent.includes("Natural gas")
    ? "kWh"
    : "km";
  document.querySelector("#unit-label").textContent = `(${unit})`;
});

activityForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = activityForm.querySelector("button[type=submit]");
  const data = new FormData(activityForm);
  submitButton.disabled = true;
  showMessage("");

  try {
    await request("/api/activities", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: data.get("description"),
        category: data.get("category"),
        amount: data.get("amount"),
      }),
    });
    activityForm.reset();
    categorySelect.dispatchEvent(new Event("change"));
    showMessage("Activity added to your log.", true);
    await loadDashboard();
  } catch (error) {
    showMessage(error.message);
  } finally {
    submitButton.disabled = false;
  }
});

loadDashboard().catch((error) => {
  showMessage(error.message);
});
