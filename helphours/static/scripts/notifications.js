// How often (in seconds) we check if we're up next
const NOTIFICATION_CHECK_INTERVAL = 1;


const cookies = Object.fromEntries(document.cookie.split('; ').map(c => c.split('=')))

console.log("cookies!")
console.log(cookies)

if(cookies['join_token']) {
    // Request notification access

    Notification.requestPermission().then(console.log)
    // set up interval to check w/ backend
    const token = cookies['join_token']

    const handle = setInterval(() => {

        console.log("checking position")
        fetch('/check_position_for?' + new URLSearchParams({
            join_token: token
        })).then(d => d.json()).then(resp => {
            const pos = resp['position']
            if(pos == -1) {
                // No longer in the queue
                console.log('no longer in queue')
                clearTimeout(handle)
            }

            if(pos == 1) {
                // Up next
                // show notifiaction
                console.log("we're up next!")
            }
        })

    }, NOTIFICATION_CHECK_INTERVAL * 1000)
}