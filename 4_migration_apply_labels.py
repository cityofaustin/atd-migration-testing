import json

import requests

from config.secrets import GITHUB_USER, GITHUB_PASSWORD

"""
make sure all labels are created in the destination repo
"""

repo_map = {
    "atd-amanda" : "Product: AMANDA",
    "atd-geospatial" : "Service: Geo",
    "atd-knack-data-tracker" : "Product: AMD Data Tracker",
    "atd-knack-development-review" : "Product: Transportation Development Services",
    "atd-knack-dts-portal" : "Product: AMD Data Tracker",
    "atd-knack-finance-purchasing" : "Product: Finance & Inventory",
    "atd-knack-forms" : "Product: ATD Forms",
    "atd-knack-signs-markings" : "Product: Signs & Markings",
    "atd-knack-street-banner" : "Product: Banners",
    "atd-knack-visitor-log" : "Product: Visitor Log",
    "atd-mobile-signals-work-orders" : "Product: Mobile Signal Work Orders",
    "atd-mobility-project-database" : "Product: Mobility Project Database",
    "atd-residential-parking-permits" : "Product: Residential Parking Permit Digitization",
    "atd-vz-data" : "Product: Vision Zero Crash Data System",
    "atd-dockless-dataviz" : "Product: Dockless Dataviz",
    "atd-finance-scraper" : "Product: Finance & Inventory",
    "atd-data-and-performance" : "Product: Data & Performance Hub",
    "atd-dockless-processing" : "Product: Dockless Dataviz",
}

label_file = "migration_label_tracking.csv"

# DEST_REPO = "atd-data-tech"
DEST_REPO = "atd-migration-testing"

url = f"https://api.github.com/repos/cityofaustin/{DEST_REPO}/labels"

labels = []

last_url = None

while True:

    res = requests.get(url, params={"per_page":100}, auth=(GITHUB_USER, GITHUB_PASSWORD))
    
    res.raise_for_status()

    for label in res.json():
        label["repo"] = repo["name"]
        labels.append(label)

    if url == last_url:
        break

    try:
        links = requests.utils.parse_header_links(res.headers["Link"])
    except KeyError:
        # if there's only one page there will be no link headers
        break

    if links:
        for link in links:
            if link.get("rel") == "next":
                url = link.get("url")
                print(url)
            elif link.get("rel") == "last":
                last_url = link.get("url")