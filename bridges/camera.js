document.querySelector("#btnstart").addEventListener("click", () =>{
    const {PythonShell} = require("python-shell");
    var path = require("path");
    var options = {
        scriptPath : path.join(__dirname, '../systems/')
    }

    var cam = new PythonShell("camera.py", options);

    cam.end(function() {
        console.log('Camera Closed');
    })
})