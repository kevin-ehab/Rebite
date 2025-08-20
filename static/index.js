function explore() {
    fetch('/explore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: null
    })
    .then(res => res.json())
    .then(data => {
        console.log("Python returned:", data.message);
        window.location = '/options'
    });
}
