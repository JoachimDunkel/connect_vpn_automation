# connect_vpn_automation

Connecting with open-vpn under Ubuntu is usually done via terminal.
This forces you to keep a terminal open for the connection.

There are existing GUI solutions that monitor an open-vpn connections, 
but these usually do not work if connecting to the network is done via a bash script that has to do additional stuff, like reading the company certificate. 

This solution is especially tailored to this use case.

After the application is properly setup, (See Section Setup) connecting to such a company vpn can then be done with one click and the connection stays open and can be monitored with an icon in the top bar.
No login necessary.

## Setup

When first starting the application it will create a `configure_connection.yaml` in the directory root.
No connection will be established until not all of it's parameters are properly supplied.
 (It should look as follows.)

```yaml

# Change this to your credentials (take a look at the source code if you are suspicious at that point. which is understandable)

SUDO_PW: ""
USER_NAME: ""
USER_PW: ""

# The public ipv4 address visible from the outside after connecting with the vpn.
# This is there to check if a connection was established. Or if you are already connected to the vpn via another ürpces.

VPN_PUB_IP: ""

# Path to the script that will run openvpn internally

OPENVPN_SCRIPT_PATH: ""

```

### Security issue

At the moment login credentials reside in a plain text file. This is a security issue, obviously. Use this project at your own risk.



