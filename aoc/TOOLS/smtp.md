If you find an open smtp server you can enumerate users. 

```

nmap --script smtp-commands,smtp-enum-users -p 25 10.64.156.234
25/tcp open  smtp
|_smtp-commands: hopaitech.thm, SIZE 33554432, 
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

```