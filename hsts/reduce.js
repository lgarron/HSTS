var fs = require("fs");

var all = [];
var hsts = [];

var csvout = [];

var sites = {};

for (var i = 0; i < 10; i++) {
  var data = JSON.parse(fs.readFileSync("data/10000/items-"+i+"0001.json"));
  for (var j in data) {
    if (!(data[j].index in sites)) {
      sites[data[j].index] = [];
    }
    data[j].index = parseInt(data[j].index);
    sites[data[j].index].push(data[j]);
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

var regex = /^max-age="?(\d+)"?(\s*;\s*(includeSubDomains)?)?\s*$/i;
function parseHSTS(page) {
  if (page.protocol !== "https") { return null; }
  if (page.hsts === null) { return null; }
  var res = regex.exec(page.hsts);
  // console.log(res);
  if (res === null) { return null; }
  return {
    maxAge: parseInt(res[1], 10),
    iSD: (res[3] !== undefined)
  };
}

// function sendsHSTS(page) {
//   return parseHSTS(page) !== null;
// }

console.log("--------\nBeginning HSTS parsing sanity console.log statements.")
console.log(parseHSTS({protocol: "https", hsts: "max-age=0; includesubDOMAINS"}));
console.log(parseHSTS({protocol: "https", hsts: "max-age=0"}));
console.log(parseHSTS({protocol: "https", hsts: "max-age=\"5\";"}));
console.log(parseHSTS({protocol: "https", hsts: "max-age=0;"}));
console.log(parseHSTS({protocol: "https", hsts: "max-age=;"}));
console.log(parseHSTS({protocol: "https", hsts: "maxage=55"}));
console.log(parseHSTS({protocol: "https", hsts: "max-age=55, includesubdomains"}));
console.log("--------")

var hstsIndices = [];
var maxAges = [];
var maxAgeZeros = [];
var iSD = [];
var sendsHSTSOverPlainHTTP = [];
var badHSTSHeader = [];
var alexaHSTSList = [];

for (var i in sites) {
  for (var j in sites[i]) {
    var page = sites[i][j];
    var hsts = parseHSTS(page);
    if (page.protocol === "https" && hsts !== null) {
      // TODO: maybe use canonical version instead of the first here?
      if(hsts.maxAge > 0) {
        hstsIndices.push(page.index);
        maxAges.push(hsts.maxAge);
        alexaHSTSList.push(page.url);
        // Take the first one we get to.
        break;
      }
      if(hsts.maxAge === 0) {
        maxAgeZeros.push(page.index);
      }
      if(hsts.iSD === 0) {
        iSD.push(page.index);
      }
    }
    else if (page.protocol === "http" && page.hsts) {
      sendsHSTSOverPlainHTTP.push(page.index);
    }
    else if (page.hsts !== null && hsts === null) {
      badHSTSHeader.push(page.index);
    }
  }
}

function sortNumbers(list) {
  return list.sort(function(a, b){return a - b;});
}

console.log("# Indices of HSTS hosts (send a valid HSTS header over either HTTPS root URL with max-age > 0.");
console.log(JSON.stringify(sortNumbers(hstsIndices)));
console.log("# max-age values of HSTS hosts, in seconds.");
console.log(JSON.stringify(sortNumbers(maxAges)));
console.log("# Valid HSTS headers sent over HTTPS with max-age == 0.");
console.log(JSON.stringify(sortNumbers(maxAgeZeros)));
console.log("# Sends HSTS over plain text.");
console.log(JSON.stringify(sortNumbers(sendsHSTSOverPlainHTTP)));
console.log("# Sends a bad HSTS header over some protocol.");
console.log(JSON.stringify(sortNumbers(badHSTSHeader)));


// Create HSTS host list.
var chromiumHSTSStr = fs.readFileSync("src/transport_security_state_static-2013-10-08.json", "utf8");
//  https://mxr.mozilla.org/mozilla-central/source/security/manager/tools/getHSTSPreloadList.js#81
var chromiumHSTSJSON = JSON.parse(chromiumHSTSStr.replace(/\/\/[^\n]*\n/g, ""));
var chromiumHSTSList = [];
for (i in chromiumHSTSJSON.entries) {
  var entry = chromiumHSTSJSON.entries[i];
  if (entry.mode && entry.mode === "force-https") {
    chromiumHSTSList.push(entry.name);
  }
}

// From http://www.shamasis.net/2009/09/fast-algorithm-to-find-unique-items-in-javascript-array/
Array.prototype.unique = function() {
  var o = {}, i, l = this.length, r = [];
  for(i=0; i<l;i+=1) o[this[i]] = this[i];
  for(i in o) r.push(o[i]);
  return r;
};


var hstsList = alexaHSTSList.concat(chromiumHSTSList);
// Strip www. prefix; we'll use the parent domain in the Python script.
hstsList = hstsList.map(function(str) {return str.replace(/^www./, "");});
hstsList = hstsList.unique().sort();

console.log(hstsList);

fs.writeFileSync("../data/hsts_list.csv", hstsList.join("\n"));
