## ffuf

ffuf -u http://MACHINE_IP/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt

or add your own words to the list

ffuf -u http://MACHINE_IP/NORAJ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt:FOOBAR