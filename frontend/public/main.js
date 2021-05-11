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
    console.log(document.baseURI);

    var image = document.getElementById("img");
    var spinner = document.getElementById("spinner");
    var results = document.getElementById("results");
    var inputImage = document.getElementById("hidden-button");


    image.style.opacity = ".3";
    spinner.style.display = "block";
    results.style.display = "none";

    //delete existing faces
    const allFacesDiv = document.getElementById("allFaces");
    allFacesDiv.innerHTML = '';

console.log(image);
console.log(image.src);
console.log(inputImage);
console.log(inputImage.files[0]);
// console.log(getBase64(inputImage.files[0]));


    getBase64(inputImage.files[0]).then(
        b64 => {
            body = JSON.stringify({img: b64});
        
            //make request here to engine in cloud...
            const Http = new XMLHttpRequest();
            const url = '/detect'; //goes to index.js
            Http.open("POST", url);
            Http.setRequestHeader("Content-Type", "application/json");
            Http.send(body);
            Http.onreadystatechange = (e) => {
                if (Http.readyState == 4 && Http.status == 200) {

                    console.log(Http.responseText);
                    console.log(JSON.parse(Http.responseText));
                    console.log(JSON.parse(Http.responseText).data); //correct

                    let fileNames = (JSON.parse(Http.responseText)).data;

                    for (let f of fileNames) {
                        var img = document.createElement("img");
                        img.src = f;
                        
                        // img.src = "/f" + i + ".png";
                        // img.width = "450";
                        // img.height = "300";

                        // var div = document.createElement("div");
                        // div.appendChild(img);
                        console.log(img);

                        allFacesDiv.appendChild(img);
                    }

                    //stop spinner
                    console.log("setting back");
                    image.style.opacity = "1";
                    spinner.style.display = "none";
                    results.style.display = "block";
                }
            }
        } 
    );

    // setTimeout(function() { 
    //     console.log("setting back");
    //     image.style.opacity = "1";
    //     spinner.style.display = "none";
    //     results.style.display = "block";
    // }, 3000);
}

function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }
