from src.establish_connection import VPNConnector
from src.configuration_handler import read_credentials

if __name__ == "__main__":
    def on_success():
        print("SUCCESS - Connection established")


    def on_failure():
        print("FAILURE - Unable to establish connection.")


    def on_already_connected(ip_address):
        print("Your public ipv4 is: {} \nSeems like you already connected to the vpn.\nExiting ".format(ip_address))
        exit(-1)


    def read_credentials_failed():
        print("Can not read credentials. Make sure they are provided as expected in the "
              "configure_connection.yaml\nExiting")
        exit(-1)

    connector = VPNConnector(read_credentials_failed, on_already_connected, on_failure, on_success, debug=True)
    read_credentials(connector)
    connector.establish_connection()
    connector.child_process.wait()