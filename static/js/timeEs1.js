const now = new Date()
const end = new Date("2022/6/8")
console.log(end.getMonth());

function cd() {
    let delta = end - now
    document.getElementById('time').innerHTML = `${Math.floor(delta / 86400000)} days, ${Math.floor(delta % 86400000 / 3600000)} hours and ${Math.floor(delta % 86400000 % 3600000 / 60000)} minutes left until the end of school`
    console.log(delta)
}

cd()
setInterval(cd,20000)

