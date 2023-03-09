# This will add the command connect_vpn to ~/.bash_aliases
# If running connect_vpn does not work yet resource your terminal or make sure bash_aliases is uncommented in your ~/.bashrc
import resources
from configuration_handler import ensure_configuration_exists

print("Creating the configuration for you to fill out.")
ensure_configuration_exists()
print("Adding 'connect_vpn' command to ~/.bash_aliases")

alias_cmd = '\nalias connect_vpn="python3 {}"'.format(str(resources.PATH_CONNECT_VPN))
with open(str(resources.PATH_BASH_ALIASES), "a") as bash_aliases:
    bash_aliases.write(alias_cmd)


print("DONE. To run just type 'connect_vpn' into a terminal.")
