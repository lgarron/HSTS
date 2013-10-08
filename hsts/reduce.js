var fs = require("fs");

var all = [];
var hsts = [];

var csvout = [];

for (var i = 0; i < 10; i++) {
  var data = JSON.parse(fs.readFileSync(
    "data/10000/items-"+i+"0001.json"
  ));
  function par(str) {return "\"" + str + "\""};
  for (var j in data) {
    all.push(data[j]);
    csvout.push("" +
      data[j].index + "," +
      par(data[j].url) + "," +
      data[j].status + "," +
      par(data[j].hsts)
    );
    if (data[j].hsts) {
      hsts.push(data[j].url);
    }
  }
}

fs.writeFileSync(
  "data/all.csv",
  csvout.join("\n")
);

fs.writeFileSync(
  "data/hsts-list-alexa-raw.csv",
  hsts.join("\n")
);