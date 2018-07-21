var d = new Date();
document.getElementById("demo").innerHTML = d;

var utc = new Date().toJSON().slice(0,10).replace(/-/g,'/');
document.write(utc);
