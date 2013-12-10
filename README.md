course-checker
==============

A small Python script for checking open courses. Uses Twilio.

```
$ cp config.template.py config.py
$ emacs config.py # Fill in your deets, yo
$ virtualenv venv
$ . venv/bin/activate
[venv] $ pip install -r requirements.txt
[venv] $ python coursechecker.py
```

And await those text messages! Best used on a separate server in conjunction with `screen`.
