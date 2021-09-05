// How often we check if the queue is open
const UPDATE_INTERVAL_SECONDS = 5;

checkQueueIsOpen();
setInterval(checkQueueIsOpen, UPDATE_INTERVAL_SECONDS * 1000);

// Selectors for the <option>s in the modality dropdown
const VIRTUAL_OPTION_SELECT = "#modality option[value='virtual']"
const IN_PERSON_OPTION_SELECT = "#modality option[value='in_person']"

const prettyStatus = (isOpen) => isOpen ? "(Open)" : "(Closed)"

function checkQueueIsOpen() {
    fetch('/queue_status').then(response => response.json())
        .then((data) => {
            // Since we have two queues now, this gets a bit weirder.
            // We'll leave the join button enabled if either queue is open.
            // This means a join request may fail if the "wrong" queue
            // was open, but the backend handles this and an error
            // will be displayed.
            if(data) {
                console.log(data)
                if(data.virtual_open || data.in_person_open) {
                    someQueuesOpen();
                }
                // Displays status of each queue in the dropdown.
                const virtualOption = document.querySelector(VIRTUAL_OPTION_SELECT);
                const inPersonOption = document.querySelector(IN_PERSON_OPTION_SELECT);
                if(virtualOption)
                    virtualOption.textContent = "Virtual " + prettyStatus(data.virtual_open);
                if(inPersonOption)
                    inPersonOption.textContent = "In-Person " + prettyStatus(data.in_person_open);
            }
            else {
                bothQueuesClosed(); 
            }
        })
        .catch((e) => {
            console.log(e);
            bothQueuesClosed();
        })
}

// If the queue is closed we visually disable the submit button,
// queue status is still checked on the back-end since this the
// 'disabled' attribute can be removed
function bothQueuesClosed() {
    const joinButton = document.getElementById('submit-button');
    joinButton.disabled = true;
    joinButton.title = 'The queue is closed.';
}

function someQueuesOpen() {
    const joinButton = document.getElementById('submit-button');
    joinButton.disabled = false;
    joinButton.removeAttribute('title');
}