9 hosts, 1 firewall

sudo nmap -PR -sn 10.66.64.0/18
This found 68 hosts, pretty sure these are other peoples machines and are out of scope. 


sudo nmap -sn 10.66.64.0/18 -oG hosts.grep
grep "Status: Up" hosts.grep | cut -d " " -f 2 > live_hosts.txt


sudo nmap -O -sV -T4 -iL live_hosts.txt -oN os_scan.txt

rustscan -a 10.200.171.10
rustscan -a 10.200.171.11

10.200.171.10
- 22
- 80
10.200.171.11
- 22


SOC_ADMIN_EXECUTE_COMMAND:list_commands

SOC_ADMIN_EXECUTE_COMMAND:SOC_SYSTEM_INFO

set system.security.alerts.enabled 1
get system.security

```
{
    "action": "retrieve",
    "object": "securityalerts",
    "id": "example-id"
}
```

internal commands:
1. help
2. shutdown
3. reboot
4. update
5. start
6. stop
7. restart
8. logrotate
9. compress
10. uncompress
11. backup
12. restore
13. delete
14. find
15. mkdir
16. mv
17. cp
18. cat
19. echo
20. head
21. tail
22. grep
23. wc -l
24. cut
25. sort
26. sed
27. awk
28. vi
29. nano
30. telnet
31. ssh
32. netstat
33. ipconfig
34. ping
35. netimport
36. netexport
37. traceroute
38. nmap
39. openmp
40. omp
41. parallel
42. ginfo
43. grep -n
44. tr -s
45. cut -c
46. tail -f
47. awk '{print $1}'



./nmap -p 53 10.200.171.121 --script dns-zone-transfer,dns-brute
