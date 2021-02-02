# Test environment 
Our test environment is Raspberry Pi 3 with Raspberry Pi Camera V2.1 and distance sensor HC-SR04.

# Configuration
Take a note that to make changes (like changing branch) you need to run the command as `superuser`.
To make it be you need to type `su pi` (and execute this command) after that you will be asked to input password.
Use our password (you can get it from the dev team).

## Remote access to terminal
We are using `Dataplicity` for remote access to test environment.
If you want to have access to Raspberry Pi for test purposes send your email address and request to be added to [Jędrzej Polaczek](https://github.com/jedrzejpolaczek).

## Nginx Website
All commands you need to type in remote terminal.
* Gain access to remote terminal.
* To start `nginx` website just type `sudo service nginx restart`.
* To check if it works type `sudo netstat -an | grep LISTEN | grep :80` or visit website `https://colorless-havanese-8101.dataplicity.io/vnc.html`
* To stop `nginx` just type `sudo systemctl stop nginx`

## Remote access to desktop
All commands you need to type in remote terminal.
* Gain access to remote terminal.
* Use command `sudo /opt/remote_desktop/start`
    * On success you should see screen like this:
    
    ![Success start remote desktop](/doc/images/success_run_remote_desktop.png)

# Usage
Take a note that to make changes (like changing branch) you need to run the command as `superuser`.
To make it be you need to type `su pi` (and execute this command) after that you will be asked to input password.
Use our password (you can get it from the dev team).

## Terminal
To access test environment terminal visit website: 

`https://www.dataplicity.com/devices/5bc41fb9-ba63-4516-800a-c79969d3a526/`

## Repository
Repositories are under the path: 

`home/pi/Workplace/ai-smart-mirror` 

`home/pi/Workplace/ai-mask-model` 

## Website
To access test environment website visit website: 

```https://colorless-havanese-8101.dataplicity.io/```

Take a note that `nginx website` must be running to make it possible.

## Remote desktop
Go to the website: 

`https://colorless-havanese-8101.dataplicity.io/vnc.html`

You should see screen like this:
    
![Login to remote desktop](/doc/images/login_remote_desktop.png)

Use our password (you can get it from the dev team). 

Now you have access to remote desktop of test environment.

Take a note that `Remote access to desktop` must be running to make it possible.

## Raspberry Pi camera
### Making photo
All commands you need to type in remote terminal.

To make o photo just use command:

`raspistill -o your_photo_name.jpg`

New file under the name `your_photo_name.jpg` appear in the directory from where you execute the command.


## Troubleshooting
### Port unavailable
* Use command `sudo netstat -tunlp`
* Check what making port (default it is port 80) unavailable.
* Most of the time it will be nginx. Just shout it down by using command `sudo systemctl stop nginx`
* You may check the status of nginx if it stopted by typing `sudo systemctl status nginx`
