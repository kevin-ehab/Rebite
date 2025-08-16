function submit(event) {
  let form = new FormData()

  let name = document.getElementById('name').value
  form.append('name', name)

  let type = document.getElementById('type').value
  form.append('type', type)

  let date = document.getElementById('date').value
  form.append('date', date)
  let image = document.getElementById('image').files[0]
  form.append('image', image)
  if (!image){
    alert('You need to choose an image.')
    return
  }
  fetch('/logging_waste2', {
    method: "POST",
    credentials: 'include',
    body: form
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
  })
  alert("Food posted!")
  window.location = '/options'
}