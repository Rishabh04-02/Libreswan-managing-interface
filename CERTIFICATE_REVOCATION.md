# Certificate Revocation

## Links followed
1. [https://raymii.org/s/tutorials/OpenSSL_command_line_Root_and_Intermediate_CA_including_OCSP_CRL%20and_revocation.html](https://raymii.org/s/tutorials/OpenSSL_command_line_Root_and_Intermediate_CA_including_OCSP_CRL%20and_revocation.html)
2. [https://jamielinux.com/docs/openssl-certificate-authority/certificate-revocation-lists.html](https://jamielinux.com/docs/openssl-certificate-authority/certificate-revocation-lists.html)


## Command used to create certificates in the project in the respective order

1. Root CA
Generating root key and then certificate

		openssl genrsa -aes256 -out ca.key.pem -passout pass:KeyPassword 4096  
		openssl req -key ca.key.pem -passin pass:KeyPassword -new -x509 -days 365 -sha256 -out ca.root.pem -config openssl.cnf 
//now tha ca.root.pem is self signed and has the crl
//it is working when i put `crlDistributionPoints = URI:http://0.0.0.0:8000/distripoint.crl` in `[ v3_ca ]`


2. Create the CRL

		openssl ca -config openssl.cnf -gencrl -out distripoint.crl -passin pass:KeyPassword

Now check contents of crl
	
	openssl crl -in distripoint.crl -noout -text

3. Check if certificate has a crl

		openssl x509 -noout -text -in certname.pem | grep -A 4 'X509v3 CRL Distribution Points'


4. Creating end user certificates (signed)
	1. Generate a key for user

			openssl req -newkey rsa:2048 -nodes -keyout keyname.pem -days 365 

	2. Create a CSR

			openssl req -out keyname.csr -key keyname.pem -new -days 365  

	3. Signing the key with root cert

			openssl ca -batch -create_serial -config openssl.cnf -cert ca.root.pem -keyfile ca.key.pem -passin pass:KeyPassword -in keyname.csr -out certname.pem -extensions usr_cert  

	4. Generate .p12 file

			openssl pkcs12 -name username -inkey keyname.pem -in certname.pem -export -out username.p12 -password pass:password 

Note - I've added `crlDistributionPoints = URI:http://localhost:8000/crl/distripoint.crl.pem` to the `openssl.cnf` along with below options:


5. Revoke a certificate

		openssl ca -config openssl.cnf -revoke certname.pem
Note - After each revocation recreate `distribution.crl` and save it.


## How i revoked certificates
added crl to `ca.root.pem` throught the `openssl.cnf` division
	
	[ v3_ca ]
	# Extensions for a typical CA (`man x509v3_config`).
	subjectKeyIdentifier = hash
	authorityKeyIdentifier = keyid:always,issuer
	basicConstraints = critical, CA:true
	crlDistributionPoints = URI:http://0.0.0.0:8000/distripoint.crl
	keyUsage = critical, digitalSignature, cRLSign, keyCertSign

then added crl to `certname.pem` when signinig it throught the command 

	openssl ca -batch -create_serial -config openssl.cnf -cert ca.root.pem -keyfile ca.key.pem -passin pass:KeyPassword -in keyname.csr -out certname.pem -extensions usr_cert

and it worked as i updated the division (`usr_crt`) of `openssl.cnf`

	[ usr_cert ]
	# Extensions for client certificates (`man x509v3_config`).
	basicConstraints = CA:TRUE
	nsCertType = client, email
	nsComment = "OpenSSL Generated Client Certificate, Libreswan Managing Interface"
	subjectKeyIdentifier=hash
	authorityKeyIdentifier=keyid,issuer
	keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
	crlDistributionPoints = URI:http://0.0.0.0:8000/distripoint.crl
	extendedKeyUsage = clientAuth, emailProtection
