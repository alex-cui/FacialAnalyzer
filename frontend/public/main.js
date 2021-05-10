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
    var inputImage = document.getElementById("hidden-button");


    image.style.opacity = ".3";
    spinner.style.display = "block";
    results.style.display = "none";

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
                console.log(Http.responseText);
            }
        } 
    );


    // const url='https://jsonplaceholder.typicode.com/posts';
    // const url='https://10.10.1.1:6443/api/v1/namespaces/kube-system/services/hello-world/proxy/10.244.1.44:8080';

    // body = JSON.stringify({img: image.src});








//     alexcui@node0:/mydata$ kubectl get pods
// NAME                                         READY   STATUS    RESTARTS   AGE
// curl                                         1/1     Running   1          8h
// hello-world-59966754c9-5qgll                 1/1     Running   0          6h14m
// hello-world-59966754c9-l9d7t                 1/1     Running   0          6h14m
// my-nginx-5b56ccd65f-4x89p                    1/1     Running   0          7h48m
// my-nginx-5b56ccd65f-6s82f                    1/1     Running   0          7h48m
// test-heartbeats-0                            1/1     Running   0          13h
// test-heartbeats-deployment-d496c5d85-qj24b   1/1     Running   0          2d9h

    // curl -H "Host: helloworld-go.default.example.com" http://$INGRESS_HOST:$INGRESS_PORT

    // alexcui@node0:/mydata$ kubectl describe services example-service
    // Name:                     example-service
    // Namespace:                default
    // Labels:                   <none>
    // Annotations:              <none>
    // Selector:                 run=load-balancer-example
    // Type:                     NodePort
    // IP:                       10.102.11.149
    // Port:                     <unset>  8080/TCP
    // TargetPort:               8080/TCP
// NodePort:                 <unset>  32620/TCP
    // Endpoints:                10.244.1.44:8080,10.244.1.45:8080
    // Session Affinity:         None
    // External Traffic Policy:  Cluster
    // Events:                   <none>


    // alexcui@node0:/mydata$ kubectl cluster-info
// Kubernetes master is running at https://10.10.1.1:6443
// KubeDNS is running at https://10.10.1.1:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

    setTimeout(function() { 
        console.log("setting back");
        image.style.opacity = "1";
        spinner.style.display = "none";
        results.style.display = "block";
    }, 3000);
}

function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }
