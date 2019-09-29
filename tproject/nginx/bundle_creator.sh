mv private.key valv_private.key
awk '{print}' certificate.crt ca_bundle.crt > valv_bundle.crt
