YHandler
========

Yahoo Fantasy Sports OAuth And Request Handler

This is the Python Script I use to access the Yahoo Fantasy Sports API via OAuth for my desktop app. It's far from polished, and not the most generalized.  However, following these steps should work:
- Place your consumer key, and consumer secret in the auth.csv file 
- call: import from YHandler *
- create a handler with: var_name = YHandler('auth.csv')

The app needs the following libraries, which you can install using pip:

**Requests:** http://docs.python-requests.org/en/latest/

**Requests-oauth:** https://github.com/maraujop/requests-oauth
