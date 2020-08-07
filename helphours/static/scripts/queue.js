var UPDATE_INTERVAL_SECONDS = 5;

updateQueue();
setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);


function updateQueue(){
    fetch('/queue').then(response => response.json()).then(renderQueue)
}

function renderQueue(data) {
    var output = '';
    var queue = data.queue
    if(queue.length === 0){
        output = '<p style="text-align: center;"> The Queue is empty. </p>';
    }
    else {
        for(var i = 0; i < queue.length; i++){
            output += '<div class="queue-entry"><div class="queue-entry-left"><div class="queue-entry-position">'
            output += queue[i].position
            output += '</div><div class="queue-entry-name">'
            output += queue[i].name
            output += '</div></div></div>'
        }
    }
    document.getElementById('queue').innerHTML = output;
}