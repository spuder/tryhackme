# XSS

## Reflected XSS

Example

Instead of 
`https://trygiftme.thm/search?term=gift`

You navigate to

`https://trygiftme.thm/search?term=<script>alert( atob("VEhNe0V2aWxfQnVubnl9") )</script>`



## Stored XSS

Stored is when you modify data stored in a database through a comment or post, then ever person who loads your comment will see the new html. Common with defacing. 



## Solutions

1. Disable dangerous rpaths (e.g. `innterHTML`, instead use `textContent`)
2. Make cookies inaccessable to JS with [HttpOnly](https://owasp.org/www-community/HttpOnly), [secure](https://owasp.org/www-community/controls/SecureCookieAttribute) or [SameSite](https://owasp.org/www-community/SameSite)


## Cheat Sheet

https://portswigger.net/web-security/cross-site-scripting/cheat-sheet



## Example

<script>alert('Reflected Meow Meow')</script>

