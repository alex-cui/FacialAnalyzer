const ub = document.getElementById("upload-button");
ub.addEventListener("click", uploadImage, false);


function uploadImage() {
    document.getElementById("hidden-button").click();
}

var loadFile = function(event) {
    var output = document.getElementById("img");
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
    results.style.display = "none";
};

var detect = function() {
    var image = document.getElementById("img");
    var spinner = document.getElementById("spinner");
    var results = document.getElementById("results");

    image.style.opacity = ".3";
    spinner.style.display = "block";
    results.style.display = "none";

    //make request here to engine in cloud...

    setTimeout(function() { 
        console.log("setting back");
        image.style.opacity = "1";
        spinner.style.display = "none";
        results.style.display = "block";
    }, 3000);
}