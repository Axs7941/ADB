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


