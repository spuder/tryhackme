For stored XSS you can inject javascript as comments or any other form that doesn't validate inputs. 

Sometimes forms use client side checks (e.g. an age dropdown box which only has numbers, but you force the form to send a string instead). 