const express = require('express');
const proxy = express();
const http = require('http');

proxy.get("*", function(req, res, next) {
    res.redirect("https://" + req.headers.host + req.path);
});

http.createServer(proxy).listen(80, function() {});
