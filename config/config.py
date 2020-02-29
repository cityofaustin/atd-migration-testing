DIR_GITHUB = "data/github"
DIR_ZENHUB = "data/zenhub"
DIR_LABELED = "data/labeled"
FAILDIR = "data/zenhub_errors"
LABEL_FILE = "migration_label_tracking.csv"
# DEST_REPO = "atd-data-tech"
DEST_REPO = "atd-migration-testing"
WORKSPACE_ID = "5caf7dc6ecad11531cc418ef" # DTS ZENHUB Workspace

SOURCE_REPOS = [
    # {"id": 183466621, "name": "atd-amanda"},
    # {"id": 117182832, "name": "atd-cctv-service"},
    # {"id": 136938110, "name": "atd-data-deploy"},
    {"id": 67241163, "name": "atd-data-publishing"},
    # {"id": 167410745, "name": "atd-data-service"},
    # {"id": 191611348, "name": "atd-data-utilities"},
    # {"id": 153001935, "name": "atd-dockless-api"},
    # {"id": 153001229, "name": "atd-dockless-dataviz"},
    # {"id": 160746380, "name": "atd-dockless-processing"},
    # {"id": 140850398, "name": "atd-finance-scraper"},
    {"id": 182321690, "name": "atd-geospatial"},
    # {"id": 181022917, "name": "atd-knack-data-tracker"},
    # {"id": 204069168, "name": "atd-knack-development-review"},
    # {"id": 187703251, "name": "atd-knack-dts-portal"},
    # {"id": 182864883, "name": "atd-knack-finance-purchasing"},
    # {"id": 187698234, "name": "atd-knack-forms"},
    # {"id": 191638408, "name": "atd-knack-signs-markings"},
    # {"id": 182868172, "name": "atd-knack-street-banner"},
    # {"id": 187706175, "name": "atd-knack-visitor-log"},
    # {"id": 149492871, "name": "atd-mobile-signals-work-orders"},
    # {"id": 185268238, "name": "atd-mobility-project-database"},
    # {"id": 138333607, "name": "atd-residential-parking-permits"},
    # {"id": 183474824, "name": "atd-service-bot"},
    # {"id": 178280308, "name": "atd-vz-data"},
]


REPO_MAP = {
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