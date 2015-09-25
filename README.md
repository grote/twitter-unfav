# Twitter UnFav

A script to remove favorited tweets from Twitter for privacy reasons.

To use this script, you first need to [generate a token to access your own account] (https://dev.twitter.com/oauth/overview/application-owner-access-tokens)

Then copy config.ini.sample to config.ini and fill in the secrets you got from Twitter.

This script is best run by a cronjob once a day:

```
# minute (0-59)
# |   hour (0-23)
# |   |    day of the month (1-31)
# |   |    |   month of the year (1-12 or Jan-Dec)
# |   |    |   |   day of the week (0-6 with 0=Sun or Sun-Sat)
# |   |    |   |   |   user
# |   |    |   |   |   |         commands
# |   |    |   |   |   |         |
  15  4    *   *   *   user      /path/to/twitter-unfav.py -t 14
```
