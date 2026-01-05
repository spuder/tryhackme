Before you can access the ports, you need to go to this port and enter he key
$MACHINE_IP:21337

http://$MACHINE_IP:8080/


sudo nmap -sS -sV $MACHINE_IP

22/tcp   open     ssh        OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open     http       nginx 1.24.0 (Ubuntu)
8000/tcp open     http-alt
8080/tcp open     http       SimpleHTTPServer 0.6 (Python 3.12.3)
9001/tcp filtered tor-orport


nmap -sV -sC -sU -p 22,80,8000,8080,9001 -O -oA full_enum $MACHINE_IP


curl "http://$MACHINE_IP:8080/%2e%2e/%2e%2e/etc/passwd"
curl: (52) Empty reply from server

curl -s -X POST "http://$MACHINE_IP:8080/cgi-bin/session_check.sh" \
     -d "id"
{"authed":false}


curl -s "http://$MACHINE_IP:8080/cgi-bin/key_flag.sh?door=hopper" | jq -r '.flag'
THM{REDACTED}

---

Multipe attack points. 

ssh is likely a no go unless I can find a private key
port 8080 is most likely
also finding the user email is very likely the next step. 

TODO: Find hopkins email

I've got the password to the system, I logged in, now I need to find the keycode. 


---

Why is the nginx misconfigured? 
Why is it using an old nginx?
Is there anything hackable about that nginx?
Why are the cameras hard coded to be inaccessible when the instructions says they work? 
What is the auth token for the SCADA termina? 
Can I hack the terminal? 
Is there anything I missed in the fakebook pages? 
How can I login as the admin on fakebook?
Does fakebook have a session storage I could pivot to admin account? 
Someone said they got the cameras on port 13400, why does that not show in port scan.



22/tcp    open  ssh
80/tcp    open  http
8000/tcp  open  http-alt
8080/tcp  open  http-proxy
9001/tcp  open  tor-orport
13400/tcp open  doip-data
13401/tcp open  unknown
13402/tcp open  unknown
13403/tcp open  unknown
13404/tcp open  unknown
21337/tcp open  unknown



---

:13401/v1/cameras
{"cameras":[{"desc":"Ward A entrance corridor","id":"cam-lobby","name":"Lobby","required_role":"guard","site":"HopSec Asylumn"},{"desc":"Service bay and cages","id":"cam-loading","name":"Supply Loading Dock 2","required_role":"guard","site":"HopSec Asylumn"},{"desc":"Jester Cell Block","id":"cam-parking","name":"Cell Block","required_role":"guard","site":"HopSec Asylumn"},{"desc":"Psych Ward Exit Gate","id":"cam-admin","name":"Psych Ward Exit","required_role":"admin","site":"HopSec HQ"}]}



