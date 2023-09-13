# django_file_sharing
This is a django application to share your file between your devices (Mac-Android-Win-Linux-Ios) **no need internet** 
## Clone project


```
git clone https://github.com/erfann31/django_file_sharing.git
```

## Run Project

Go to project root and execute the following command in console to run the Project: 

```
pip install -r requirements.txt
python manage.py makemigrations file
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
```

## Know Your IP Address 
### Windows

Press Win + R to open the Run dialog, type cmd, and press Enter.</br>
In the Command Prompt window, type ipconfig and press Enter. Look for the "IPv4 Address" under your active network connection.
### macOS

Click the Apple menu and choose "System Preferences."</br>
Select "Network."</br>
In the left sidebar, click on your active network connection (Wi-Fi or Ethernet).</br>
Your IP address will be displayed on the right side.</br>
### Linux:

Open a terminal window.</br>
Type ifconfig or ip and press Enter. Look for your active network interface to find your IP address.</br>
## File Sharing
To communicate and share files, your devices must be on the same network. It means that they should all be connected to the same Wi-Fi.</br>
Then you should search the IP address obtained in the previous step along with the port in your browser.</br>
```
http://your_server_ip:8080
```
For example:
```
http://192.168.1.1:8080
```
