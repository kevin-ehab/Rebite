function order(food_name, food_type, date, user_name, address, account){
    fetch('/order', {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify({food_name, food_type, date, user_name, address, account})
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message)
    })
}