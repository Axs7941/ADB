const express = require("express");
const router = express.Router();
const routes = require("./routes/home");

var app = express();
app.use(express.static("./routes"));

app.get("/", function (req, res) {
  res.sendFile("index.html", { root: __dirname });
});

//app.get("/");

module.exports = router;
app.listen(8080);
