import requests
import re
import time
import os
import hashlib
import exifread
from PIL import Image
from termcolor import colored
import sys
from colorama import Fore, init
sys.stderr = open(os.devnull, 'w')
import concurrent.futures
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from geopy.geocoders import Nominatim
import exifread

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def askRetry(callback_func):
    try:
        print()
        lanjut = str(input("[" + colored("~", "green") + "] 🤖 Do you want to continue? [y/N]:"))
        if lanjut == "y" or lanjut == "Y":
            print()
            callback_func()
        elif lanjut == "n" or lanjut == "N":
            main()
        else : 
            print("🤖 Sorry, I didn't understand that. Just 'y' or 'n', please.")
    except ValueError:
        print(colored("[ERROR]", "red") + " Input rejected: expected a string, received a number instead.")
        time.sleep(2)
        main()
    except KeyboardInterrupt:
        print("\n\n🤖 Shutdown signal received. See you next time!")
        time.sleep(2)
        quit()

def topTitle():
    sub = Fore.RESET + "V1.0"
    print(Fore.GREEN + rf"""
     _    __      _     _______
    | |  / /___  (_)___/ / ___/_________ _____
    | | / / __ \/ / __  /\__ \/ ___/ __ `/ __ \
    | |/ / /_/ / / /_/ /___/ / /__/ /_/ / / / /
    |___/\____/_/\____//____/\___/\__,_/_/ /_/  {sub}""")
    print()
    print("[" + colored(" VoidScan ", "green") + "] Made By " + colored("SURYOX", "green"))
    print()
    print("[" + colored(" github.com/suryox666 ", "green") + "] | [ " + colored("saweria.co/suryos", "green") + " ] | [ " + colored("trakteer.id/suryos", "green") + " ]")
    print()

