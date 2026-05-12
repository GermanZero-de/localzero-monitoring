#!/usr/bin/env sh
# Generated using hints here: https://letsencrypt.org/docs/certificates-for-localhost/#making-and-trusting-your-own-certificates
openssl req -x509 -out fullchain.cer -keyout ssl-cert.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost,DNS:analytics.localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
