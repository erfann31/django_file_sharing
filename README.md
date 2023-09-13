# django_file_sharing
this is a django application to share offline your file between your devices (Mac-Android-Win-Linux-Ios)
## Clone project


```
git clone https://github.com/erfann31/django_file_sharing.git
```

## Run this project

Go to project root and execute the following command in console to run the server: 

```
pip install -r requirements.txt
python manage.py makemigrations file
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
```

## Know your IP address 
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
Type ifconfig or ip a and press Enter. Look for your active network interface to find your IP address.</br>
