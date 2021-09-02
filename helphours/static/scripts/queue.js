// How many seconds we should wait before polling the server again
const UPDATE_INTERVAL_SECONDS = 10;

// After 120 minutes of not refreshing the page or clicking any buttons
// stop making requests to the API
const TIMEOUT_MINUTES = 120;

// Hold previous fetch result, if it's the same, don't bother re-rendering
var lastPullResponse;

// Hold the states of dropdown menus for when we refresh
var dropDownStates = {};

// Fetch the queue when the page loads
updateQueue();

var updateInterval = setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);

const store1 = window.localStorage;
var viewStateMap = new Map();

viewStateMap['remote'] = store1.getItem('remote') == null ? true : store1.getItem('remote') == 'true';
viewStateMap['in_person'] = store1.getItem('in_person') == null ? true : store1.getItem('in_person') == 'true';

document.getElementById("virtual-queue").checked = viewStateMap['remote'];
document.getElementById("in-person-queue").checked = viewStateMap['in_person'];

store1.setItem('remote', viewStateMap['remote']);
store1.setItem('in_person', viewStateMap['in_person']);

var checkboxesChanged = false;

// After TIMEOUT_MINUTES, stop retrieving the queue; the client is probably
// idle or left the page open accidentally
setTimeout(() => {
    clearInterval(updateInterval);
    clearQueue();
    displayMessage('Connection timed out, refresh the page.')
}, TIMEOUT_MINUTES * 60 * 1000);


// Fetches the new queue and updates the page
function updateQueue() {
    fetch('/queue').then(response => response.json())
        .then(renderQueue)
        .catch((e) => {
            clearQueue();
            displayMessage('Couldn\'t connect to the server to retrieve the queue.');
            console.log(e);
        });
}

// Given the queue in JSON form, will parse the queue object and 
// update the page if necessary.
function renderQueue(data) {
    let dataJSON = JSON.stringify(data);
    if (lastPullResponse === dataJSON && !checkboxesChanged) {
        // Nothing changed, don't bother re-rendering
        return;
    }

    // Queue changed, let's re-render and save this result
    clearQueue();
    lastPullResponse = dataJSON;

    let queue = data.queue.filter(entry => viewStateMap[entry.modality]);

    if (!queue || queue.length === 0) {
        displayMessage('The queue is empty.');
    } else {
        let queueContainer = document.getElementById("queue");
        let template = document.getElementById("queue-entry-template");
        let newDropDownStates = {};

        for (let i = 0; i < queue.length; i++) {
            let newEntry = template.content.cloneNode(true);

            // Add this person's place in line and name
            newEntry.querySelector('.queue-entry-position').textContent = queue[i].position + ":";
            newEntry.querySelector('.queue-entry-name').textContent = queue[i].name;
           
            // Display modality for entry
            const modalities = {
                'remote': "Remote",
                'in_person': "In Person"
            };
            const modalityDisplay = modalities[queue[i].modality];
            if(modalityDisplay)
                newEntry.querySelector('.queue-entry-modality').textContent = `(${modalityDisplay})`;
            else
                newEntry.querySelector('.queue-entry-modality').style.display = 'none';

            if ("id" in queue[i]) {
                // If the id of the student is present, then we are authenticated as an
                // instructor, so prepare all other instructor-only fields
                newEntry.querySelector('.queue-entry-expanded-desc').textContent = queue[i].desc;
                newEntry.querySelector('.queue-entry-expanded-time').textContent = queue[i].time;
                // Assing this entry's id so we know who was helped/removed
                newEntry.querySelectorAll('button').forEach(button =>
                    button.value = queue[i].id
                );
                // Retrieve the DOM nodes from the fragment
                let entry = Array.prototype.slice.call(newEntry.childNodes)[1];

                // Add event listener and pointer cursor to dropdown toggle
                let expandToggle = entry.querySelector('.queue-entry-expand-toggle');
                expandToggle.addEventListener('click', () => { toggleExpanded(entry, queue[i].id) });
                expandToggle.style.cursor = 'pointer';

                // Restore previous dropdown states
                if (queue[i].id in dropDownStates && dropDownStates[queue[i].id]) {
                    entry.querySelector('.queue-entry-box').classList.toggle('active');
                    entry.querySelector('.queue-entry-expanded').classList.toggle('active');
                    newDropDownStates[queue[i].id] = true;
                } else {
                    newDropDownStates[queue[i].id] = false;
                }
            } else {
                // We aren't authenticated, so hide all the unnecessary DOM elements
                // (Besides, the buttons won't even be hooked up to anything)
                newEntry.querySelectorAll('button').forEach(button =>
                    button.style.display = 'none'
                );
                newEntry.querySelector('.queue-chevron').style.display = 'none';
            }
            // We're done filling all the necessary fields, add this entry into
            // the queue div on the page
            queueContainer.appendChild(newEntry);
        }
        dropDownStates = newDropDownStates;
    }

    checkboxesChanged = false;
}

// Gets rid of all entries in the queue div
function clearQueue() {
    let queue = document.getElementById("queue");
    if (queue)
        while (queue.firstChild)
            queue.removeChild(queue.firstChild)
}

// Instead of displaying queue entries in the queue, displays a message
// (either error message or "queue is empty" message)
function displayMessage(content) {
    let message = document.getElementById('queue-message').content.cloneNode(true);
    message.querySelector('.queue-message').textContent = content;
    document.getElementById('queue').appendChild(message);
}

// Function which will toggle whether the entry accordion is open
function toggleExpanded(queueEntry, entryId) {
    queueEntry.querySelector('.queue-entry-box').classList.toggle('active');
    queueEntry.querySelector('.queue-entry-expanded').classList.toggle('active');
    dropDownStates[entryId] = !dropDownStates[entryId];
}

function setCheckbox(queue) {
    viewStateMap[queue] = !viewStateMap[queue];
    store1.setItem(queue, viewStateMap[queue]);
    checkboxesChanged = true;
    updateQueue();
}