Django-comment is a commenting system building on top of django. 


# Introductions
* the app is based on bootstrap[>=3]

* the app displays a comment form  and get the list of comments for some object. 

    All users who has actually logged in can add comments. Both owners and superusers can edit and delete comments.
    All users can vote for comments which are extremely clever.


# Installation #
You should to copy the following apps into your project:

- **comment**

- **acount**

   application acount is responsible for login and logout
 
- **html5tags**

   html5tags provide basic style for comment form and pagination

- **toollib**

   toollib is a common module for rendering template, pagination etc

You also should install django_avatar 

- **django_avatar**

   avatar should be installed for handling user avatars. invoke the following command:

      *** easy_install django_avatar ***


# Configuration #

   - add the following to your **settings.py**

    **INSTALLED_APPS += (
        'comment',
        'acount',
        'html5tags',
        'toollib'
        'avatar',
        )**

   - add the following to your **urls.py**

   **urlpatterns += patterns('',
                  url(r'', include('comment.urls')),
                  url(r'auth/', include('account.urls')),
                  )**

                      
# How to use 'comment' ? #

-  you should use **syncdb** to install comment,account and avatar model before running.

-  Wherever you want to display comments for one object, first load the comments template tags:
   ** {% load comment_tags %} **

-  Then, use the comment_list tag to display comments:
   ** {% comments app_name model_name 1 prefix pageno request %}**

object_pk: id of some object(e.g. article or blog entry) which is commented
model_name: the object's model name
app: the app which the object belongs to


# Global Settings
- There are a number of settings available to easily customize the comments that appear on the site. You can find them in file config.py. Listed below are those settings:

   PAGE_SIZE：  An integers displaying amount of comments each page. Defaults to 10


# Other
- If you still have some questions, you can refer to example
