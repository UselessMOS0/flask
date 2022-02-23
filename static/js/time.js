function time() {
    let now = new Date();
    document.getElementById('time').innerHTML = `${now.getHours().toString().length < 2 ? "0" + now.getHours() : now.getHours()} : ${now.getMinutes().toString().length < 2 ? "0" + now.getMinutes() : now.getMinutes()} :  ${now.getSeconds().toString().length < 2 ? "0" + now.getSeconds() : now.getSeconds()}`
}

setInterval(time, 50) /// setInterval(funzione, millisecondi, parametro1(della funzione), parametro2, ...)