function preprocess() {
  fetch("/preprocess", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {})
    .catch((error) => {
      console.error("Error:", error);
    });
  return false;
}

function showWordCount() {
  fetch("/showWordCount", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      add_word_count_table(data.data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return false;
}

function showFirstThreeLines() {
  fetch("/showFirstThreeLines", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      add_first_three_lines_table(data.data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return false;
}


function search(search_word) {
  var search_word = document.getElementById(search_word).value;
  fetch("/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ search_word: search_word }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      add_data_to_table(data.data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return false;
}

function show_twenty_lines(file_name, search_word) {
  var file_name = document.getElementById(file_name).value;
  var search_word = document.getElementById(search_word).value;
  fetch("/showLines", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ file_name: file_name, search_word: search_word }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      add_twenty_lines(data.data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return false;
}

function add_data_to_table(data) {
  var headers = ["name", "line_number", "line"];
  var headings = ["File Name", "Line Number", "Sentence"];

  document.getElementById("output_div").innerHTML = "";

  var outputHTML = "";
  outputHTML += "<table>";
  outputHTML += "<tr>";
  for (var i = 0; i < headers.length; i++) {
    outputHTML += "<th>" + headings[i] + "</th>";
  }
  outputHTML += "</tr>";
  for (var i = 0; i < data.length; i++) {
    outputHTML += "<tr>";
    for (var j = 0; j < headers.length; j++) {
      outputHTML += "<td>" + data[i][headers[j]] + "</td>";
    }
    outputHTML += "</tr>";
  }
  outputHTML += "</table>";
  // output our html
  document.getElementById("output_div").innerHTML = outputHTML;
}

function add_word_count_table(data) {
  var headers = ["name", "word_count"];
  var headings = ["File Name", "Word Count"];

  document.getElementById("wordCount").innerHTML = "";

  var outputHTML = "";
  outputHTML += "<table>";
  outputHTML += "<tr>";
  for (var i = 0; i < headers.length; i++) {
    outputHTML += "<th>" + headings[i] + "</th>";
  }
  outputHTML += "</tr>";
  for (var i in data) {
    outputHTML += "<tr>";
    outputHTML += "<td>" + i + "</td>";
    outputHTML += "<td>" + data[i] + "</td>";
    outputHTML += "</tr>";
  }
  outputHTML += "</table>";
  // output our html
  document.getElementById("wordCount").innerHTML = outputHTML;
}

function add_first_three_lines_table(data) {
  var headers = ["name", "three_lines"];
  var headings = ["File Name", "1st Line", "2nd Line", "3rd Line"];

  document.getElementById("wordCount").innerHTML = "";

  var outputHTML = "";
  outputHTML += "<table>";
  outputHTML += "<tr>";
  for (var i = 0; i < headings.length; i++) {
    outputHTML += "<th>" + headings[i] + "</th>";
  }
  outputHTML += "</tr>";
  for (var i in data) {
    outputHTML += "<tr>";
    outputHTML += "<td>" + i + "</td>";
    outputHTML += "<td>" + data[i][0] + "</td>";
    outputHTML += "<td>" + data[i][1] + "</td>";
    outputHTML += "<td>" + data[i][2] + "</td>";
    outputHTML += "</tr>";
  }
  outputHTML += "</table>";
  // output our html
  document.getElementById("wordCount").innerHTML = outputHTML;
}


function add_twenty_lines(data) {
  var headers = ["name", "three_lines"];
  var headings = ["Count", "Lines"];

  document.getElementById("wordCount").innerHTML = "";

  var outputHTML = "";
  outputHTML += "<table>";
  outputHTML += "<tr>";
  for (var i = 0; i < headings.length; i++) {
    outputHTML += "<th>" + headings[i] + "</th>";
  }
  outputHTML += "</tr>";

  outputHTML += "<tr>";
  outputHTML += "<td>" + data.count + "</td>";
  outputHTML += "<td>" + data.lines.join('\n') + "</td>";
  outputHTML += "</tr>";
  
  outputHTML += "</table>";
  // output our html
  document.getElementById("wordCount").innerHTML = outputHTML;
}


