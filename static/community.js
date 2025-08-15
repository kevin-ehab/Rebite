const btns = document.querySelectorAll('button');

btns.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.innerText = '✅ Ordered ✅';
        btn.style.backgroundColor = 'green';
        btn.style.transform = 'scale(1.05)';
        btn.style.transition = 'all 0.3s ease';
        btn.disabled = true;

        // Slight bounce effect
        setTimeout(() => {
            btn.style.transform = 'scale(1)';
        }, 150);
    });
});

function order(food_name, food_type, date, user_name, address, account) {
    fetch('/order', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ food_name, food_type, date, user_name, address, account })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    });
}
