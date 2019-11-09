var rest = require('./rest.js');
var post = require('./post.js');

var sampleRate = 500;
var loopState = true;

var Readoptions = {
    host: 'localhost',
    port: 39320,
    path: '/iotgateway/read?ids=Channel1.SimuDev.Tag1&ids=Channel1.SimuDev.Tag2&ids=Channel1.SimuDev.exitLoop',
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
};

console.log("Starting Services..")

var serviceLoop = setInterval(function() {
    rest.getJSON(Readoptions,
        function(statusCode, result) {

            //console.log("Result: (" + statusCode + ")" + JSON.stringify(result));
            var tag1 = result.readResults[0].v;
            var tag2 = result.readResults[1].v;
            var exitLoop = result.readResults[2].v;

            console.log("Tag1 is: " + tag1 + ". Tag 2 is " + tag2);
            sumResults = tag1 + tag2;
            console.log("Some post proc results (Tag1 + Tag2) = " + sumResults);

            var requestData = [{ "id": "Channel1.PostProc.Sum of Tags", "v": sumResults }];
            post.writerequest(requestData);

            if (exitLoop == 1) {
                clearInterval(serviceLoop);
                console.log("Exited")
            }
        });


}, sampleRate);