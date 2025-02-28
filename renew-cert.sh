#!/bin/bash
docker run -it --rm --name certbot \
           -v "/etc/letsencrypt:/etc/letsencrypt" \
           -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
           -p 80:80 -p 443:443 certbot/certbot certonly

sudo cp /etc/letsencrypt/live/irnus-dl.slickerius.com/fullchain.pem nginx/
sudo cp /etc/letsencrypt/live/irnus-dl.slickerius.com/privkey.pem nginx/
