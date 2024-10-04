# Network

#### Video Demo: [Network](https://youtu.be/ou5z6xs0qQA)

## Problem to Solve 

Design a Twitter-like social network website for making posts and following users.

## Understanding

The `network` project is a Django-based web application.

The URL configuration is defined in `network/urls.py`, which includes routes for the `index` page, `login`, `logout`, and `registration`. These routes are linked to views defined in `network/views.py`, each handling specific functionality:
* The `index` view currently returns a basic, mostly-empty template.
* The `login_view` renders a login form when accessed via a `GET` request. If a `POST` request is submitted with valid credentials, the user is authenticated and redirected to the index page.
* The `logout_view` logs the user out and redirects to the index page.
* The `register` view displays a registration form and creates a new user when the form is submitted.
* The application can be started by running python manage.py runserver, after which the web interface can be accessed through a browser. Upon registration, users can log in, and the page will reflect the signed-in status. The HTML layout, defined in `network/templates/network/layout.html`, uses conditions to render different content depending on whether the user is authenticated. This ensures that features like user-specific links and content are only visible when appropriate.

In `network/models.py`, the models for the application are defined. The project starts with a `User` model, which inherits from Django's `AbstractUser`, providing fields such as username, email, and password. Additional fields can be added if there is more information about the user that needs to be stored. Other models will also need to be added to represent posts, likes, and followers, allowing the application to handle core social network features.

Whenever changes are made to the models, it is necessary to run migrations using `python manage.py makemigrations` followed by `python manage.py migrate` to update the database schema accordingly.

## Specification

TODO
