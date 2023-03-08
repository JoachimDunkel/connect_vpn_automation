from urllib.request import urlopen
import re as r


def get_public_ip():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)


if __name__ == "__main__":
    print(get_public_ip())
