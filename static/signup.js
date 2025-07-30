function signUp(){
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    const name = document.getElementById('name').value
    const address = document.getElementById('address').value
    fetch('/signup2', {
        method: ['Post'],
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password, address, name})
    })
    .then(res => res.json())
    .then(data =>{
        alert(data.message)
        if (data.redirect === 1){
            window.location = '/options'
        }else if (data.redirect === 2){
            window.location = '/login'
        }
    })
}