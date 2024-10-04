# Network

#### Video Demo: [Network](https://youtu.be/ou5z6xs0qQA)

## Problem to Solve 

Design a Twitter(X)-like social network website for making posts and following users.

## Understanding

The `network` project is a Django-based web application.

The URL configuration is defined in `network/urls.py`, which includes routes for the `index` page, `login`, `logout`, and `registration`. These routes are linked to views defined in `network/views.py`, each handling specific functionality:
* The `index` view initially returns a basic, mostly-empty template.
* The `login_view` renders a login form when accessed via a `GET` request. If a `POST` request is submitted with valid credentials, the user is authenticated and redirected to the index page.
* The `logout_view` logs the user out and redirects to the index page.
* The `register` view displays a registration form and creates a new user when the form is submitted.
* The application can be started by running python manage.py runserver, after which the web interface can be accessed through a browser. Upon registration, users can log in, and the page will reflect the signed-in status. The HTML layout, defined in `network/templates/network/layout.html`, uses conditions to render different content depending on whether the user is authenticated. This ensures that features like user-specific links and content are only visible when appropriate.

In `network/models.py`, the models for the application are defined. The project starts with a `User` model, which inherits from Django's `AbstractUser`, providing fields such as username, email, and password. Additional fields can be added if there is more information about the user that needs to be stored. Other models will also need to be added to represent posts, likes, and followers, allowing the application to handle core social network features.

Whenever changes are made to the models, it is necessary to run migrations using `python manage.py makemigrations` followed by `python manage.py migrate` to update the database schema accordingly.

## Specification

The Network project implements several key features to create an interactive social network-like platform. Below are the functionalities developed for the application:

#### New Post:
Signed-in users are able to create new text-based posts by entering content into a text area and clicking a button to submit the post. The “New Post” feature can either be placed at the top of the “All Posts” page, or it can be placed on a separate page, allowing users to easily share their thoughts.

#### All Posts:
The “All Posts” link in the navigation bar takes users to a page where all posts from all users are displayed, with the most recent posts appearing first. Each post includes:
* The username of the poster
* The content of the post
* The date and time the post was made
* The number of “likes” the post has (which starts at 0 until the like functionality is implemented)

#### Profile Page:
Clicking on a username loads that user’s profile page. The profile page displays:
* The number of followers the user has
* The number of people the user is following
* All of the user’s posts in reverse chronological order
* For any signed-in user viewing another user’s profile, a “Follow” or “Unfollow” button is displayed, allowing them to toggle whether they are following the other user’s posts. A user cannot follow their own profile.

#### Following:
The “Following” link in the navigation bar takes the user to a page where they can view posts made by users they follow. This page functions like the “All Posts” page, but is filtered to show only the posts from followed users. This page is only accessible to users who are signed in.

#### Pagination:
On pages displaying posts, only 10 posts are shown per page. If there are more than 10 posts, a “Next” button is displayed to navigate to the next page of posts. A “Previous” button is also displayed if the user is not on the first page. This allows for efficient post browsing and a better user experience.

#### Edit Post:
Users can click an “Edit” button or link on any of their own posts to modify the content. When the "Edit" option is selected, the post’s content is replaced with a text area, allowing the user to update the post. Once the changes are made, clicking “Save” submits the edited post. JavaScript ensures that the post can be edited and saved without requiring the entire page to reload. For security, only the user who created a post is allowed to edit it, ensuring no unauthorized modifications to other users’ posts.

#### “Like” and “Unlike”:
Users can toggle between “liking” and “unliking” any post by clicking a button or link on the post. When a post is liked or unliked, JavaScript asynchronously sends the update to the server using the fetch API, which updates the like count on the page without requiring a reload. This ensures a smooth user experience and real-time feedback.

## Credit and Disclaimer

This problem originates from [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/projects/4/network/) and any solution here is explicitly for educational purposes only.
