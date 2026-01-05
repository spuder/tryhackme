# ffuf

use `-s` for silent and `-fc 403,404` to hide errors

Search for files

`ffuf -u http://10.65.147.30/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -s -fc 403,404`

Search for just web extensions (.aspx, .html, .css, .exe)

`ffuf -u http://10.65.147.30/indexFUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/web-extensions.txt -s -fc 403,404`

Search for 'words' but add .php and .txt

`ffuf -u http://10.65.147.30/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt -e .php,.txt -s -fc 403,404`

Search for directories

`ffuf -u http://10.65.147.30/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt -s -fc 403,404` 