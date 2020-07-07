#!/bin/bash
#
# Listens for UDP message broadcast on a port and if the message
# matches the signature of what's expected for the status indicator,
# it opens the control UI of the indicator in a Chrome browser.

# which port to listen for broadcasts on
LISTEN_PORT=1234

echo "Status controller UI launcher"

while true; do
  echo "Listening for broadcast..."
  availability=$(nc -ul $LISTEN_PORT -w 0)

  echo "Received broadcast: " $availability
  echo "Parsing components..."
  OIFS=$IFS
  IFS=':'
  read -ra MSG <<< "$availability"
  IFS=$OIFS

  echo "Determining next course of action..."
  if [ "${MSG[0]}" == "AVAILABILITY" ]; then
    endpointIp="${MSG[1]}"
    endpointPort="${MSG[2]}"

    if [ -z "${endpointIp}" ]; then
      echo "Message is missing IP address"
    elif [ -z "${endpointPort}" ]; then
      echo "Message is missing port number"
    else
      echo "Found endpoint: ${endpointIp}:${endpointPort}"
      echo "Opening in Chrome..."
      /usr/bin/open -a "/Applications/Google Chrome.app" "http://${endpointIp}:${endpointPort}"
      break
    fi
  else
    echo "Message '${availability}' did not match expected format - likely a different broadcast"
  fi
done
