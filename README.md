# Postforum App

## Here is my flask app submission

I have created an app in the style of mytwits but have restyled it to be a generic forum website, which gives logged in users the ability to created threads and have discussions by replying to those thread / posts.

You can create an account and log in and make posts under that username. you can delete your own posts and reply to anyones posts. You can log out too. It has an api where you can make push and posts requests

The things I've implemented that are not in the mytwits app are the abililty to reply to posts and to sign up for an account. For displaying the replies I created a nested jinja for loop to loop over the replies for each posts and display them if they are related to that post.  I've also added some css styling in the static directory, but mainly used the default bootstrap styles.

To do this I added some methods to the dbhelper object such as gettings all replys for a certain post, getting the user id of who made a post. Getting the user for a certain id, checking how many replies there are to a post, one for adding a reply. I also re-implemented all the basic querys used in the mytwits application. This is all contained in the dbhelper.py file. I also created seperate templates for each method such as adding a reply and deleting a post and all the other funcitonalities. These are rendered according to the route from the main myforumapp.py file.

In the dump.sql file I implemented the schema for the database of the app using the mytwits schema as a basic model and adding another table for replys which is linked users table and the posts table via foreign keys. 

I also added some IP address info at the bottom regarding site and the client with the thought of doing something more with it but didn't add anything more than disaplying them.

## The commit history for this project can be viewed [HERE](https://gitlab.doc.gold.ac.uk/ljame002/term2-labs/commits/master)

## App url:

http://doc.gold.ac.uk/usr/336

## Login Credentials to use:

username: bob
password: pass
