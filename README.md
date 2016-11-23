# db0.company

A division by zero.

### Specs

- Made with Django 1.9.4

### Quick start

```shell
virtualenv env
source env/bin/activate
pip install --upgrade setuptools
pip install -r requirements.txt
python manage.py runserver
```

Open your browser to [http://localhost:8000/](http://localhost:8000/) to see the website


### In production

- Create the file `db0/local_settings.py` with:
  ```python
  from boto.s3.connection import OrdinaryCallingFormat
  AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
  AWS_ACCESS_KEY_ID = 'your aws key'
  AWS_SECRET_ACCESS_KEY = 'your aws secret key'
  DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
  STATIC_FULL_URL = 'your bucket url'
  AWS_STORAGE_BUCKET_NAME = 'your bucket name'

  DEBUG = False
  SECRET_KEY = 'random generated secret key'
  ALLOWED_HOSTS = ['your domain']
  ```

- Compile the CSS:
  ```css
  lessc web/static/less/style.less web/static/css/style.css
  ```

- Upload the static files (including the compiled CSS) to your AWS bucket in a `static` folder

### Contributing

- Since the database file is in the repo, you don't need to bother migrating when updating.
  However, it's important to commit your migration files and the database files when changed.
  Don't commit test database objects.
