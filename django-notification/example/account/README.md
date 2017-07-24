#account docs#
# What can 'account' do for you ? #
account is a django app, containing frequently-used   features:register, login, logout, change__password,
 email_reset_password. Of course, it supports django admin, and supports South
to migrate db data.

# How to install 'account' ? #

- first, copy ***account*** app into your project.
- second, add ***account*** into INSTALLED_APPS in your **settings.py**, then include account's url as follow:

   ***urlpatterns += patterns('',
                        url(r'^auth/', include('account.urls')),
                        )***

- third, set ***LOGIN_URL = '/auth/login/'*** 

 ***LOGOUT_URL = '/auth/logout/'***

  **PROTOCOL = 'http'**  # or other protocol that your site support

  **DOMAIN = your domain**

  **CONNECT_US = your email**  #  tell user how to connect you
	
- last, you should use **syncdb** to install account's model before running.

# More config ?  #
- **EMAIL_SUFFIX**

   If you want to limit email to ***'@funshion.com'***, set as follow: 

    ***EMAIL_SUFFIX = '@funshion.com'***

   Default, no limits to email. 

    ***EMAIL_SUFFIX = ''***

- **PASSWORD__MIN__LENGTH**

   If you want to limit password length to ***大于等于6位***, set as follow:

    **PASSWORD_MIN_LENGTH** = 6
   
   Default, ***PASSWORD_MIN_LENGTH*** is 6.
 
- **REGISTER_AUTO_LOGIN**
  
   Default, when a user register successfully, then we'll login him automatically.

   You can change the default action by set: 

   ***REGISTER_AUTO_LOGIN = False***

# Connect us #


email to **dev-web-sys@funshion.com**



