const express = require("express");
const router = express.Router();
//const routes = require("./routes/home");
const http = require("http");

var app = express();
var LineByLineReader = require("line-by-line");
var stopword = require("stopword");
const removePunctuation = require("remove-punctuation");
app.use(express.static("./routes"));

const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: false }));

// parse application/json
app.use(bodyParser.json());

var words_file_line = {};
var file_line = {};

var files = ["sample.txt", "sample1.txt","Alice.txt", "CandideEn.txt","CandideFr.txt", "Shakespeare.txt"];

function getMapValue(map, key) {
  return map[key] || [];
}

function indexFile(num) {
  var file_index = num.toString();
  var line_no = 1;
  lr = new LineByLineReader(files[num]);

  lr.on("line", function (line) {
    const words = stopword.removeStopwords(
      removePunctuation(line).split(/\s+/)
    );
    for (var i = 0; i < words.length; i++) {
      const word = words[i].toLowerCase();
      words_file_line[word] = getMapValue(words_file_line, word).concat(
        file_index + "_" + line_no
      );
    }
    file_line[file_index + "_" + line_no] = line;
    line_no++;
  });

  lr.on("end", function () {
    //console.log('Completed Indexing file ' + num.toString());
  });
}

async function indexFiles() {
  for (var num = 0; num < files.length; num++) {
    var ind = await indexFile(num);
  }
}

router.get("/", function (req, res) {
  res.sendFile("index.html", { root: __dirname });
});

router.get("/preprocess", (req, res) => {
  indexFiles();
  res.json({message: 'Done preprocessing'});
});

router.post("/search", (req, res) => {
  var inp = req.body.search_word;
  var inp = inp.toLowerCase();
  var out = [];
  var array = inp.split(/\s+/);

  var response = [];

  for (var i = 0; i < array.length; i++) {
    if(words_file_line[array[i]]){
      for(var j = 0; j < words_file_line[array[i]].length; j++){
        var [index, line] = words_file_line[array[i]][j].split('_');
        const line_number = parseInt(line);
        response.push({name: files[parseInt(index)], line_number: line_number, line: file_line[words_file_line[array[i]][j]]});
      }
    }
  }

  res.json({data: response});
});



module.exports = router;

app.use("/", router);
app.listen(8080);
