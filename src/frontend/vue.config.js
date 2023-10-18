const { defineConfig } = require('@vue/cli-service')
const fs = require('fs')
module.exports = {
    devServer: {
        https: {
                key: fs.readFileSync('../main/resources/ssl/key.pem'),
                cert: fs.readFileSync('../main/resources/ssl/cert.pem'),
                passphrase: 'password'
              },
        port: 3000,
        proxy: {
            '/describe': {
                target: 'https://localhost:8080/',
                ws: true,
                changeOrigin: true,

             }
         }
    }
}