#!/usr/bin/env bash
mv ./ssl/private.key ./ssl/valv_private.key
awk '{print}' ./ssl/certificate.crt ./ssl/ca_bundle.crt > ./ssl/valv_bundle.crt
