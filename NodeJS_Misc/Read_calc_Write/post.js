var request = require('request');

exports.writerequest = function(requestData) {
    request({
        url: 'http://localhost:39320/iotgateway/write',
        method: "POST",
        json: true,
        headers: {
            "content-type": "application/json",
        },
        json: requestData
    }, function(error, response, body) {
        console.log('write sucessful');
    })
}