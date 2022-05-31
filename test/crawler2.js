const login = require("./login");

login();

var request = require("request");
var OAuth2 = require("oauth2").OAuth2;

var oauth2 = new OAuth2("403917684893024",  // 페이스북 APP ID
                        "5c3a1c7ce8bfca6899901565e8a87cd3", // 페이스북 APP SECRET
                        "", "https://www.facebook.com/dialog/oauth",
                        "https://graph.facebook.com/oauth/access_token",
                        null);

app.get("/facebook/auth", function (req, res) {
    var redirect_uri = "http://localhost:4000"
    var params = {"redirect_uri": redirect_uri,
    "scope":"user_about_me,publish_actions"};
        res.redirect(oauth2.getAuthorizeUrl(params));
});

app.get("/Path_To_Be_Redirected_to_After_Verification", function (req, res) {
    if(req.error_reason) {
        res.send(req.error_reason);
    }
    if (req.query.code) {
        var loginCode = req.query.code;
        var redirect_uri = "http://localhost:4000";
        oauth2.getOAuthAccessToken(loginCode, 
            { 
                grant_type: "authorization code",
                redirect_uri: redirect_uri
            },
                function(err, accessToken, refreshToken, params) {
                    if(err) {
                        console.error(err);
                        res.send(err);
                    }
                    var access_token = accessToken;
                    var expires = params.expires;
                    req.session.access_token = access_token;
                    req.session.expires = expires;
                });
    }
});

app.get("/get_fb_profile", function(req, res){
    oauth2.get("https://graph.facebook.com/me",
    req.session.accessToken, function(err, data, response) {
        if(err) {
            console.error(err);
            res.send(err);
        } else {
            var profile = JSON.parse(data);
            console.log(profile);
            var profile_img_url = "https://graph.facebook.com/"+profile.id+"/picture";
        }
    });
});

app.post("/post_to_fb", function(req, res) {
    var url = "https://graph.facebook.com/me/feed";
    var params = {
        access_token: req.session.access_token,
        message: req.body.text,
        link: req.body.url
    };
    request.post({url: url, qs: params}, function(err, resp, body) {
        if(err) {
            console.error(err)
            return;
        }
        body = JSON.parse(body);
        if(body.error) {
            var error = body.error.message;
            console.error("Error returned from facebook : " + body.error.message);
            if(body.error.code == 341) {
                error = "You have reached the post limit for facebook. Please wait for 24 hours before posting again to facebook."
                console.error(error);
            }
            res.send(error);
        }
        var return_ids = body.id.split("_");
        var user_id = return_ids[0];
        var post_id = return_ids[1];
        var post_url = "https://www.facebook.com"+user_id+"/posts/"+post_id;
        res.send(post_url);
    });
});
