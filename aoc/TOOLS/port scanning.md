# Rustscanner

Rustscanner is a modern take on nmap

https://github.com/bee-san/RustScan


rustscan 10.66.145.190



# nmap quick 20 ports

sudo nmap -sS -T5 --top-ports 20 $MACHINE_IP

# nmap quick 100 ports

sudo nmap -sS -T4 -F $MACHINE_IP

# nmap quick 1000 ports

sudo nmap -sS -p- $MACHINE_IP



sudo nmap -sn 10.66.64.0/18 -oG hosts.grep
grep "Status: Up" hosts.grep | cut -d " " -f 2 > live_hosts.txt


sudo nmap -O -sV -T4 -iL live_hosts.txt -oN os_scan.txt