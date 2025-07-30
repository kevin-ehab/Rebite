function login(){
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    fetch('/login2', {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify({ email , password})
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message)
        if (data.redirect){
            window.location = '/options'
        }
    })
}