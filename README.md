# ai-smart-mirror

## Testing environment 
Our test environment is Raspberry Pi 3 with Raspberry Pi Camera V2.1 and distance sensor HC-SR04.

### Remote access to terminal

We are using `Dataplicity` for remote access to Raspberry Pi.
If you want to have access to Raspberry Pi for test purposes send your email address and request to be added to [Jędrzej Polaczek](https://github.com/jedrzejpolaczek).

### Remote access to desktop
* Gain access to remote terminal.
* Use command `sudo /opt/remote_desktop/start`
    * On success you should see screen like this:
    ![Success start remote desktop](/doc/images/success_run_remote_desktop.png)
* Go to the website `https://colorless-havanese-8101.dataplicity.io/vnc.html`
    * You should see screen like this:
    ![Login to remote desktop](/doc/images/login_remote_desktop.png)
    * Use there password.

### Troubleshooting
#### Port unavailable
* Use command `sudo netstat -tunlp`
* Check what making port (default it is port 80) unavailable.
* Most of the time it will be nginx. Just shout it down by using command `sudo systemctl stop nginx`
* You may check the status of nginx if it stopted by typing `sudo systemctl status nginx`

### How to use camera
#### Making photo
To make o photo just use command:
`raspistill -o your_photo_name.jpg`
New file under the name `your_photo_name.jpg` appear in the directory from where you execute the command.
#### Repository

Repository is under path `home/pi/Workplace/ai-smart-mirror`

#### Making changes

To make changes (like changing branch) you need to run the command as `superuser`.
To make it be you need to type `su pi` (and execute this comma

