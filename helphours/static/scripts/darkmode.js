let store = window.localStorage;
if (store.getItem('darkMode') === 'true') {
    let bodyEl = document.getElementById('body');
    bodyEl.className = 'dark';
    document.getElementById('dark-mode-toggle').textContent = "Light Mode";
}

function toggleDarkMode() {
    let bodyEl = document.getElementById('body');
    let store = window.localStorage;
    if (bodyEl.className === 'dark') {
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