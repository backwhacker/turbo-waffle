# Turbo Waffle

Use your Echo or Echo Dot to turn on/off stuff, now with SSH.

## Usage

- "Alexa, turn on $thing"
- "Alexa, turn off the $thing"

## Install

- Clone this repository
- Install python (I used 2.7.9 but should work with 3.x)
- Install wakeonlan py package (`pip install wakeonlan` or from source)
- Start the script with `python turbo-waffle.py`

### Supervisord

You can use supervisord to run your script
Sample config:

```
[program:turbo-waffle]
command=/usr/bin/python /srv/turbo-waffle/turbo-waffle.py
process_name=%(program_name)s
numprocs=1
directory=/srv/turbo-waffle/
autorestart=true
user=nobody                   ; setuid to this UNIX account to run the program
redirect_stderr=true
stdout_logfile=/var/log/turbo-waffle.log
stdout_logfile_maxbytes=1MB
stdout_capture_maxbytes=1MB
```

## Thanks

- https://github.com/toddmedema/echo
- https://github.com/efpe/amazon-alexa-lg-tv