def username_search():
    clear()
    topTitle()

    username = input("[" + colored("~", "green") + "]" + " Username : ")
    print("")

    sites = {
        "GitHub": ("https://github.com/{}", ["not found"]),
        "Reddit": ("https://www.reddit.com/user/{}", ["nobody on reddit"]),
        "Instagram": ("https://www.instagram.com/{}", ["page isn't available"]),
        "Telegram" : ("https://t.me/{}", ["If you have Telegram, you can contact"]),
        "TikTok": ("https://www.tiktok.com/@{}", ["couldn't find this account"]),
        "Pinterest": ("https://www.pinterest.com/{}", ["sorry", "not found"]),
        "Twitch": ("https://www.twitch.tv/{}", ["sorry"]),
        "Steam": ("https://steamcommunity.com/id/{}", ["error", "not found"]),
        "SoundCloud": ("https://soundcloud.com/{}", ["404"]),
        "Medium": ("https://medium.com/@{}", ["not found"]),
        "Keybase": ("https://keybase.io/{}", ["not found"]),
        "Threads" : ("https://www.threads.net/{}", ["Login"]),
        "Facebook" : ("https://www.facebook.com/{}", ["This content isn't available right now"]),
        "X" : ("https://x.com/{}", ["This account doesn’t exist"]),
        "YouTube" : ("https://www.youtube.com/@{}", ["404 Not Found"]),
        "LinkedIn" : ("https://www.linkedin.com/in/{}", ["Login"]),
        "Snapchat" : ("https://www.snapchat.com/@{}", ["sorry"])
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    found = []

    def check(site):
        name, (template, errors) = site
        url = template.format(username)

        try:
            r = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
            text = r.text.lower()

            if any(err in text for err in errors):
                print("[" + colored("x", "red") + "] " + colored(f"{name}", "red") + " : " + colored("NOT FOUND", "red"))
                return

            if username.lower() not in r.url.lower():
                print("[" + colored("x", "red") + "] " + colored(f"{name}", "red") + " : " + colored("NOT FOUND", "red"))
                return

            if r.status_code == 200:
                print("[" + colored("✓", "green") + "] " + colored(f"{name}", "green") + " : " + colored(f"{url}", "green"))
                found.append(url)

        except:
            print("[" + colored("x", "red") + "] " + colored(f"{name}", "red") + " : " + colored("ERROR", "red"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        ex.map(check, sites.items())

    print("\n[" + colored("+", "green") + "]" + " Accounts found :", colored(len(found), "green"))

    if found:
        folder = "reports/username_search"
        os.makedirs(folder, exist_ok=True)
        file = os.path.join(folder, f"voidscan_username_search_{username}.txt")
        open(file, "w", encoding="utf-8").write("\n".join(found))
        print("[" + colored("+", "green") + "]" + " Saved to :", colored(file, "green"))

    askRetry(username_search)

def whois_query(domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(("whois.verisign-grs.com", 43))
    s.send((domain + "\r\n").encode())
    
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
    
    s.close()
    return response.decode(errors="ignore")


def extract(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else "N/A"

def domain_lookup():
    clear()
    topTitle()

    raw = input("[" + colored("~", "green") + "] Domain : ").strip()
    print("")

    if not raw:
        print("Domain kosong")
        askRetry(domain_lookup)
        return

    domain = raw.lower()
    domain = domain.replace("http://", "")
    domain = domain.replace("https://", "")
    domain = domain.replace("www.", "")
    domain = domain.split("/")[0].strip()

    try:
        ip = socket.gethostbyname(domain)
        print("[" + colored("+", "green") + "] Domain : " + colored(f"{domain}", "green"))
        print("[" + colored("+", "green") + "] IP Address : " + colored(f"{ip}", "green"))

        try:
            rdns = socket.gethostbyaddr(ip)[0]
            print("[" + colored("+", "green") + "] Reverse DNS : " + colored(f"{rdns}\n", "green"))
        except:
            print("[" + colored("+", "green") + "] Reverse DNS : " + colored("N/A", "red"))

    except:
        print("[" + colored("+", "red") + "] Cannot resolve IP")
        askRetry(domain_lookup)
        return

    whois = whois_query(domain)

    if "No match for" in whois:
        print("[" + colored("+", "red") + "] Domain not found in registry")
        askRetry(domain_lookup)
        return

    print("\n[" + colored("+", "green") + "] Domain Information")

    print("[" + colored("~", "green") + "] Registered On : " + colored(f"{extract(r'Creation Date:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + "] Expires On : " + colored(f"{extract(r'Registry Expiry Date:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + "] Updated On : " + colored(f"{extract(r'Updated Date:\s*(.*)', whois)}", "green"))

    print("[" + colored("~", "green") + "] Status :")
    status = re.findall(r'Domain Status:\s*(.*)', whois)
    print(colored("\n".join(status), "green") if status else colored("N/A", "red"))

    print("[" + colored("~", "green") + "] Name Servers :")
    ns = re.findall(r'Name Server:\s*(.*)', whois)
    print(colored("\n".join(ns), "green") if ns else colored("N/A", "red"))
    print()

    print("[" + colored("+", "green") + "] Registrar Information")

    print("[" + colored("~", "green") + f"] Registrar : " + colored(f"{extract(r'Registrar:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] IANA ID : " + colored(f"{extract(r'Registrar IANA ID:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] Email : " + colored(f"{extract(r'Registrar Abuse Contact Email:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] Abuse Email : " + colored(f"{extract(r'Registrar Abuse Contact Email:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] Abuse Phone : " + colored(f"{extract(r'Registrar Abuse Contact Phone:\s*(.*)', whois)}", "green"))
    print()

    print("[" + colored("+", "green") + "] Registrant Contact")

    print("[" + colored("~", "green") + f"] Organization : " + colored(f"{extract(r'Registrant Organization:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] Country : " + colored(f"{extract(r'Registrant Country:\s*(.*)', whois)}", "green"))
    print("[" + colored("~", "green") + f"] Email : " + colored(f"{extract(r'Registrant Email:\s*(.*)', whois)}", "green"))
    print()

    print("[" + colored("+", "green") + "] Technical Contact")

    print("[" + colored("~", "green") + f"] Email : " + colored(f"{extract(r'Tech Email:\s*(.*)', whois)}", "green"))
    print()

    askRetry(domain_lookup)

def wa_check(e164):
    try:
        r = requests.get(
            f"https://wa.me/{e164.replace('+','')}",
            timeout=10,
            allow_redirects=True
        )
        return "LIKELY ACTIVE" if "whatsapp.com" in r.url else "UNKNOWN"
    except:
        return "UNKNOWN"

def tg_check(e164):
    try:
        r = requests.get(f"https://t.me/+{e164.replace('+','')}", timeout=10)
        return "POSSIBLE" if r.status_code == 200 else "UNKNOWN"
    except:
        return "UNKNOWN"

def operator_id(prefix):
    mapping = {
        "0811": "Telkomsel",
        "0812": "Telkomsel",
        "0813": "Telkomsel",
        "0821": "Telkomsel",
        "0852": "Telkomsel",
        "0853": "Telkomsel",
        "0817": "XL",
        "0818": "XL",
        "0819": "XL",
        "0859": "XL",
        "0814": "Indosat",
        "0815": "Indosat",
        "0816": "Indosat",
        "0855": "Indosat",
        "0856": "Indosat",
        "0857": "Indosat",
        "0858": "Indosat",
        "0895": "Tri",
        "0896": "Tri",
        "0897": "Tri",
        "0898": "Tri",
        "0899": "Tri",
        "0881": "Smartfren",
        "0882": "Smartfren",
        "0887": "Smartfren",
        "0888": "Smartfren"
    }
    return mapping.get(prefix, "Unknown")

def phone_lookup():
    clear()
    topTitle()

    raw = input("[" + colored("~", "green") + "] Phone Number : ").strip()

    if raw.startswith("08"):
        prefix = raw[:4]
        raw = "+62" + raw[1:]
    else:
        prefix = ""

    try:
        num = phonenumbers.parse(raw)

        valid = phonenumbers.is_valid_number(num)
        possible = phonenumbers.is_possible_number(num)

        country = geocoder.description_for_number(num, "en")
        operator = carrier.name_for_number(num, "en")
        tz = ", ".join(timezone.time_zones_for_number(num))

        e164 = phonenumbers.format_number(
            num, phonenumbers.PhoneNumberFormat.E164
        )
        intl = phonenumbers.format_number(
            num, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        if operator == "" and prefix:
            operator = operator_id(prefix)

        num_type = phonenumbers.number_type(num)
        line_type = "VoIP" if num_type == 6 else "Mobile"

        print("")

        wa_status = wa_check(e164)
        tg_status = tg_check(e164)

        score = 0
        if valid: score += 40
        if possible: score += 20
        if line_type != "VoIP": score += 20
        if operator != "Unknown": score += 10
        if wa_status == "LIKELY ACTIVE": score += 5
        if tg_status == "POSSIBLE": score += 5

        if score >= 80:
            verdict = colored("VERY LIKELY ACTIVE", "green")
        elif score >= 60:
            verdict = colored("LIKELY ACTIVE", "yellow")
        elif score >= 40:
            verdict = colored("UNCERTAIN", "orange")
        else:
            verdict = colored("LOW PROBABILITY ACTIVE", "red")

        print("[" + colored("+", "green") + "] Number :", colored(intl, "green"))

        print("\n[" + colored("+", "green") + "] Intelligence")
        print("[" + colored("~", "green") + "] Country :", colored(country, "green"))
        print("[" + colored("~", "green") + "] Operator :", colored(operator, "green"))
        print("[" + colored("~", "green") + "] Timezone :", colored(tz, "green"))
        print("[" + colored("~", "green") + "] Line Type :", colored(line_type, "green"))
        print("[" + colored("~", "green") + "] Valid :", colored(valid, "green"))
        print("[" + colored("~", "green") + "] Possible :", colored(possible, "green"))

        print("\n[" + colored("+", "green") + "] Messaging Footprint")
        print("[" + colored("~", "green") + "] WhatsApp :", colored(wa_status, "green"))
        print("[" + colored("~", "green") + "] Telegram :", colored(tg_status, "green"))

        print("\n[" + colored("+", "green") + "] Activity Assessment")
        print("[" + colored("~", "green") + "] Score :", score, "/ 100")
        print("[" + colored("~", "green") + "] Verdict :", colored(verdict, "green"))

        print("\n⚠️ Note: 100% confirmation requires telecom access")

    except:
        print("[" + colored("+", "red") + colored("Invalid number", "red"))

    askRetry(phone_lookup)

def image_osint():
    clear()
    topTitle()

    path = input("[" + colored("~", "green") + "] Image path : ").strip()
    print("")

    if not os.path.exists(path):
        print("[" + colored("+", "red") + "] File not found")
        askRetry(image_osint)
        return

    # 📁 File info
    size = os.path.getsize(path)
    file_name = os.path.splitext(os.path.basename(path))[0]

    print("[" + colored("+", "green") + "] File Information")
    print("[" + colored("~", "green") + "] File :", colored(file_name, "green"))
    print("[" + colored("~", "green") + "] Size :", colored(f"{size/1024:.2f} KB", "green"))

    # 🔐 Hash
    with open(path, "rb") as f:
        data = f.read()

    md5 = hashlib.md5(data).hexdigest()
    sha1 = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()

    print("\n[" + colored("+", "green") + "] Hash Fingerprint")
    print("[" + colored("~", "green") + "] MD5 :", colored(md5, "green"))
    print("[" + colored("~", "green") + "] SHA1 :", colored(sha1, "green"))
    print("[" + colored("~", "green") + "] SHA256 :", colored(sha256, "green"))

    # 🖼️ Image properties
    img = Image.open(path)

    print("\n[" + colored("+", "green") + "] Image Properties")
    print("[" + colored("~", "green") + "] Format :", colored(img.format, "green"))
    print("[" + colored("~", "green") + "] Resolution :", colored(f"{img.width} x {img.height}", "green"))
    print("[" + colored("~", "green") + "] Mode :", colored(img.mode, "green"))

    # 📷 EXIF
    print("\n[" + colored("+", "green") + "] EXIF Metadata")

    with open(path, "rb") as f:
        tags = exifread.process_file(f)

    exif_data = []

    if not tags:
        print("[" + colored("+", "red") + "] No EXIF data found")
    else:
        for tag in tags:
            if "GPS" not in tag:
                value = str(tags[tag])
                print("[" + colored("~", "green") + f"] {tag} :", colored(value, "green"))
                exif_data.append(f"{tag}: {value}")

    # 📍 GPS extraction
    gps_tags = {t: tags[t] for t in tags if "GPS" in t}

    lat = lon = None

    if gps_tags:
        print("\n[" + colored("+", "green") + "] GPS Location Found")

        def convert(value):
            d = float(value.values[0])
            m = float(value.values[1])
            s = float(value.values[2])
            return d + (m / 60.0) + (s / 3600.0)

        try:
            lat = convert(gps_tags["GPS GPSLatitude"])
            lon = convert(gps_tags["GPS GPSLongitude"])

            print("[" + colored("~", "green") + "] Latitude :", colored(lat, "green"))
            print("[" + colored("~", "green") + "] Longitude :", colored(lon, "green"))
            print("[" + colored("~", "green") + "] Google Maps :", colored(f"https://maps.google.com/?q={lat},{lon}", "green"))
        except:
            print("[" + colored("+", "red") + "] GPS parse error")
    else:
        print("\n[" + colored("+", "red") + "] GPS : Not found")

    # 🔍 Reverse search links
    print("\n[" + colored("+", "green") + "] Reverse Image Search")
    print("[" + colored("~", "green") + "] Google Lens :", colored("https://lens.google.com/", "green"))
    print("[" + colored("~", "green") + "] Yandex Images :", colored("https://yandex.com/images/", "green"))
    print("[" + colored("~", "green") + "] Bing Visual :", colored("https://www.bing.com/visualsearch", "green"))

    # 💾 Save report
    folder = "reports/image_osint"
    os.makedirs(folder, exist_ok=True)

    file = os.path.join(folder, f"voidscan_image_osint_{file_name}.txt")

    with open(file, "w", encoding="utf-8") as f:
        f.write(f"File: {path}\n")
        f.write(f"Size: {size} bytes\n\n")

        f.write("=== HASH ===\n")
        f.write(f"MD5: {md5}\n")
        f.write(f"SHA1: {sha1}\n")
        f.write(f"SHA256: {sha256}\n\n")

        f.write("=== IMAGE ===\n")
        f.write(f"Format: {img.format}\n")
        f.write(f"Resolution: {img.width}x{img.height}\n")
        f.write(f"Mode: {img.mode}\n\n")

        f.write("=== EXIF ===\n")
        if exif_data:
            f.write("\n".join(exif_data))
        else:
            f.write("No EXIF data\n")

        if lat and lon:
            f.write(f"\n\nGPS: {lat}, {lon}")
            f.write(f"\nMaps: https://maps.google.com/?q={lat},{lon}")

    print("\n[" + colored("+", "green") + "] Saved to :", colored(file, "green"))

    askRetry(image_osint)

def main():
    while True :
        clear()
        topTitle()
        print("[" + colored("+", "green") + "]" + " 1. Username Search")
        print("[" + colored("+", "green") + "]" + " 2. Domain Intelligence")
        print("[" + colored("+", "green") + "]" + " 3. Phone Lookup" + colored(" -> BETA", "green"))
        print("[" + colored("+", "green") + "]" + " 4. Image OSINT")
        print("[" + colored("+", "green") + "]" + " 5. Exit\n")
        try:
            choose = int(input(("[" + colored("~", "green") + "] : ")))
        except ValueError:
            print()
            print("[" + colored("ERROR", "red") + "] System rejected your input. Only numbers are allowed! 🔒")
            time.sleep(3)
            main()
        print("")
        if choose == 1: username_search()
        elif choose == 2: domain_lookup()
        elif choose == 3: phone_lookup()
        elif choose == 4: image_osint()
        elif choose == 5: exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🤖 Shutdown signal received. See you next time!")
        time.sleep(2)
