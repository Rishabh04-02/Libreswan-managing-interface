**Note** - Before Proceeding make sure you've read the [INSTALLATION INSTRUCTIONS](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/INSTALLATION_INSTRUCTIONS.md)

# Libreswan Administration Guide
This guide aims to improve user experience when using Libreswan Administration Interface.

## Functionalities 
![Functionalities](https://image.ibb.co/hH1zRU/01_Functionalities.png)

* Add User
* Create VPN for remote host connection profiles
* Create Subnet to Subnet VPN connection profiles
* Generate Private Key (CA private key)
* Generate root certificate (Using CA private key)
* Create certificate configurations (for user certificates)
* Generate user certificates
* Revoke user certificates
* Enable user (Allow User to login)
* Disable user (Disallow User to login)
* Delete User Data (Keys & Certificates)
* Delete all certificates (User, CA & Default Certificate configuration)
* Account activation (email verification)
* Download the certificate generated for user

### Add User
This will add the user to the interface. To add user visit the following link or choose the add user option from the Libreswan Interface(top right corner)

	http://HOSTNAME/admin/auth/user/add/
![Add user Image](https://image.ibb.co/fHQ4t9/02_Add_User.png)

### Create VPN for remote host connection profiles
It lets you add and configure your connection and then saving the connection by using the option `write to file`

	http://HOSTNAME/admin/vpn/vpnforremotehost/
![Create VPN for remote host connection profiles](https://image.ibb.co/cKBcD9/03_VPNfor_Remote_Host.png)

After adding and saving configuration, select `write to file` action from the dropdown menu. You'll see a success message as in the image below.
![Success - VPN for remote host connection profiles](https://image.ibb.co/kBKKRU/08_Success_VPNfor_Remote_Host.png)

### Create Subnet to Subnet VPN connection profiles
It lets you add and configure your connection and then saving the connection by using the option `write to file`.

	http://HOSTNAME/admin/vpn/subnettosubnet/
![Create Subnet to Subnet VPN connection profiles](https://image.ibb.co/gdF4t9/05_Subnetto_Subnet_Conection.png)

After adding and saving configuration, select `write to file` action from the dropdown menu. You'll see a success message as in the image below.
![Success - Subnet to Subnet VPN connection profiles](https://image.ibb.co/gBMAY9/06_Success_Subnetto_Subnet_Conection.png)

### Generate Private Key (CA private key)
This will generate a CA private key and will be used to sign all the user certificates. User just need to choose `save key as private key` action from dropdown after selecting the desired key name and password.

	http://HOSTNAME/admin/vpn/generateprivatekey/
![CA Private Key](https://image.ibb.co/fqL4t9/07_Generate_CAPrivate_Key.png)

After choosing the option `save key as private key` you'll see a success message as shown in the image below.
![Success - CA Private Key](https://image.ibb.co/edZVY9/04_Success_Generate_CAPrivate_Key.png)

### Generate root certificate (Using CA private key)
This will be generated using the CA private key. Just select the desired configuration and choose action `Generate root certificate` from the dropdown menu.

	http://HOSTNAME/admin/vpn/generaterootcertificate/
![Generate Root certificate](https://image.ibb.co/ddOPt9/09_Generate_CARoot_Certificate.png)

After choosing the above mentioned action you'll see a success message as shown in the image below.
![Success - Generate Root certificate](https://image.ibb.co/i6KKRU/10_Success_Generate_CARoot_Certificate.png)

### Create certificate configurations (for user certificates)
This will let you add multiple certificate configuration to the interface. It will then provide an action from dropdown menu to `Save configuration as Default configuration`  after adding and choosing the desired certificate configuration, which means saving the configuration which the user generated certificates will have.

	http://HOSTNAME/admin/vpn/certificateconfiguration/
![Save Configuration as Default configuration](https://image.ibb.co/iXYPt9/11_User_Certificateconfiguration.png)

After `Save configuration as Default configuration` you'll see a success message as shown in the image below.
![Save Configuration as Default configuration](https://image.ibb.co/fOjVY9/12_Success_User_Certificateconfiguration.png)

Note - Please save any of the added configuration as default configuration before you begin to generate user certificates.

### Generate user certificates
This will generate the CA signed certificates for users.

	http://HOSTNAME/admin/vpn/generatecertificate/

#### Prerequisites
* User should have verified email(activated account) -	It can be done by visiting the following link and entering the valid details:

		http://HOSTNAME/activate_account/
	On entering the valid credentials the user will get the account activation link in email(registered email id). Here is one such link:

		http://HOSTNAME/activate/LQ/4xt-60306def302911f8e957/

* Admin should have completed the step - **Create certificate configurations (for user certificates)**

![Generate user certificates](https://image.ibb.co/mtvhfp/13_Generate_User_Certificate.png)

After choosing the action `Generate User certificate` from the dropdown menu, you'll see a success message as shown in the image below.
![Success - Generate user certificates](https://image.ibb.co/b6iDmU/14_Success_Generate_User_Certificate.png)

### Revoke user certificates
It is used to revoke the generated user certificates. It can be done by choosing the action `Revoke User certificate` from the dropdown menu after selection the users from the following url.

	http://HOSTNAME/admin/vpn/generatecertificate/
![Revoke User certificate](https://image.ibb.co/iXhTLp/16_Revoke_User_Certificate.png)

After successfully revoking the certificate you'll see a success message as shown in the image below.
![Success - Revoke User certificate](https://image.ibb.co/gxcv0p/17_Success_Revoke_User_Certificate.png)

### Enable user (Allow User to login)
It enables the user to login to this interface and download the certificate generated for him/her. *By default all user accounts are enabled*. To enable any disabled account just visit the following url, then select the users and then choose the action `Enable User(Allow user to login)` from the dropdown menu.

	http://HOSTNAME/admin/auth/user/
![Disable user](https://image.ibb.co/giexD9/24_Enable_User.png)

After enabling user account successfully you'll see a success message as shown in the image below.
![Success - Disable user](https://image.ibb.co/c6qhfp/25_Success_Enable_User.png)

### Disable user (Disallow User to login)
It prevents user from login to this interface. When the user account is disabled user can't use any functionality of this interface. User can be Enabled by the administrator anytime. To disable any user account just visit the following url, then select the users and then choose the action `Disable User(Disallow user to login)` from the dropdown menu.

	http://HOSTNAME/admin/auth/user/
![Disable user](https://image.ibb.co/dvHHD9/22_Disable_User.png)

After disabling user successfully you'll see a success message as shown in the image below.
![Success - Disable user](https://image.ibb.co/jTxTLp/23_Success_Disable_User.png)

### Delete User Data (Keys & Certificates)
This will delete the keys and certificates created for the user. It's good to revoke a certificate first then use this option as that will prevent the certificate from being used. After visiting the following url select users and then from dropdown menu select the action `Delete User Data (Keys & Certificates)` 

	http://HOSTNAME/admin/vpn/generatecertificate/
![Delete User Data](https://image.ibb.co/f2qtmU/18_Delete_User_Data.png)

After successfully deleting the user data you'll see success message as shown in the image below.
![Success - Delete User Data](https://image.ibb.co/dMk4t9/19_Success_Delete_User_Data.png)

### Delete all certificates (User, CA & Default Certificate configuration)
This will delete all the User generated certificates as well as CA certificates and default certificate configuration. Select any user then from the dropdown choose the action `Delete all certificates (User, CA)` This will delete everything from the system.

	http://HOSTNAME/admin/vpn/generatecertificate/
OR 

	http://HOSTNAME/admin/auth/user/
![Delete all certificates](https://image.ibb.co/mZoPt9/20_Delete_All_Certificates.png)

After successfully deleting all the certificates you'll see success message as shown in the image below.
![Success - Delete all certificates](https://image.ibb.co/n4uxD9/21_Success_Delete_All_Certificates.png)

### Account activation (email verification)
This lets the user to activate the account and hence use the functionality of the interface.
User can activate his/her account by visiting the following link and entering the valid login credentials:
	
	http://HOSTNAME/activate_account/

After that user will receive an email on it's registered email id with the activation link. eg. sample mail sent to user:

	Subject: Hello newuser - Activate Your Libreswan Account
	From: noreply@libreswan.org
	To: newuser@gmail.com
	Hi ,
	Please click on the link below to confirm your registration:
	http://HOSTNAME/activate/MO/4uj-759a7a1a792880768519/

### Download the certificate generated for user
This will let user download the certificate generated for him/her and after successful login user will also be able to see the generated password for his/her certificate.
For user login - User should enter login credentials on `http://HOSTNAME/` in the user login section.
