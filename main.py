import dotenv
import os
import requests
import json
from datetime import datetime

dotenv.load_dotenv()
api_key = os.getenv("CF_KEY")
zone = os.getenv("ZONE")

with open("ip.txt", mode="r") as file:
    old_ip = file.read()

with open("subdomains.json") as subdomains:
    subdomains = json.load(subdomains)


def getPublicIp():
    res = requests.get("https://api.ipify.org")
    public_ip = res.content.decode("utf-8")
    return public_ip


def checkIpChange(ip, old_ip):
    if old_ip != ip:
        return ip, True
    else:
        return old_ip, False


def main():
    print(f"Running CDUS utlity at {datetime.now()}")
    public_ip = getPublicIp()

    ip, ip_changed = checkIpChange(ip=public_ip, old_ip=old_ip)

    if ip_changed:
        print(f"IP changed from {old_ip} to {ip}")
        with open("ip.txt", "w") as file:
            file.write(ip)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        for list_of_subdomains in subdomains.values():
            for subdomain in list_of_subdomains:
                url = f"https://api.cloudflare.com/client/v4/zones/{zone}/dns_records/{subdomain.get('id')}"
                res = requests.patch(url, headers=headers, json=subdomain)
                if res.status_code == 200:
                    print(
                        f"The IP for subdomain {subdomain.get('name')} was updated successfully."
                    )

    else:
        print(f"Public IP has not changed {ip}")


if __name__ == "__main__":
    main()
