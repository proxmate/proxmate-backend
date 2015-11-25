# Proxmate

## Overview

Proxmate is a browser plug-in service using web proxy technology to allow users to easily access certain web content that would normally not be accessible for them due to geo blocking of IPs.


## Product components

* Chrome (and Opera) plugin: https://github.com/SecureSoftwareVenture/proxmate-chrome
* Backend: https://github.com/SecureSoftwareVenture/proxmate-backend

### Chrome

This is the plugin that installs as ad-on in Chrome browsers.

### Backend

This is the software that is used by the Chrome plugin in order to make Proxmate operational.


## Configuration

- `apt-get install ipython git python-setuptools python-pip python-mysqldb python-dev memcached python-memcache`
- `apt-get install apache2 phpmyadmin mysql-server nginx uwsgi-plugin-python libjpeg8-dev zlib1g-dev`

___

- `pip install -r requirements.txt`

___

- `python manage.py migrate`
- `python manage.py runserver`

___
