console.log('Loading a web page');
var page = require('webpage').create();
var url = 'https://garron.net';

page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36';


page.onResourceRequested = function (request) {
    // console.log('Request ' + JSON.stringify(request, undefined, 4));
};

page.onResourceReceived = function (response) {

    for (i in response.headers) {
      if (response.headers[i].name.toLowerCase() === "strict-transport-security") {
        console.log(response.url);
        console.log(response.headers[i].value);
      }
    }

    // console.log('Receive ' + JSON.stringify(response.url, undefined, 4));
    // console.log('Receive ' + JSON.stringify(response.redirectURL, undefined, 4));
};

page.open(url, function (status) {
    console.log("Loaded");
    page.render('garron.net.png');
    //Page is loaded!
    // phantom.exit();
});