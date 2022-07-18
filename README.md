# Technical Assessment
 <h2>Starting it</h2>
 Run using __python main.py__ in the project's directory. Put your IPs of interent in the **ip_addresses.txt** file. As it is now,
 this file contains the IPs of some public NTP servers taken from the internet.
 <h2>Thinking process</h2>
<ol>
 <li> I looked up the documentation of the NTP protocol and the differences between versions.</li>
 <li> I searched for ways to communicate with an NTP server in Python. Found two:
  <ul>
   <li> The [NTP library-ntplib](https://pypi.org/project/ntplib/) </li>
   <li> Crafting a packet manually and sending it to the server</li>
  </ul>
 </li>
 <li> I tried using the NTP library at first, because it seemed more simple.</li>
 <li> Upon sending a few requests with it and checking [the source code](https://github.com/cf-natali/ntplib) ,
      I noticed that the version in the response header is the same as the one sent in the request.
 </li>
 <li> Since there are only 4 NTP versions (and they are backwards-compatible), I decided that, for each IP, I will try to send a 
      request with version 4; if it goes through, I will conclude that the server has NTPv4. If this doesn't go through, I will
      try to send a request with version 3, and so on, until NTPv1. If none of these requests give a response, I will conclude
      that the IP does not run NTP.
 </li>
 <li> Because certain requests didn't go through the first one or two times, I decided to try for a maximum of 3 times before
      concluding that a certain version is not supported (although this slows the script down). 
 </li>
 <li> Lastly, I decided to check for each IP on a separate thread, for efficiency.
 </li>
</ol>

<h2>Alternative ideas</h2>
<ul>
 <li>Checking if port 123 is open before even sending an NTP request and sending requests only to the IPs
     for which the port is open. (I tried this briefly but got denied)
 </li>
 <li>Crafting the NTP packet manually and maybe figuring out a way to tell the version from the format of the response
     (this would take looking further at the exact differences between versions, as described in their RFCs)
 </li>
</ul>
