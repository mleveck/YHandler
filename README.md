YHandler
========

Yahoo Fantasy Sports OAuth And Request Handler

This is the Python Script I use to access the Yahoo Fantasy Sports API via OAuth for my desktop app. It's far from polished, and not the most generalized.  However, following these steps should work:
- Place your consumer key, and consumer secret in the auth.csv file 
- call: from YHandler import *
- create a handler with: var_name = YHandler('auth.csv')

The app needs the following libraries, which you can install using pip:

**Requests:** http://docs.python-requests.org/en/latest/

**Requests-oauth:** https://github.com/maraujop/requests-oauth

**lxml**

This script has been udpated to work with newer versions of the requests and oauth. The previous script was broken when the requests library updated and removed hooks into the oauth header creation. The library now does this step manually.

Additional functions have been added to this library to make querying the Yahoo fantasy API a bit simpler. Soon this will be added as a package to PIP so no dependencies will be necessary.

*TODO* examples