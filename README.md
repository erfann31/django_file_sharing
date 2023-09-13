![5](https://github.com/erfann31/django_file_sharing/assets/75057732/61b25650-28b7-4f47-93b0-92e2f724db76)# django_file_sharing
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

## Previews
![1](https://github.com/erfann31/django_file_sharing/assets/75057732/affff44b-fd2e-4801-b543-aff351d9ab96)
![2](https://github.com/erfann31/django_file_sharing/assets/75057732/d22cb003-8bef-44b3-90d3-06f1ad39e5be)
![3](https://github.com/erfann31/django_file_sharing/assets/75057732/5943d05c-ed69-41e0-8eff-3aa466e48843)
![4](https://github.com/erfann31/django_file_sharing/assets/75057732/b612229c-4cd7-4d1a-bd66-28b0bcda0e6f)
![5](https://github.com/erfann31/django_file_sharing/assets/75057732/83b1ab96-c608-4da8-81d7-6f03e7b15aac)
![6](https://github.com/erfann31/django_file_sharing/assets/75057732/fb545cd9-98e3-45e8-9b0c-ac159dcff00c)



