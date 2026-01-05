# YARA

/home/ubuntu/Downloads/easter

YARA is rules for malware. Defined in a DSL

example 1
```
rule TBFC_KingMalhare_Trace
{
    meta:
        author = "Defender of SOC-mas"
        description = "Detects traces of King Malhare’s malware"
        date = "2025-10-10"
    strings:
        $s1 = "rundll32.exe" fullword ascii
        $s2 = "msvcrt.dll" fullword wide
        $url1 = /http:\/\/.*malhare.*/ nocase
    condition:
        any of them
}
```

example 2
```
rule TBFC_KingMalhare_Trace
{
    strings:
        $TBFC_string = "Christmas"

    condition:
        $TBFC_string 
}
```

It's time to complete the practical task! The blue team has to search for the keyword TBFC: followed by an ASCII alphanumeric keyword across the /home/ubuntu/Downloads/easter directory to extract the message sent by McSkidy. Can you help decode the message sent by McSkidy?