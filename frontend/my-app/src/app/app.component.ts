import { Component } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'my-app';
  public loading : boolean = false;
  public faces = [];
  public backendURL = "http://127.0.0.1:5000";

  constructor(private http: HttpClient) {}
  
  public uploadImage() {
      document.getElementById("hidden-button").click();
  }

  public loadFile(event) {
    var output = <HTMLImageElement>document.getElementById("img");
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
  }

  public detect() {
    var image = document.getElementById("img");
    var inputImage = <HTMLInputElement>document.getElementById("hidden-button");
    image.style.opacity = ".3";

    this.getBase64(inputImage.files[0]).then(
        b64 => {
            // console.log(b64);
            this.loading = true;
            this.faces = [];
        
            //find all faces
            this.http.post(this.backendURL + "/detect", {img: b64}).subscribe(res => {
              console.log("done");

              let temp = []
              for (let r of <any>res['data']) {
                temp.push("data:image/png;base64," + r);
              }

              // console.log(temp);
              // console.log(temp[0].substring(temp[0].length - 20));
              // console.log(temp[1].substring(temp[1].length - 20));
              // console.log(temp[2].substring(temp[2].length - 20));


              //guess age of faces
              this.http.post(this.backendURL + "/guessAge", {imgs: temp}).subscribe(res2 => {
                console.log(res2);

                //guess gender of faces
                this.http.post(this.backendURL + "/guessGender", {imgs: temp}).subscribe(res3 => {
                  console.log(res3);
  
                  for (let i = 0; i < res['data'].length; i++) {
                    this.faces.push({
                      src: temp[i],
                      age: res2['data'][i].class,
                      ageConfidence: res2['data'][i].confidence,
                      gender: res3['data'][i].class,
                      genderConfidence: res3['data'][i].confidence,
                    });
                  }

                  image.style.opacity = "1";
                  this.loading = false;
                }, err => {
                  console.log(err);
                  this.loading = false;
                });
              }, err => {
                console.log(err);
                this.loading = false;
              });
            }, err => {
              console.log(err);
              this.loading = false;
            });
        } 
    );
  }

  public getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }

  public changePhone(body) {
    return this.http.post('http://127.0.0.1:5000/detect', {
      data: body
    });
  }
}
