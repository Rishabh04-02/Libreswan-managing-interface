# Libreswan-managing-interface
Managing Interface for Libreswan VPN software.

* The project is built using [django](https://github.com/django/django).
* Django version - [1.11.13](https://www.djangoproject.com/weblog/2015/jun/25/roadmap/) LTS.
* Serving Django Applications with Apache and mod_wsgi - [Reference](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7).
* [Django Documentation](https://docs.djangoproject.com/en/1.11/contents/) - followed.
* Sample database file ``libreswan_managing_interface/sample_database.cnf``. Create a new file named ``database.cnf`` in the same directory as that of ``sample_database.cnf`` and paste the contents of ``sample_database.cnf`` in it and modify the contents for establishing database connectivity.


# Initial project setup/First time installation

* Migrating the databases using the management script:

```
cd ~/libreswan_managing_interface
./manage.py makemigrations
./manage.py migrate
```

* Create an administrative user for the project by typing:

```
./manage.py createsuperuser
```
This will let you select a username, provide an email address, and choose and confirm a password.

* Now collecting all of the static content into the directory location:

```
./manage.py collectstatic
```
The static files will be placed in a directory called static within the project directory.

Testing the project by starting up the Django development server with this command:

```
sudo ./manage.py runserver 127.0.0.1:8000
```
Note - Use ``sudo`` before running server as it needs to write ``etc/conf.d/``  and will generate secured keys and certificates.

In the web browser, visit the server's domain name or IP address followed by ``:8000``:
```
http://server_domain_or_IP:8000
```
