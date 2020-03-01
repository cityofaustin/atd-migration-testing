DIR = "data"
LABEL_FILE = "migration_label_tracking.csv"
DEST_REPO = "atd-monorepo-testing"
DEST_REPO_ID = 244223631 # atd-migration-testing
WORKSPACE_ID = "5caf7dc6ecad11531cc418ef" # DTS ZENHUB Workspace

SOURCE_REPOS = [
    # {"id" : 55646931, "name" : "atd-data-and-performance"},
    # {"id" : 67241163, "name" : "atd-data-publishing"},
    # {"id" : 136938110, "name" : "atd-data-deploy"},
    # {"id" : 138333607, "name" : "atd-residential-parking-permits"},
    # {"id" : 140626918, "name" : "atd-data-tech"},
    # {"id" : 140850398, "name" : "atd-finance-scraper"},
    # {"id" : 149492871, "name" : "atd-mobile-signals-work-orders"},
    # {"id" : 153001229, "name" : "atd-dockless-dataviz"},
    # {"id" : 153001935, "name" : "atd-dockless-api"},
    # {"id" : 160746380, "name" : "atd-dockless-processing"},
    # {"id" : 164503017, "name" : "lunch-near-atd-cameron"},
    # {"id" : 178280308, "name" : "atd-vz-data"},
    # {"id" : 181022917, "name" : "atd-knack-data-tracker"},
    {"id" : 182321690, "name" : "atd-geospatial"},
    # {"id" : 182864883, "name" : "atd-knack-finance-purchasing"},
    # {"id" : 182868172, "name" : "atd-knack-street-banner"},
    # {"id" : 183466621, "name" : "atd-amanda"},
    # {"id" : 185268238, "name" : "atd-mobility-project-database"},
    # {"id" : 187703251, "name" : "atd-knack-dts-portal"},
    # {"id" : 191638408, "name" : "atd-knack-signs-markings"},
    # {"id" : 197414350, "name" : "atd-gridsmart"},
    # {"id" : 209419491, "name" : "atd-micromobility-aggregation-privacy"},
    # {"id" : 213555617, "name" : "atd-airflow"},
    # {"id" : 232883213, "name" : "atd-mds"},
    # {"id" : 235453293, "name" : "atd-monorepo-migration"},
    # {"id" : 244223631, "name" : "atd-monorepo-testing"},
    
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
    "atd-micromobility-aggregation-privacy" : "Product: Dockless Dataviz",
}