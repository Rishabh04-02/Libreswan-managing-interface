# Installation Instructions

## Prerequisites (System)
Note - These can also be installed in virtualenv and not in whole system.

1. **Virtual Environment [Installation](https://virtualenv.pypa.io/en/stable/installation/)**

2. **Python 3.5 [Download](https://www.python.org/downloads/)**

		Version check:	$	python3 -V
		Output format:	Python 3.5.4

3. **pip3 [Install pip with Python3](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3)**

		Version check:	$	pip3 -V
		Output format:	pip 10.0.1 from ..../lib/python3.5/site-packages/pip (python 3.5)

## Steps to get the app running
1. **Install virtualenv and activate it [Installation](https://virtualenv.pypa.io/en/stable/installation/)**

	To install virtualenv, we will use the pip3 command, as shown below:

		$	pip3 install virtualenv
	Once it is installed, run a version check to verify that the installation has completed successfully:

		$	virtualenv --version
	We should see the following output, or something similar:

		Output format:	16.0.0
	virtualenv installed successfully.

2. **Install django 2.0.x**

	For that you first need to clone the `Libreswan-managing-interface` from the main repo/fork

		git clone git@github.com:Rishabh04-02/Libreswan-managing-interface.git
	OR

		git clone https://github.com/Rishabh04-02/Libreswan-managing-interface.git
	OR
	Download from [Libreswan-managing-interface - Github](https://github.com/Rishabh04-02/Libreswan-managing-interface)	after that get into the `Libreswan-managing-interface` directory
		
		cd Libreswan-managing-interface
	then create a virtualenv (`librenv` or any other name of your choice) in the folder using the command below:

		virtualenv librenv
	Now activate the virtualenv using the command below:

		source librenv/bin/activate
	You’ll know it’s activated once the prefix is changed to (`librenv`), which will look similar to the following depending on what directory you are in:

		(librenv) user@host:$
	Now install django 2.0.x using the command below:

		(librenv) user@host:$	pip3 install django==2.0.6
	check django version from one of the following two ways:

		python
		>>> import django
		>>> django.VERSION
		(2, 0, 0, 'final', 0)
	OR
		
		(librenv) user@host:$	python -c "import django; print(django.get_version())"

3. **Install `pip` in `virtualenv`**

	*Installing on Debian (Wheezy and newer) and Ubuntu (Trusty Tahr and newer) for Python 3.x*
	Run the following command from a terminal:

		sudo apt-get install python3-pip

	*Installing pip on CentOS 7 for Python 3.x*
	Assuming you installed Python 3.5 from EPEL, you can install Python 3's setup tools and use it to install pip.
	Note - First command requires you to have enabled EPEL for CentOS7

		sudo yum install python35-setuptools
		sudo easy_install pip

4. **Install mysqlclient in virtualenv**

	instal using the command below:

		(librenv) user@host:$	pip3 install mysqlclient
		
	while trying to install mysqlclient, you might get error due to pip cache. [Here is how to resolve it](https://github.com/PyMySQL/mysqlclient-python/issues/379).

5. **Configuration settings**

	* Add database login credentials
	Copy the contents of file `libreswan_managing_interface/sample_database.cnf` to file `libreswan_managing_interface/database.cnf` and update the details.

	* Add host ip to allowed IP's list
	In the `libreswan_managing_interface/settings.py` add your HOST_NAME to the following line:

		ALLOWED_HOSTS = [192.56.167.123]	#sample host IP

	* Add SMTP credentials
	To the file `libreswan_managing_interface/settings.py` add the SMTP user credentials to the following lines:

		    EMAIL_HOST = 'smtp.gmail.com'
		    EMAIL_HOST_USER = 'myemail@gmail.com'
		    EMAIL_HOST_PASSWORD = 'mypasswordhere'

	* Add HOSTNAME to `config/openssl.cnf`
	In this file on line `87` & `103` find the below mentioned content:

		    crlDistributionPoints = URI:http://HOSTNAME/crl/distripoint.crl
		
		Replace `HOSTNAME` with your hostname on both the lines. The URI will be included in generated certificates and will be used to revoke the certificates.

	* Set the Language & Timezone 	
	In the file `libreswan_managing_interface/settings.py` set the following options according to your convenience:

			LANGUAGE_CODE = 'en-us'
			TIME_ZONE = 'Asia/Kolkata'

6. **Preparing the app for running**

	* Migrating the databases using the management script using the command below:

			(librenv) user@host:$	./manage.py migrate

	* Create an administrative user for the project by typing:

			(librenv) user@host:$	./manage.py createsuperuser
		This will let you select a username, provide an email address, and choose and confirm a password.

	* Now collecting all of the static content into the directory location:
		
			(librenv) user@host:$	./manage.py collectstatic
		The static files will be placed in a directory called static within the project directory.

7. **Running the app**

	* If you want to generate VPN profile then follow the below instructions:

			(librenv) user@host:$	sudo su
			(librenv) root@host:$	./manage.py runserver 0.0.0.0:8000

		Now on your browser navigate to - `http://HOSTNAME:8000/`
		Your site will be running.
		Note - Becoming superuser (`sudo su`) before running server as it needs to write `etc/conf.d/` and will generate secured keys and certificates.

	* If you want to create certificates then follow the below instructions:
	It can be run using the commands below:

			(librenv) user@host:$	sudo su
			(librenv) root@host:$	./manage.py runserver 0.0.0.0:8000

		Now on your browser navigate to - `http://HOSTNAME:8000/`
		Your site will be running.
		Note - Becoming superuser (`sudo su`) before running server as it needs to write `etc/conf.d/` and will generate secured keys and certificates. This issue will be fixed soon.

8. **Deactivate the environment**

			(librenv) user@host:$	deactivate

### References
1) [https://www.digitalocean.com/community/tutorials/](https://www.digitalocean.com/community/tutorials/how-to-install-django-and-set-up-a-development-environment-on-ubuntu-16-04)
2) [Serve django app](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7)
3) [Django version](https://stackoverflow.com/questions/6468397/how-to-check-django-version/6468505#6468505)
4) [Virtualenv Installation](https://virtualenv.pypa.io/en/stable/installation/)
5) [Install pip with Python3](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3)
6) [Python Download](https://www.python.org/downloads/)
