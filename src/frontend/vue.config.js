const { defineConfig } = require('@vue/cli-service')
const fs = require('fs')
module.exports = {
    devServer: {
        allowedHosts: "all",
        https: {
                key: fs.readFileSync('../main/resources/ssl/key.pem'),
                cert: fs.readFileSync('../main/resources/ssl/cert.pem'),
                passphrase: 'password'
              },
        port: 443,
        proxy: {
            '/describe': {
                target: 'https://localhost:8080',
                ws: true,
                changeOrigin: true,

             }
         }
    }
}