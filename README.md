# email2print
An alternative to the shutdown Google Print service. Send you file to a predefined e-mail address and have it printed within minutes.

## How it works

email2print is supposed to be mitigate the lack of a simple way to remotely print to your home printer from anywhere in the world, after the Google Print service was shut down.
It uses an e-mail account with IMAP access to receive an e-mail message with attachments that should be printed. Downloads the attachments and prints them one by one. Additionally,
it can also upload the attached pdf files to paperless-ngx service which one can set up to store documents in private web service.

## Required packages

Please install python3-yaml package

sudo apt-get install python3-yaml

## Set up

### Requirements

1. E-mail account with IMAP access. Preferably GMAIL.
2. Optional: paperless-ngx instance

### Email configuration

I use GMAIL. The neat feature it has is that if you have an email address like *blahblah@gmail.com*, you can add a suffix to the login part separated by '+' and it will still reach your e-mail inbox. So I use *blahblah+print@gmail.com* and set up a rule which puts each email sent to that address in a Print subfolder of my e-mail inbox.

### Security

Apart from authorization security, there is no limitation to what can be printed and who can print. That might be undesirable from some users, but this limitation can probably be also introduced via means of e-mail rules. At least until something more robust is implemented.

### Configuration

Adjust config.yaml to your needs.

### Installation

- Put config.yaml in /etc/email2print
- Put email2print.py in /usr/local/bin
- Put email2print.service and email2print.timer in /usr/lib/systemd/system.
- Issue:

sudo systemctl daemon-reload
sudo systemctl enable email2print.timer

