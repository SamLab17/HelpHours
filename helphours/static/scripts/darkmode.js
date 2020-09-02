let store = window.localStorage;
if (store.getItem('darkMode') === 'true') {
    let bodyEl = document.getElementById('body');
    bodyEl.className = 'dark';
}

function toggleDarkMode() {
    let bodyEl = document.getElementById('body');
    let store = window.localStorage;
    if (bodyEl.className === 'dark') {
        // Make light mode
        // bodyEl.style.backgroundColor = 'inherit';
        // bodyEl.style.color = 'inherit';
        bodyEl.className = '';
        store.setItem('darkMode', false)
        console.log('set to false')
    } else {
        // bodyEl.style.backgroundColor = '#222';
        // bodyEl.style.color = '#fff';
        bodyEl.className = 'dark';
        store.setItem('darkMode', true)
        // console.log('set to true')
    }
}