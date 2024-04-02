from homeharvest import scrape_property
import pandas as pd
from datetime import datetime

# Load Florida ZIP codes
fl_zip_codes_df = pd.read_csv(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\flzips.csv')
all_properties = pd.DataFrame()

# Iterate over each ZIP code
for zip_code in fl_zip_codes_df['zip']:
    print(f"Processing ZIP code: {zip_code}")
    properties = scrape_property(
        location=str(zip_code),
        listing_type="for_rent",  # Change as needed
    )

    # Assuming 'scrape_property' returns a DataFrame with a column named 'listing_type'
    # that indicates whether the property is for rent or for sale, directly append to 'all_properties'
    all_properties = pd.concat([all_properties, properties], ignore_index=True)

# Generate filename based on current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"HomeHarvest_Florida_{current_timestamp}_forrent.csv"

# Export all properties to a single CSV file
all_properties.to_csv(filename, index=False)
print(f"Exported all for rent properties to {filename}")

for zip_code in fl_zip_codes_df['zip']:
    print(f"Processing ZIP code: {zip_code}")
    properties = scrape_property(
        location=str(zip_code),
        listing_type="for_sale",  # Change as needed
    )

    # Assuming 'scrape_property' returns a DataFrame with a column named 'listing_type'
    # that indicates whether the property is for rent or for sale, directly append to 'all_properties'
    all_properties = pd.concat([all_properties, properties], ignore_index=True)

# Generate filename based on current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"HomeHarvest_Florida_{current_timestamp}_forsale.csv"

# Export all properties to a single CSV file
all_properties.to_csv(filename, index=False)
print(f"Exported all for rent properties to {filename}")