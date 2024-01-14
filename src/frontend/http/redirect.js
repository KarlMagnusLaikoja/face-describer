const express = require('express');
const httpRedirect = express();
const http = require('http');

httpRedirect.get("*", function(req, res, next) {
    res.redirect("https://" + req.headers.host + req.path);
});

http.createServer(httpRedirect).listen(80, function() {});
