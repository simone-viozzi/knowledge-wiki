from collections import Counter

import bs4
import requests

COMMON_DOMAINS = ("https://bites-data.s3.us-east-2.amazonaws.com/"
                  "common-domains.html")
TARGET_DIV = {"class": "middle_info_noborder"}


def get_common_domains(url=COMMON_DOMAINS):
    """Scrape the url return the 100 most common domain names"""
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    trs = soup.find("div", TARGET_DIV).find_all('tr')
    return [tr.find_all("td")[2].text for tr in trs]


def get_most_common_domains(emails, common_domains=None):
    """Given a list of emails return the most common domain names,
       ignoring the list (or set) of common_domains"""
    if common_domains is None:
        common_domains = get_common_domains()

    # for multiple lookups a set is faster
    common_domains = set(common_domains)

    domains = Counter()
    for email in emails:
        name, domain = email.split('@')
        domain = domain.lower()
        if domain in common_domains:
            continue
        domains[domain] += 1

    return domains.most_common()
