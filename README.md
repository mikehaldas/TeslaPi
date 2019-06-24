<h1>TeslaPi</h1>
TelsaPi is a security alarm project that integrates an outdoor motion sensor with the headlights and horn of a Tesla car. It works with all models. The project uses a Raspberry Pi, an outdoor PIR motion detector, and the Tesla API. The code is written in the Python programming language.
<br><br>
Written by Mike Haldas
<hr>
<h2>Installation</h2>
Integration with the Telsa API is done using the TeslaJSON API wrapper written by Greg Glockner. (https://github.com/gglockner/teslajson).

Open the terminal program on your Raspbery Pi run the following commands. Please note that before you run the program, you should also complete the wiring setup in the next section.
<ol>
  <li>wget https://github.com/gglockner/teslajson/archive/master.zip</li>
  <li>unzip master.zip</li>
  <li>cd teslajson-master</li>
  <li>sudo python setup.py install</li>
  <li>cd ..</li>
  <li>rm master.zip</li>
  <li>wget https://github.com/mikehaldas/TeslaPi/archive/master.zip</li>
  <li>unzip master.zip</li>
  <li>cd TeslaPi-master</li>
  <li>Edit the vars.py file. You should enter your user ID and password that you use on the teslamotors.com website for the USERID and PASS variables, then save the file and exit.</li> 
  </ol>
  If you want to test the API communication with your Tesla before you wire the motion detector to your Raspberry Pi, you can run the following command: python gps.py
  
  This will connect to your car and print the GPS longitute and lattitute. If the program gives you an error the first time you run it, try to run it again. If you car is sleeping the first time it is run, there may be an error. This is a bug that needs to be fixed.
  
  When you are ready to run TeslaPi, use the following command: python TeslaPi.py

<h2>Raspberry Pi / Motion Sensor Wiring</h2>
<img src="https://www.cctvcamerapros.com/v/images/RPi/Raspberry-Pi-Motion-Sensor-Alarm.jpg" alt="Raspberry Pi Motion Sensor Alarm">
Here is a link to the outdoor motion sensor that was used to test this project. Please note that it is shown in the above wiring diagram with the front cover removed to show the location of the power and output terminals. https://www.cctvcamerapros.com/PIR-Outdoor-Motion-Sensor-p/takex-ms-100e.htm
<br>
This is how it is wired.
<ol>
  <li>The outputs of the motion sensor are wired to GPIO 16 pin and a ground pin.</li>
  <li>A 12V DC power supply is used to power the motion detector.</li>
  <li>Although not pictured, the Raspberry Pi obviously also needs to be connected to a power source.</li>
  <li>The Raspberry Pi must be connected to an Internet connection either via WIFI or the hard wired Ethernet port.</li>
</ol>
  <hr>
  <h2>TelsaPi Alarm System Logic</h2>
  There are a lot of comments in the TeslaPi.py program that explain the logic of the application. The program basically works as follows.
  <ul>
  <li>After you run TeslaPi.py, a connection is initiated to your Tesla.</li>
  <li>The program waits for the motion detector to sense motion.</li>
  <li>When motion is detected, an alarm cycle begins.</li>
  <li>An alarm cycle consists of a duration and 5 escalation levels.</li>
  <li>Each escalation level has it's own set of alarm actions that can be easily modified. For example: level 1 - flash headlight 3x, level 2, flash headlights 3x and beep horn 1x, level 3 - flash lights 5x and beep horn 2x, etc.</li>
  <li>If motion is continuous or occurs again within the alarm cycle threshold, the escalation level is incremented.</li>
  <li>The escalation level resets after level 5 or if the alarm cycle threshold time has passed.</li>
  

