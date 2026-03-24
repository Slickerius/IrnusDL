# IrnusDL

by sl0ck

---

## About

IrnusDL is a web utility for parsing and downloading Irama Nusantara releases given a release's URL with the injection of the appropriate metadata. This project was envisioned to support the needs of Last.fm scrobblers and those who collect digital music files.

![demo](static/img/demo.gif)

## Deployment

IrnusDL is deployed on a k3s cluster via [sl0ck-k8s](https://github.com/Slickerius/sl0ck-k8s). See that repo for all Kubernetes manifests.

### Build and push image

```sh
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/slickerius/irnusdl:latest --push .
```

### TLS renewal

```sh
sudo docker run --rm -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/dns-cloudflare certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini -d irnus-dl.slickerius.com -d irnus-dl.slickeri.us
```

```sh
kubectl create secret tls irnusdl-tls --cert=/etc/letsencrypt/live/irnus-dl.slickerius.com/fullchain.pem --key=/etc/letsencrypt/live/irnus-dl.slickerius.com/privkey.pem -n irnusdl --dry-run=client -o yaml | kubectl apply -f -
```

```sh
kubectl rollout restart deployment/irnusdl -n irnusdl
```
