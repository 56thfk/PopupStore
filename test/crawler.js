const login = require("./login");

login();

var access_token = "";
var socketio = require("socket.io");
var express = require("express");
var http = require("http");
var fb = require("fb");
var url = require("url");
var fs = require("fs");
var es = require("elasticsearch");
var jsonfile = require("jsonfile");
var morgan = require("morgan");
var bodyParser = require('body-parser');
var morgan = require("morgan");

var client = null;
var app = express();


app.use(bodyParser.urlencoded( {
    extended: true
}));
app.use(bodyParser.json());
//app.use(app.router);
//app.use(express.bodyParser()); // 3.x 버전
//app.use(express.logger); // 3.x 버전
app.use(morgan('dev')); // 4.x 버전
app.use(express.static(__dirname + '/public'));
var run = http.createServer(app);

run.listen(30000, function(error){
    client = new es.Client({
        host:'127.0.0.1:9200',
        log:'trace'
    });
    console.log("Express server listening on port 30000");
});

app.get('/', function(request, response) {
    fs.readFile("./getAccessToken.html", function(error, data) {
        response.sendFile("getAccessToken.html");
    });
});

function getAccessToken() {
    fb.api("oauth/access_token", {
        client_api: 403917684893024,
        client_secret: "5c3a1c7ce8bfca6899901565e8a87cd3",
        redirect_uri: "http://localhost:4000/PopUpStore",
        grant_type: "client_credentials"
    }, function(res) {
        if(!res || res.error) {
            console.log(!res ? "error occurred" : res.error);
            return;
        }else {
            access_token = res.access_token;
            fb.setAccessToken(access_token);
            feedLink = "260674821297104/posts"; // 가져올 포스트
            getWallFeeds(feedLink, {});
        }

    });
}
function getWallFeeds(feedLink, args) {
    fb.api(feedLink, "get", args, function(res) {
        if(!res || res.error) {
            console.log(!res ? "error occurred" : res.error);
            return;
        }
        processMessage(res.data);
        var nextLinkParts = url.parse(res.paging.next, true);
        var args = {
            limit: nextLinkParts.query.limit,
            until: nextLinkParts.query.until,
            access_token: nextLinkParts.query.access_token
        };

        getWallFeeds(feedLink, args);
    });
}

function processMessage(data) {
    for (i in data) {
        var json = {
            message: data[i].message,
            story: data[i].story
        };
        client.index({
            index: "huffpost",
            type: "huffpost",
            id: data[i].id,
            body: {
                message: data[i].message,
                created_time: data[i].created_time    
            }
        }, function(err, res) {
            if(err) {
                console.log(err);
            }else{
                console.log("success");
            };
        });
    }
}

getAccessToken();