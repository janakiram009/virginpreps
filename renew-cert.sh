#!/bin/bash
docker run -it --rm \
  -v /home/ubuntu/certbot/conf:/etc/letsencrypt \
  -v /home/ubuntu/certbot/www:/var/www/certbot \
  certbot/certbot renew
docker-compose restart nginx
