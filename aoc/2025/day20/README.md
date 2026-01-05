# Race Conditions

https://tryhackme.com/room/race-conditions-aoc2025-d7f0g3h6j9


Leverage burp repeater to send multiple requests in parallel. 

## Countermeasures

Use atomic database transactions so stock deduction and order creation execute as a single, consistent operation.
Perform a final stock validation right before committing the transaction to prevent overselling.
Implement idempotency keys for checkout requests to ensure duplicates aren’t processed multiple times.
Apply rate limiting or concurrency controls to block rapid, repeated checkout attempts from the same user or session.
