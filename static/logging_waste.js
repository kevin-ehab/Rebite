function submit(event) {
  const name = document.getElementById('name').value;
  const type = document.getElementById('type').value;
  const date = document.getElementById('date').value;

  fetch('/logging_waste2', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, type, date })
  })
  .then(response => response.json())
  .then(data => {
    alert("Food posted!");
    console.log(data);
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Failed to submit food waste.");
  });
}