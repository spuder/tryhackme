## Scan Local Network

`nmap -sn 192.168.11.0/24`

Note that if layer 2 adjacent, nmap will return the mac address because it sends a arp request. 
Otehrwise it just returns 'host is up'

## Dryrun

nmap -sL

sl does a scanlist so it only lists out which hosts _will_ be targeted. 


## Connect Scan

-sT tries to initate TCP 3 way handshake with every host. Most noisy

## Stealth Scan

-sS Does not complete 3 way handshake which is much more stealthy. 

-T has different levels, Aggressive takes less than 1 second, paranoid takes 9 hours. 

-T0 (paranoid)
-T1 (sneaky)
-T2 (polite)
-T3 (normal)
-T4 (aggressive)


## UDP Scan

-sU scans UDP services

## Fast Scan

-F scans 100 most popular

## Port Scans

-p[range] lets you pick ports, e.g. `-p10-1024`
-p-25 scans all ports between 1 and 25
-p- scans all ports (same as `-p1-65535`)

## OS Detection

-O detects the OS

`nmap -sS -O 192.168.124.211`

## Version Detection

-sV detects 'versions' of openssh ect..
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)

## All Detection

-A detects OS, Version and does traceroute


## Scan report

`-oN <filename>` Normal output
`-oX <filename>` XML output
`-oG <filename>` Grep/awk output

nmap -oG results.txt

## How it works

nmap sends 
- 2 ICMP echo requests
- 2 TCP packets to 443 with SYN flag set
- 2 TCP packets to port 80 with the ACK flag set


# Static nmap binaries

If a host doesn't have nmap installed, you can use a statically compiled binary

wget https://github.com/opsec-infosec/nmap-static-binaries/releases/download/v2/nmap-x64.tar.gz