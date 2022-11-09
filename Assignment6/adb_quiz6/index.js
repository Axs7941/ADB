const express = require("express");
const router = express.Router();
//const routes = require("./routes/home");
const http = require("http");
var fs = require('fs');
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
var stopwords = [];

var files = ["A1.txt","A2.txt","A3.txt", "C1.txt","C2.txt", "S1.txt", "S2.txt", "S3.txt", "S4.txt", "S5.txt"];
var file_words = {};
var first_three_lines = {};

function getMapValue(map, key) {
  return map[key] || [];
}

async function loadStopWords() {
  lr = new LineByLineReader('shortliststopwords.txt');
  lr.on("line", function (line) {
    stopwords.push(line.replace(/"/g, '').trim());
  });

  lr.on("end", function () {
    console.log('Completed Loading stop words');
    console.log(stopwords);
  });
}

function indexFile(num, word_count) {
  var file_index = num.toString();
  var line_no = 1;
  var array_sw = [];

  lr = new LineByLineReader(files[num]);
  
  lr.on("line", function (line) {
    word_count = word_count + line.split(/\s+/).length;
    const words = stopword.removeStopwords(
      removePunctuation(line).split(/\s+/), stopwords
    );

    for (var i = 0; i < words.length; i++) {
      const word = words[i].toLowerCase();
      words_file_line[word] = getMapValue(words_file_line, word).concat(
        file_index + "_" + line_no
      );
    }
    file_line[file_index + "_" + line_no] = words.join(' ');

    if(line_no <= 3){
      first_three_lines[files[num]] = getMapValue(first_three_lines, files[num]).concat(words.join(' '));
    }

    line_no++;

  });

  lr.on("end", function () {
    //console.log('Completed Indexing file ' + num.toString());
    file_words[files[num]] = word_count;
  });
}

async function indexFiles() {
  await loadStopWords();
  for (var num = 0; num < files.length; num++) {
    var word_count = await indexFile(num, 0);
  }
}

router.get("/", function (req, res) {
  res.sendFile("index.html", { root: __dirname });
});

router.get("/preprocess", (req, res) => {
  indexFiles();
  res.json({message: 'Done preprocessing'});
});

router.get("/showWordCount", (req, res) => {
  res.json({data: file_words});
});

router.get("/showFirstThreeLines", (req, res) => {
  res.json({data: first_three_lines});
});

router.post("/showLines", (req, res) => {
  var file_name = req.body.file_name;
  var word = req.body.search_word.toLowerCase();

  var file_index;
  var lines = [];

  for(var i = 0; i < files.length; i++){
    if(files[i] === file_name)
      file_index = i;
  }

  for(var i = 0; i < words_file_line[word].length; i++){
    var [index, line] = words_file_line[word][i].split('_');
    var count = 0;
    index = parseInt(index);
    if(index == file_index){
      count++;
      if(count <= 20){
        lines.push(file_line[words_file_line[word][i]]);
      }
    }
  }

  res.json({data: {count: count, lines: lines}});
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
