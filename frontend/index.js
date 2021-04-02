const express = require('express')
const app = express();
const path = require('path');

const port = 8000;

app.use(express.static("public"));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/public/main.html'));
    // res.sendFile(express.static('/public/main.html'));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`)
});