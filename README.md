<h1>TeslaPi</h1>
TelsaPi is a security alarm project that integrates an outdoor motion sensor with the headlights and horn of a Tesla car. It works with all models. The project uses a Raspberry Pi, an outdoor PIR motion detector, and the Tesla API. The code is written in the Python programming language.
<br><br>
Written by Mike Haldas
<hr>
<h2>Installation</h2>
your Raspbery Pi follow these steps. Please note that before you run the program, you should also complete the wiring setup in the next section.
<ol>
  <li>Open a terminal window.</li>
  <li>wget https://github.com/gglockner/teslajson/archive/master.zip</li>
  <li>unzip master.zip</li>
</ol>
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
<h2>Tesla API Integration</h2>
The integration with the Telsa API is done using the [TeslaJSON API written by Greg Glockner](https://github.com/gglockner/teslajson).
