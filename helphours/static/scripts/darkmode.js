const store = window.localStorage;

if (store.getItem('darkMode') === 'true') {
    let bodyEl = document.getElementById('body');
    bodyEl.classList.add('dark');
    store.setItem('darkMode', true)
    document.getElementById('dark-mode-moon').style.display = "none";
    document.getElementById('dark-mode-sun').style.display = "block";
    // Don't show a transition when the page loads
    bodyEl.classList.add('no-transition');
    setTimeout(() => {bodyEl.classList.remove('no-transition')})
} else {
    document.getElementById('dark-mode-moon').style.display = "block";
    document.getElementById('dark-mode-sun').style.display = "none";
}

function toggleDarkMode() {
    let bodyEl = document.getElementById('body');
    if (bodyEl.classList.contains('dark')) {
        // Change to light mode
        bodyEl.className = '';
        store.setItem('darkMode', false)
        document.getElementById('dark-mode-moon').style.display = "block";
        document.getElementById('dark-mode-sun').style.display = "none";
    } else {
        // Change to dark mode
        bodyEl.className = 'dark';
        store.setItem('darkMode', true)
        document.getElementById('dark-mode-moon').style.display = "none";
        document.getElementById('dark-mode-sun').style.display = "block";
    }
}