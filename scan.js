// NOTE: the list of responses recived do not include the header of the actual page.
// HSTS is probably also not enforced on the page load.

var webpage = require("webpage");
var system = require("system");
var fs = require("fs");

// Chrome
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36';
LOAD_TIME = 15000; //ms

var globalSTSList = {};

function writeGlobalSTSList() {
    var str = JSON.stringify(globalSTSList, null, "  ");
    fs.write("data/phantomjs.json", str);
}

// http://stackoverflow.com/questions/2300771/jquery-domain-get-url
function getHost(url)
{
    var a = document.createElement('a');
    a.href = url;
    return a.hostname;
}

function getHSTS(response)
{
    var a = document.createElement('a');
    a.href = response.url;
    var hsts = null;
    if (a.protocol == "https:") {
        for (var i in response.headers) {
          if (response.headers[i].name.toLowerCase() === "strict-transport-security") {
            hsts = response.headers[i].value;
            // Don't return, let the last time override. TODO: is that how browsers handle it?
          }
        }
    }
    return hsts;
}

function process(url) {
    var page = webpage.create();
    globalSTSList[url] = {};

    system.stderr.write("Starting with " + url + "\n");
    page.settings.userAgent = USER_AGENT;

    page.onResourceReceived = function (response) {
        var host = getHost(response.url);
        var hsts = getHSTS(response);
        if (hsts) {
            globalSTSList[url][host] = hsts;
        }
        system.stdout.write(".");
        system.stdout.flush();
    };

    function finalize() {
        console.log(url, JSON.stringify(globalSTSList[url], null, "  "));
        var str = JSON.stringify(globalSTSList, null, "  ");
        var fileName = ("data/phantomjs/" + url + ".json").replace("://", ".");
        fs.write(fileName, str);
        phantom.exit();
    }

    page.open(url, function (status) {
        //Page is loaded!
        // phantom.exit();
        setTimeout(finalize, LOAD_TIME);
    });
}

process(system.args[1]);

// process("http://passwordbox.com", phantom.exit);

// process("https://www.facebook.com");

// var array = fs.read("data/hsts_list_test.csv").split("\n");

// domain = "icloud.com";
// var array = [
//     // "http://" + domain,
//     // "http://www." + domain,
//     // "https://" + domain,
//     "https://www." + domain
// ];


// function next(i) {
//     var url = array[i];
//     process(url);

//     if (i+1 < array.length) {
//         setTimeout(function(){next(i+1);}, 1000);
//     }
// }

// next(0);

// function writeGlobalSTSListCron() {
//     writeGlobalSTSList();

//     setTimeout(writeGlobalSTSListCron, 10000);
// }

// writeGlobalSTSListCron();