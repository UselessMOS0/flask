const now = new Date()
const end = new Date(2022,6,8)

function cd() {
    let delta = end - now
    document.getElementById('time').innerHTML = `${Math.floor(delta / 86400000)} days, ${Math.floor(delta % 86400000 / 3600000)} hours and ${Math.floor(delta % 86400000 % 3600000 / 60000)} minutes left until the end of school`
}

cd()
setInterval(cd,20000)

