# Container build documentation

This documents creating a container on webparametrics.co.uk, for the full build of the server, see

[https://bernie-skipole.github.io/webparametrics/](https://bernie-skipole.github.io/webparametrics/)

This container will serve a project 'exercise' giving timed audio prompts.

On server webparametrics.co.uk, as user bernard

lxc launch ubuntu:20.04 exercise

lxc list

This gives container ip address 10.105.192.40

lxc exec exercise -- /bin/bash

apt-get update

apt-get upgrade

apt-get install python3-pip

adduser bernard

record the password


## Install git, and clone skitest repository

Then as user bernard create an ssh key

runuser -l bernard

ssh-keygen -t rsa -b 4096 -C "bernie@skipole.co.uk"

copy contents of .ssh/id_rsa.pub to github

clone any required repositories

git clone git@github.com:bernie-skipole/exercise.git

copy /home/bernard/exercise to /home/bernard/www without the .git and .gitignore
(this rsync command can be used to update /www whenever git pull is used to update /exercise)

rsync -ua --exclude=".*" ~/exercise/ ~/www/

The exercise Python program requires the skipole package
and waitress

python3 -m pip install --user skipole

python3 -m pip install --user waitress

It should now be possible to run exercise

python3 ~/www/exercise/code/exercise.py

And you should get the message

Serving on http://0.0.0.0:8000

Use ctrl-c to exit, and set up a service to run this automatically

## Install exercise.service

as root, copy the file

cp /home/bernard/www/exercise.service /lib/systemd/system

Enable the service with

systemctl daemon-reload

systemctl enable exercise.service

systemctl start exercise

This starts /home/bernard/www/exercise/code/exercise.py on boot up.

The site will be visible at.

[https://webparametrics.co.uk/exercise](https://webparametrics.co.uk/exercise)



