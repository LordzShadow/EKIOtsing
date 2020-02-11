#!/usr/bin/python
import argparse
import sys
import time

from bs4 import BeautifulSoup
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description="Otsi infot EKI lehtedelt.")

parser.add_argument("-sv", help="Kasuta Sõnaveebi otsinguks(leiab ainult ühe tähenduse)", action='store_true')
parser.add_argument("-ekss", help="Kasuta EKSS otsinguks", action='store_true')
parser.add_argument("-os", help="Kasuta ÕS otsinguks(ei anna alati täpset vastust)", action='store_true')
parser.add_argument("-a", "--all", help="Otsi kõigist", action='store_true')
parser.add_argument("sõna", help="Sõna, mida otsid")

args = vars(parser.parse_args())
all = args["all"]
sv = args["sv"]
ekss = args["ekss"]
os = args["os"]
word = args["sõna"]

sv_url = f"https://sonaveeb.ee/search/est-est/simple/{word}/1"
os_url = f"https://www.eki.ee/dict/qs/index.cgi?Q={word}&F=M"
ekss_url = f"http://www.eki.ee/dict/ekss/index.cgi?Q={word}&F=M"
if not sv and not ekss and not os:
    sv = True

if all:
    sv = True
    os = True
    ekss = True

print("Alustame otsimist!\n")

if sv:
    # kasuta sonaveebi
    print("-- Otsin infot Sõnaveebist! --\n")
    html = requests.get(sv_url)
    html.encoding = 'utf-8'
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        print(bcolors.OKGREEN + soup.find_all(class_="homonym-intro")[0].get_text() + bcolors.ENDC)
        print()
    except IndexError:
        if not ekss and not os:
            print("Ei leidnud sõna tähendust! Otsin kuskilt mujalt?[y/n]", end=":")
            jes = True if input().upper() == "Y" else False
            print()
            if jes:
                ekss = True
                os = True
            else:
                print("\nVäljun programmist!")
                sys.exit()
        else:
            print("Ei leidnud sõna tähendust! Liigun edasi...\n")
time.sleep(1)
if ekss:
    # kasuta ekss
    print("-- Otsin infot Eesti Keelt Seletavast Sõnaraamatust! --\n")
    html = requests.get(ekss_url)
    html.encoding = 'utf-8'
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    tahendused = soup.find_all('span', class_='d')
    if len(tahendused) == 0:
        if os:
            print("Ei leidnud sõna tähendust! Liigun edasi...\n")
        else:
            print("Ei leidnud sõna tähendust! Otsin ÕS-ist?[y/n]", end=":")
            jes = True if input().upper() == "Y" else False
            print()
            if jes:
                os = True
            else:
                print("\nVäljun programmist!")
                sys.exit()
    for tahendus in tahendused:
        if tahendus.get_text() != "(üldisemalt)":
            print(bcolors.OKGREEN + tahendus.get_text().capitalize() + bcolors.ENDC + "\n")
            time.sleep(0.8)

time.sleep(1)
if os:
    print("-- Otsin infot Õigekeelsussõnaraamatust! --")
    print("(ei anna alati täpset vastust)\n")
    html = requests.get(os_url)
    html.encoding = 'utf-8'
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    tahendused = soup.find_all('span', class_='d')
    try:
        print(bcolors.OKGREEN + tahendused[0].get_text() + bcolors.ENDC + "\n")
    except IndexError:
        print("Ei leidnud sõna tähendust!")
time.sleep(1)
print("Väljun programmist!")