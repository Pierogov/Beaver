import re
import csv
import requests
import time
import argparse
import os
from time import gmtime, strftime

# Get Info from ipinfo.io
def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        isp = data.get("org", "N/A")
        country = data.get("country", "N/A")
        return isp, country
    except Exception as e:
        return f"Error: {e}", "N/A", "N/A"

# Validate IP addresses
def is_private_ip(ip):
    try:
        parts = [int(x) for x in ip.split(".")]
        if len(parts) != 4:
            return False
        a, b = parts[0], parts[1]
        return (
            a == 10 or
            (a == 172 and 16 <= b <= 31) or
            (a == 192 and b == 168)
        )
    except ValueError:
        return False

def main():
    # Args
    parser = argparse.ArgumentParser(description="Simple tool created to simplify log analysis.")
    parser.add_argument("input_file", help="Path to the input log file.")
    parser.add_argument(
        "-s","--success",
        default="",
        metavar="<str>",
        help="If set, the program will only parse records with successfull login, searched by provided string."
    )
    parser.add_argument(
        "-d","--delay",
        type=float,
        default=0.5,
        metavar="<s>",
        help="Delay between requests to avoid API rate limits (default: 0.5s)"
    )
    parser.add_argument(
        "-f","--fast", 
        action="store_true",
        help="Skip unnecesary messages and banners made to look better"
    )
    parser.add_argument(
        "-p","--private", 
        action="store_true",
        help="Include private IPs in final file (idk why)"
    )
    args = parser.parse_args()

    # Banner
    show_banner = args.fast
    if(show_banner != True):
    
        print("__________                                 ")
        print("\\______   \\ ____ _____ ___  __ ___________ ")
        print("|    |  _// __ \\\\__  \\\\  \\/ // __ \\_  __ \\ ")
        print("|    |   \\  ___/ / __ \\\\   /\\  ___/|  | \\/ ")
        print("|______  /\\___  >____  /\\_/  \\___  >__|    ")
        print("        \\/     \\/     \\/          \\/       ")
        print("\n=================================================\nSimple tool created to simplify log analysis.")
        print("=================================================\nMade by bored SOC operator...\n=================================================\n")
        time.sleep(1)

    # Regex for IPv4 addresses
    ip_regex = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$')

    # Timestamp for unique filenames
    currentTime = strftime("%d_%m_%Y_%H_%M_%S", gmtime())

    # Files
    input_file = args.input_file
    ips_found_file = "output_ip_list_" + currentTime + ".txt"
    isp_file = "output_isp_" + currentTime + ".csv"

    # Unique IP set
    found_ips = set()

    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return
    else:
        print(f"Parsing file: '{input_file}', please wait for the IP regex to finish.")
    if(args.success!=""):
        success_regex = re.compile(args.success)
    
    # Find all IPs
    if(show_banner != True):
        max = sum(1 for _ in open(input_file))
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        if(show_banner != True):
            i = 1
        for row in reader:
            if(args.success==""):
                for cell in row:
                    ips = ip_regex.findall(cell)
                    found_ips.update(ips)

            else:
                successful = False
                for cell in row:
                    success = success_regex.findall(cell)
                    if(len(success)>=1):
                        successful = True
                if(successful==True):
                    for cell in row:
                        ips = ip_regex.findall(cell)
                        found_ips.update(ips)
            if(show_banner != True):
                print(f"[{i}/{max}] -> Searching for IPs in this row")
                i+=1

    # Write unique IPS to file
    with open(ips_found_file, "w+", encoding='utf-8') as f:
        for ip in sorted(found_ips):
            f.write(ip + "\n")

    # Results buffer
    results = []

    # Array with all IPs
    with open(ips_found_file, "r", encoding="utf-8") as f:
        ips = [line.strip() for line in f if line.strip()]

    print(f"\nFound {len(ips)} IP addresses, now checking ISP:")

    for idx, ip in enumerate(ips, start=1):
        if is_private_ip(ip):
    # If private skip and don't delay or save to file
            isp, country = "Private IP", "N/A"
            if(args.private):
                results.append((ip, isp, country))
            print(f"[{idx}/{len(ips)}] {ip} -> {isp}, {country}")
        else:
            isp, country = get_ip_info(ip)
            results.append((ip, isp, country))
            print(f"[{idx}/{len(ips)}] {ip} -> {isp}, {country}")
    # Respect for free API:)
            time.sleep(args.delay) 

    # Save results to final file
    with open(isp_file, "w+", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "ISP", "Country"])
        writer.writerows(results)

    print(f"\nResults saved in '{isp_file}'")

if __name__ == "__main__":
    main()