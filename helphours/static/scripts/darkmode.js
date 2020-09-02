let store = window.localStorage;
if (store.getItem('darkMode') === 'true') {
    let bodyEl = document.getElementById('body');
    bodyEl.classList.add('dark');

    // Don't show a transition when the page loads
    bodyEl.classList.add('no-transition');
    setTimeout(() => {bodyEl.classList.remove('no-transition')})

    document.getElementById('dark-mode-toggle').textContent = "Light Mode";
}

function toggleDarkMode() {
    let bodyEl = document.getElementById('body');
    let store = window.localStorage;
    if (bodyEl.classList.contains('dark')) {
        bodyEl.className = '';
        store.setItem('darkMode', false)
        console.log('set to false')
        document.getElementById('dark-mode-toggle').textContent = "Dark Mode";
    } else {
        bodyEl.className = 'dark';
        store.setItem('darkMode', true)
        document.getElementById('dark-mode-toggle').textContent = "Light Mode";
    }
}