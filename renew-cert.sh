#!/bin/bash
sudo docker run --rm -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/dns-cloudflare certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini -d irnus-dl.slickerius.com -d irnus-dl.slickeri.us

kubectl create secret tls irnusdl-tls --cert=/etc/letsencrypt/live/irnus-dl.slickerius.com/fullchain.pem --key=/etc/letsencrypt/live/irnus-dl.slickerius.com/privkey.pem -n irnusdl --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/irnusdl -n irnusdl
