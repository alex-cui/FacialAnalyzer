const ub = document.getElementById("upload-button");
ub.addEventListener("click", uploadImage, false);

function uploadImage() {
    document.getElementById("hidden-button").click();
}