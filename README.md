# Application Structure:

- *app.yaml*: flask definitions including paths for static files, handlers, etc
- *appengine_config.py*: configuration for GAE to include lib folder in push
- *main.py*: the main flask application
- *main_test.py*: test cases for the main flask application
- *requirements.txt*: a list of third party python dependencies for the application
- *lib*: directory of external library dependencies, generated by running `pip install -r requirements.txt -t lib/`
- *static*: a directory of static resources (e.g. css, js, etc) for the application
- *templates*: a directory of templates to be rendered by the flask application