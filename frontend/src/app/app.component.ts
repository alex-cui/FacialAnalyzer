import { Component } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  public loading : boolean = false;
  public faces = [];
  public backendURL = "http://127.0.0.1:5000";
  // public backendURL = "http://node0.alexcui-qv98630.cs179icloud-pg0.utah.cloudlab.us:30604";

  public ages = {};
  public genders = {};
  public celebs = {};

  public guessAge = true;
  public guessGender = true;
  public guessCeleb = true;

  public faceTime = 0.00;
  public guessTime = 0.00;
  public ageTime = "";
  public genderTime = "";
  public celebTime = "";


  constructor(private http: HttpClient) {}
  
  public uploadImage() {
    document.getElementById("hidden-button").click();
  }

  public loadFile(event) {
    var output = <HTMLImageElement>document.getElementById("img");
    if (event.target.files[0]) {
      output.src = URL.createObjectURL(event.target.files[0]);
      output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
      }
    }
  }

  public detect() {
    var inputImage = <HTMLInputElement>document.getElementById("hidden-button");
    if (!inputImage.files[0]) {
      return;
    }
    var image = document.getElementById("img");
    image.style.opacity = ".3";

    this.getBase64(inputImage.files[0]).then(
      b64 => {
          this.loading = true;
          this.resetData();
          let time = performance.now();

          //find all faces
          this.http.post(this.backendURL + "/detect", {img: b64}).subscribe(res => {

            let tempFaces = [];
            for (let r of <any>res['data']) {
              tempFaces.push("data:image/png;base64," + r);
            }

            for (let i = 0; i < res['data'].length; i++) {
              this.faces.push({
                src: tempFaces[i],
              });
            }

            this.faceTime = parseFloat(this.getTimer(time));
            let flag = 0;
            let greatestTime = 0.00;

            //guess age of faces
            if (this.guessAge) {
              flag++;
              let t1 = performance.now();

              this.http.post(this.backendURL + "/guessAge", {imgs: tempFaces}).subscribe(res2 => {          
                //add data to faces
                for (let i = 0; i < res['data'].length; i++) {
                  let age = res2['data'][i].class;
          
                  this.faces[i]['age'] = age;
                  this.faces[i]['ageConfidence'] = res2['data'][i].confidence;
                  this.ages[age] = this.ages[age] ? (this.ages[age] + 1) : 1;
                }

                this.ageTime = this.getTimer(t1);
                if (parseFloat(this.ageTime) > greatestTime) {
                  greatestTime = parseFloat(this.ageTime);
                }
                this.checkFinishedGuessing(--flag, greatestTime, image)
              }, err => {
                console.log(err);
              });
            }

            //guess gender of faces
            if (this.guessGender) {
              flag++;
              let t1 = performance.now();

              this.http.post(this.backendURL + "/guessGender", {imgs: tempFaces}).subscribe(res2 => {
                //add data to faces
                for (let i = 0; i < res2['data'].length; i++) {
                  let gender = res2['data'][i].class;

                  this.faces[i]['gender'] = gender;
                  this.faces[i]['genderConfidence'] = res2['data'][i].confidence;
                  this.genders[gender] = this.genders[gender] ? (this.genders[gender] + 1) : 1;
                }

                this.genderTime = this.getTimer(t1);
                if (parseFloat(this.genderTime) > greatestTime) {
                  greatestTime = parseFloat(this.genderTime);
                }
                this.checkFinishedGuessing(--flag, greatestTime, image)
              }, err => {
                console.log(err);
              });
            }

            //guess closest looking celebrity
            if (this.guessCeleb) {
              flag++;
              let t1 = performance.now();

              this.http.post(this.backendURL + "/guessCelebrity", {imgs: tempFaces}).subscribe(res2 => {
                //add data to faces
                for (let i = 0; i < res2['data'].length; i++) {
                  let celeb = res2['data'][i].class;

                  this.faces[i]['celeb'] = celeb;
                  this.faces[i]['celebConfidence'] = res2['data'][i].confidence;
                  this.celebs[celeb] = this.celebs[celeb] ? (this.celebs[celeb] + 1) : 1;
                }

                this.celebTime = this.getTimer(t1);
                if (parseFloat(this.celebTime) > greatestTime) {
                  greatestTime = parseFloat(this.celebTime);
                }
                this.checkFinishedGuessing(--flag, greatestTime, image)
              }, err => {
                console.log(err);
              });
            }

            //just done
            if (!this.guessAge && !this.guessGender && !this.guessCeleb) {
              image.style.opacity = "1";
              this.loading = false;
            }
          }, err => {
            console.log(err);
            image.style.opacity = "1";
            this.loading = false;
          });
      }, err => {
        console.log(err)
      }
    );
  }

  public resetData() {
    this.faces = [];
    this.ages = {};
    this.genders = {};
    this.celebs = {};
    this.faceTime = 0.00;
    this.guessTime = 0.00;
    this.ageTime = "";
    this.genderTime = "";
  }

  public checkFinishedGuessing(flag, greatestTime, image) {
    if (flag == 0) {
      this.guessTime = greatestTime;
      image.style.opacity = "1";
      this.loading = false;
    }
  }

  public getTimer(t) {
    return ((performance.now() - t) / 1000).toFixed(2);
  }

  public getTimeInfo() {
    let s = "";

    if (this.guessAge && this.ageTime)
      s += "Guessed ages in: " + this.ageTime + " second(s)\n";
    if (this.guessGender && this.genderTime)
      s += "Guessed genders in: " + this.genderTime + " second(s)\n";
    if (this.guessCeleb && this.celebTime)
      s += "Guessed celebrities in: " + this.celebTime + " second(s)";

    return s;
  }

  public getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }
}
