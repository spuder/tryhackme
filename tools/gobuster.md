gobuster dir -u https://$MACHINE_IP:8443 \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .txt,js,html,conf,zip,bak,py -k