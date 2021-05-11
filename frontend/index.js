const express = require('express')
const app = express();
const path = require('path');
const request = require('request-promise'); 

const port = 8000;

app.use(express.static("public"));
app.use(express.static(__dirname + '/node_modules/bootstrap/dist'));
// app.use(express.json()); //parses request body
app.use(express.json({limit: "50mb"}));
app.use(express.urlencoded({limit: "50mb", extended: true, parameterLimit:50000}));
// app.use(express.static(process.cwd() + '../../backend/cropped_photos/main')); //have images available, cant just call relative path

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname + '/public/main.html'));
  // res.sendFile(express.static('/public/main.html'));
});



app.post('/postdatatoFlask', async function (req, res) { 
  var data = { // this variable contains the data you want to send 
      data1: "foo", 
      data2: "bar" 
  } 

  var options = { 
      method: 'POST', 
      uri: 'http://127.0.0.1:5000/postdata', 
      body: data, 
      json: true // Automatically stringifies the body to JSON 
  }; 
   
  var returndata; 
  var sendrequest = await request(options) 
  .then(function (parsedBody) { 
      console.log(parsedBody); // parsedBody contains the data sent back from the Flask server 
      returndata = parsedBody; // do something with this data, here I'm assigning it to a variable. 
  }) 
  .catch(function (err) { 
      console.log(err); 
  }); 
   
  res.send(returndata); 
}); 

app.post('/detect', async function (req, res) { 
  console.log("here");
  console.log(req.body);
  console.log(JSON.stringify(req.body));


  var options = { 
      method: 'POST', 
      uri: 'http://127.0.0.1:5000/detect', 
      body: req.body,
      json: true // Automatically stringifies the body to JSON 
  }; 



   
  var returndata; 
  var sendrequest = await request(options) 
          .then(function (parsedBody) { 
              // console.log(parsedBody); // parsedBody contains the data sent back from the Flask server 
              returndata = parsedBody; // do something with this data, here I'm assigning it to a variable. 
          }) 
          .catch(function (err) { 
              console.log(err); 
          }); 
   
  res.send(returndata); 
}); 

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`)
});