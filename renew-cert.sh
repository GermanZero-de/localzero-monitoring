#!/bin/bash

# fail on error
set -x

docker exec acme-sh --renew -d monitoring-test.localzero.net -d monitoring.localzero.net \
    --standalone --server https://acme-v02.api.letsencrypt.org/directory \
    --cert-file /acme.sh/ssl-cert.cer --key-file /acme.sh/ssl-cert.key
docker exec nginx-testing nginx -s reload