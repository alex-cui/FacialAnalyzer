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
  public images = [];

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
            this.loading = true;
            this.images = [];
        
            this.http.post('http://127.0.0.1:5000/detect', {img: b64}).subscribe(res => {
              console.log("done");
              console.log(res);

              for (let b64 of <any>res['data']) {
                  this.images.push("data:image/png;base64," + b64);
              }

              image.style.opacity = "1";
              this.loading = false;
            }, err => {
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
