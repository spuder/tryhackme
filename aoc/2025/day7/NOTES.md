tbfc-devqa01
10.65.140.95


Scan TCP 

nmap -p- --script=banner 10.65.140.95

Starting Nmap 7.80 ( https://nmap.org ) at 2025-12-07 20:24 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.65.140.95
Host is up (0.00040s latency).
Not shown: 65531 filtered ports
PORT      STATE SERVICE
22/tcp    open  ssh
|_banner: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.14
80/tcp    open  http
21212/tcp open  trinket-agent
|_banner: 220 (vsFTPd 3.0.5)
25251/tcp open  unknown
|_banner: TBFC maintd v0.2\x0AType HELP for commands.



Also scan UDP

nmap -sU 10.65.140.95