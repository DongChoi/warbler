Warbler

Warbler is a Twitter clone project created using Flask, Jinja, SQLAlchemy, PostgreSQL, RDS, and Elastic Beanstalk. The goal of this project is to provide users with a RESTful API backend allowing them to create, delete, like, and unlike messages. Additionally, the application implements user sign up, authorization, and authentication using Flask sessions and cookies.

Features
User authentication (login, signup, logout)
Tweeting (creating, deleting, editing tweets)
Following/unfollowing other users
Timeline of tweets from followed users
Search functionality for users and tweets
Hashtag support for tweets
User profiles with bio and profile picture
Technologies used
Flask
Jinja
SQLAlchemy
PostgreSQL
RDS
Elastic Beanstalk
Installation
Clone the repository
Install the dependencies using pip install -r requirements.txt
Create a .env file and add the required environment variables (such as database credentials)
Start the application using flask run
Usage
Once the application is started, users can navigate to the app's homepage and sign up for an account or log in to an existing account. From there, users can create, edit, and delete tweets, follow and unfollow other users, and view their timeline. Users can also search for other users and tweets using the search functionality.

Demo
A live demo of the application can be found on [Github](insert link here).

Additional Information
This project was completed in February 2023
The application leverages SQLAlchemy to dynamically query the relational database using many-to-many relationships
Server side rendering is achieved using Jinja, flash messages, and template inheritance
