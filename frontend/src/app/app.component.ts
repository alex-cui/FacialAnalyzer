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
  public backendURL1 = "http://127.0.0.1:5000";
  public backendURL2 = "http://127.0.0.1:5000";
  // public backendURL = "http://node0.alexcui-qv98630.cs179icloud-pg0.utah.cloudlab.us:5000";

  public ages = {};
  public genders = {};
  public guessAge = true;
  public guessGender = true;

  public faceTime = "";
  public ageTime = "";
  public genderTime = "";



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
            this.resetData();
            let time = performance.now();

            //find all faces
            this.http.post(this.backendURL1 + "/detect", {img: b64}).subscribe(res => {
              console.log("done");
              this.faceTime = this.getTimer(time);

              let tempFaces = [];
              for (let r of <any>res['data']) {
                tempFaces.push("data:image/png;base64," + r);
              }

              for (let i = 0; i < res['data'].length; i++) {
                this.faces.push({
                  src: tempFaces[i],
                });
              }

              let ageDone = false;
              let genderDone = false;

              //guess age of faces
              if (this.guessAge) {
                let t1 = performance.now();

                this.http.post(this.backendURL1 + "/guessAge", {imgs: tempFaces}).subscribe(res2 => {
                  console.log(res2);
                  this.ageTime = this.getTimer(t1);

                  for (let i = 0; i < res['data'].length; i++) {
                    let age = res2['data'][i].class;
  
                    this.faces[i]['age'] = age;
                    this.faces[i]['ageConfidence'] = res2['data'][i].confidence;
                    this.ages[age] = this.ages[age] ? (this.ages[age] + 1) : 1;
                  }

                  if (this.guessGender) {
                    if (genderDone) {
                      image.style.opacity = "1";
                      this.loading = false;
                    }
                  }
                  else {
                    image.style.opacity = "1";
                    this.loading = false;
                  }
                  ageDone = true;
                }, err => {
                  console.log(err);
                  image.style.opacity = "1";
                  this.loading = false;
                });
              }

              //guess gender of faces
              if (this.guessGender) {
                let t1 = performance.now();

                this.http.post(this.backendURL2 + "/guessGender", {imgs: tempFaces}).subscribe(res3 => {
                  console.log(res3);
                  this.genderTime = this.getTimer(t1);

                  for (let i = 0; i < res3['data'].length; i++) {
                    let gender = res3['data'][i].class;
  
                    this.faces[i]['gender'] = gender;
                    this.faces[i]['genderConfidence'] = res3['data'][i].confidence;
                    this.genders[gender] = this.genders[gender] ? (this.genders[gender] + 1) : 1;
                  }

                  if (this.guessAge) {
                    if (ageDone) {
                      image.style.opacity = "1";
                      this.loading = false;
                    }
                  }
                  else {
                    image.style.opacity = "1";
                    this.loading = false;
                  }
                  genderDone = true;
                }, err => {
                  console.log(err);
                  image.style.opacity = "1";
                  this.loading = false;
                });
              }

              //just done
              if (!this.guessAge && !this.guessGender) {
                image.style.opacity = "1";
                this.loading = false;
              }
            }, err => {
              console.log(err);
              image.style.opacity = "1";
              this.loading = false;
            });
        } 
    );
  }

  public resetData() {
    this.faces = [];
    this.ages = {};
    this.genders = {};
    this.faceTime = "";
    this.ageTime = "";
    this.genderTime = "";
  }

  public getTimer(t) {
    return ((performance.now() - t) / 1000).toFixed(2);
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
