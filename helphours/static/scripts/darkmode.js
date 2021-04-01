const store = window.localStorage;
const bodyEl = document.getElementById('body');

// Rave variables
let i = 0;
const msPerFrame = 250;
const contentDiv = document.getElementById('body');
const raveDuckImg = '/static/images/rave_duck.gif';
const navDuck = document.getElementById('nav-duck');
const ogDuckImg = navDuck.getAttribute('src');
const amplitude = 100;
const shift = 255 - amplitude;
let step = 1.7 * (msPerFrame / 1000);
let interval = NaN;

let fairyCursor = new FairyDustCursor();

if(store.getItem('raveMode') === 'true') {
    enableRave();
} else {
    disableRave();
}

if (store.getItem('darkMode') === 'true') {
    bodyEl.classList.add('no-transition');
    setDarkMode();
    setTimeout(() => {bodyEl.classList.remove('no-transition')})
    // Don't show a transition when the page loads
} else {
    document.getElementById('dark-mode-moon').style.display = "block";
    document.getElementById('dark-mode-sun').style.display = "none";
}

function toggleDarkMode() {
    if (bodyEl.classList.contains('dark')) {
        // Change to light mode
        setLightMode(); 
    } else {
        // Change to dark mode
        setDarkMode(); 
    }
}

function setLightMode() {
    if(!bodyEl.classList.contains('dark'))
        return;
    store.setItem('darkMode', false)
    document.getElementById('dark-mode-moon').style.display = "block";
    document.getElementById('dark-mode-sun').style.display = "none";
    bodyEl.classList.remove('dark');
}

function setDarkMode() {
    if(bodyEl.classList.contains('dark'))
        return;
    store.setItem('darkMode', true)
    document.getElementById('dark-mode-moon').style.display = "none";
    document.getElementById('dark-mode-sun').style.display = "block";
    bodyEl.classList.add('dark');
    disableRave();
}



function toggleRaveMode() {
    let bodyEl = document.getElementById('body');
    bodyEl.classList.toggle('rave');
    if (bodyEl.classList.contains('rave')) {
       enableRave();
    } else {
        disableRave(); 
    }
}


function enableRave() {
    if(interval != NaN)
        window.clearInterval(interval);
        store.setItem('raveMode', true);
    interval = window.setInterval(() => {
            // Idea here comes from lolcat: https://github.com/busyloop/lolcat
            let red = Math.sin(step * i + 0) * amplitude + shift;
            let green = Math.sin(step * i + 2.0 * Math.PI / 3) * amplitude + shift;
            let blue = Math.sin(step * i + 4.0 * Math.PI / 3) * amplitude + shift;
            contentDiv.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`
            i++;
    }, msPerFrame);
    navDuck.setAttribute('src', raveDuckImg);
    const leftHomeDuck = document.getElementById('left-home-duck');
    if(leftHomeDuck){
        leftHomeDuck.setAttribute('src', raveDuckImg);
        const rightHomeDuck = document.getElementById('right-home-duck');
        if(rightHomeDuck){
            // should always be !null
            rightHomeDuck.setAttribute('src', raveDuckImg);
        }
    }
    setLightMode();
    fairyCursor.resumeEffect();
}

function disableRave() {
    if(interval == NaN)
        return;
    store.setItem('raveMode', false);
    contentDiv.style.backgroundColor = "";
    window.clearInterval(interval);
    navDuck.setAttribute('src', ogDuckImg);
    const leftHomeDuck = document.getElementById('left-home-duck');
    if(leftHomeDuck){
        leftHomeDuck.setAttribute('src', ogDuckImg);
        const rightHomeDuck = document.getElementById('right-home-duck');
        if(rightHomeDuck){
            // should always be !null
            rightHomeDuck.setAttribute('src', ogDuckImg);
        }
    }
    interval = NaN;
    fairyCursor.pauseEffect();
}

