const btns = document.querySelectorAll('.order-btn');
btns.forEach(btn => {
  btn.addEventListener('click', () => {
    const food_name = btn.dataset.foodName;
    const food_type = btn.dataset.foodType;
    const date = btn.dataset.date;
    const user_name = btn.dataset.userName;
    const address = btn.dataset.userAddress;
    const account = btn.dataset.account;

    btn.innerText = '⏳ Ordering... ⏳'
    btn.style.backgroundColor = 'yellow'

    fetch('/order', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: 'include',
      body: JSON.stringify({ food_name, food_type, date, user_name, address, account })
    })
    .then(res => res.json())
    .then(data => {
      if (!data.error) {
        btn.innerText = '✅ Ordered ✅';
        btn.style.backgroundColor = 'green';
        btn.disabled = true;

        btn.style.transform = 'scale(1.05)';
        btn.style.transition = 'all 0.3s ease';
        setTimeout(() => {
          btn.style.transform = 'scale(1)';
        }, 150);
      } else {
        btn.innerText = '❌ Not Ordered ❌';
        btn.style.backgroundColor = 'red';
      }

      alert(data.message);
    })
    .catch(err => {
      console.error("Order failed:", err);
      btn.innerText = '❌ Error ❌';
      btn.style.backgroundColor = 'red';
    });
  });
});
