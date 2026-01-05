```bash
sudo nmap -sS -p- $MACHINE_IP
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
25/tcp    open  smtp
8443/tcp  open  https-alt
21337/tcp open  unknown
```

```bash
nmap -p25 --script=smtp-commands,smtp-enum-users $MACHINE_IP
Starting Nmap 7.98 ( https://nmap.org ) at 2025-12-31 20:43 -0700
Nmap scan report for 10.66.164.77
Host is up (0.093s latency).

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-enum-users: 
|   root
|   admin
|   administrator
|   webadmin
|   sysadmin
|   netadmin
|   guest
|   user
|   web
|_  test
| smtp-commands: hostname, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
|_ 2.0.0 Commands: AUTH BDAT DATA EHLO ETRN HELO HELP MAIL NOOP QUIT RCPT RSET STARTTLS VRFY XCLIENT XFORWARD
```

port 8443

nginx/1.29.3


## Hopflix

sbreachblocker@easterbunnies.thm

123456

password has something to do with rabbits


## Hopsec Bank

## Mail


## Texts

44 7911 123456
