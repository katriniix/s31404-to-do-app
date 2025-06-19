const dateInput = document.getElementById("day");
const taskList = document.getElementById("list");
const addButton = document.getElementById("addBtn");

const modal = document.getElementById("modal");
const titleInput = document.getElementById("task-title");
const colorToggle = document.getElementById("color-toggle");
const colorLabel = document.getElementById("color-label");
const colorPicker = document.getElementById("task-color");
const saveButton = document.getElementById("save-task");

colorToggle.onchange = () => {
  colorLabel.classList.toggle("hidden", !colorToggle.checked);
};
dateInput.value = new Date().toISOString().slice(0, 10);
loadTasks();

dateInput.onchange = loadTasks;
addButton.onclick = openModal;
saveButton.onclick = saveTask;
modal.onclick = (e) => { if (e.target === modal) closeModal(); };

function openModal() {
  titleInput.value = "";
  colorToggle.checked = false;
  colorLabel.classList.add("hidden");
  colorPicker.value = "#33aaff";
  modal.classList.remove("hidden");
  titleInput.focus();
}

function closeModal() {
  modal.classList.add("hidden");
}

function saveTask() {
  const title = titleInput.value.trim();
  if (!title) {
    return;
  }
  const payload = {
    title: title,
    color: colorToggle.checked ? colorPicker.value : "",
    date: dateInput.value
  };

  fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(response => response.ok && response.json())
  .then(() => {
    closeModal();
    loadTasks();
  });
}

function loadTasks() {
  fetch(`/api/tasks?date=${dateInput.value}`)
    .then(response => response.json())
    .then(taskArray => {
      taskList.innerHTML = "";
      taskArray.forEach(task => {
        const row = document.createElement("div");
        row.className = "task";

        const taskColor = task.color || "";
        row.innerHTML = `
          <input type="checkbox" ${task.done ? "checked" : ""}>
          <span class="task-tag ${taskColor ? "" : "no-color"}" style="background:${taskColor}">
            ${task.title}
          </span>`;

        row.querySelector("input").onchange = (e) =>
          fetch(`/api/tasks/${task._id}/toggle`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ done: e.target.checked })
          }).then(loadTasks);

        taskList.appendChild(row);
      });
    });
}
