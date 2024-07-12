# IrnusDL

by sl0ck

---

## About

IrnusDL is a web utility for parsing and downloading Irama Nusantara releases given a release's URL with the injection of the appropriate metadata. This project was envisioned to support the needs of Last.fm scrobblers and those who collect digital music files.

![demo](static/img/demo.gif)

## Installation

Make sure that you have the appropriate Docker Engine installed. When running this on an HTTPS server, paste your `privkey.pem` and `fullchain.pem` files to the `nginx/` directory. If not running on an HTTPS server, change the WebSocket protocol used in `static/js/script.js` to `ws://`. 

Running this application requires only the following command:

```sh
$ ./start.sh
```

And do the following to restart the app.

```sh
$ ./restart.sh
```
