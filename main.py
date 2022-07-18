"""
Create a Golang or Python script that reads all ip addresses, from
STDIN or from a file for the purpose of detecting NTP, sends the
service a payload and successfully extracts the NTP version from the
response.
The script must be efficient.
It must be thread safe and use multiple goroutines or thread workers.
The hosts that do not have NTP do not need to be printed.
"""
from threading import Thread
import ntplib


def readIPAddressesFromFile(filename):
    ips = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            ip = line.strip()
            ips.append(ip)
    return ips


def checkNTP_withLib(ip):
    client = ntplib.NTPClient()
    versionsWorking = []
    maxVersion = 0
    version = 4  # we start by checking if it runs version 4
    versionFound = False

    while version >= 1 and versionFound is False:
        retries = 0
        while retries < 3 and versionFound is False:  # we do the request at most 3 times for each version
            try:
                response = client.request(ip, version=version)
                if version not in versionsWorking:
                    maxVersion = response.version
                versionFound = True
            except Exception:
                pass
            retries += 1
        version -= 1  # after each unsuccessful try, decrease the version

    if maxVersion != 0:
        print(f"{ip} runs NTP version {maxVersion}")
    else:  # the IP appears not to run NTP
        return


def main():
    ips = readIPAddressesFromFile("ip_addresses.txt")

    threads = []

    for ip in ips:
        thread = Thread(target=checkNTP_withLib, args=(ip,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


main()
