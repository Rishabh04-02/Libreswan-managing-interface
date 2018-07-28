# Certificate Revocation

## Links followed
1. [https://raymii.org/s/tutorials/OpenSSL_command_line_Root_and_Intermediate_CA_including_OCSP_CRL%20and_revocation.html](https://raymii.org/s/tutorials/OpenSSL_command_line_Root_and_Intermediate_CA_including_OCSP_CRL%20and_revocation.html)
2. [https://jamielinux.com/docs/openssl-certificate-authority/certificate-revocation-lists.html](https://jamielinux.com/docs/openssl-certificate-authority/certificate-revocation-lists.html)

## Command used to create certificates in the project in the respective order

1. Root CA
Generating root key and then certificate

		openssl genrsa -aes256 -out ca.key.pem -passout pass:KeyPassword 4096
		openssl req -key ca.key.pem -passin pass:Password -new -x509 -days 365 -sha256 -out ca.root.pem

2. Creating end user certificates (signed)
	1. Generate a key for user

			openssl req -newkey rsa:2048 -nodes -keyout keyname.pem -days 365

	2. Create a CSR

			openssl req -out keyname.csr -key keyname.pem -new -days 365

	3. Signing the key with root cert

			openssl ca -batch -create_serial -config openssl.cnf -cert ca.root.pem -keyfile ca.key.pem -passin pass:KeyFinalPassword -in keyname.csr -out certname.pem

	4. Generate .p12 file

			openssl pkcs12 -name username -inkey keyname.pem -in certname.pem -export -out username.p12 -password pass:password

Note - I've added `crlDistributionPoints = URI:http://localhost:8000/crl/distripoint.crl.pem` to the `openssl.cnf` along with below options:

	# For certificate revocation lists.
	# crlDistributionPoints = URI:http://HOSTNAME/crl/distripoint.crl.pem
	crlDistributionPoints = URI:http://localhost:8000/crl/distripoint.crl.pem
	crlnumber         = $dir/config/crl/crlnumber
	crl               = $dir/config/crl/ca.crl.pem
	crl_extensions    = crl_ext
	default_crl_days  = 60

where `localhost:8000` will be replaced by `servername`.


Can you please provide me with the commands also as I'm having difficulty dealing with the commands in the tutorials as in our project I've used different commands to achieve the same purpose.

Also I've figured out another way (Just in case nothing else works) that I can do the things (generate certs, etc) in the way as they are in the tutorial. Hence replacing the commands I've used in the project with the ones mentioned in the tutorials. But in that way I've to use the intermediate certificates. I don't think its a good way to go.