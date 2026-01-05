# Password cracking

## Dictionary Attacks

```
pdfcrack -f flag.pdf -w /usr/share/wordlists/rockyou.txt
```


```
zip2john flag.zip > ziphash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt ziphash.txt
```

## Masking Attacks

