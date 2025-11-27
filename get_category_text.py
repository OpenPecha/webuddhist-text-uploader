import csv

# Read and filter text_upload_log.csv
category_id = "dJpr4gMF72E4UpCnJ84sh"
text_type = "commentary"

results = []

with open('text_upload_log.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['category_id'] == category_id:
            results.append({
                'instance_id': row['instance_id']
            })

# Print results
print(f"Found {len(results)} matching records:")
print("-" * 80)

text_ids = [result['instance_id'] for result in results]
print(text_ids)

# Additional instance IDs to remove
additional_ids_to_remove = [
    'XyNfJSzMAHgD1tWV06reJ',
    'ZyCEGdklE9MkvUKxuPvtD',
    'XQrslJEpxtpWST06r80xq',
    'kpwuI1RlfJx2ZMXpVNwe9',
    'LTk08IwbyRwoPfVjtIeoH',
    'ZWBXiuyeeXXeeRNy25kHW',
    '1j2w41A1hi0cpbBn2otO2',
    'v9kZpKol6uZ2NBEprMSPP',
    'soliSjWusY4GsDErGU5yX',
    'QxTbJGUyBdCbcDCINCNms',
    '2BQMUAyxVgi8BuGdPa5k4',
    'ADDnRM1IbpnODLbkIYSCs',
    'oyaWUzbJHrhqrOJ97H3Bs',
    'IR4y9pazBzA0ukYUzLDsP',
    'WSasdEWD0XrUBqcBWeMch',
    'bcaMB1FOXpWhfMPtCiMjj',
    'zTFh2qw6du5ekDZ8xy9Rs',
    'WDWz01L08hrOZnd0Swdff',
    '1HXsu9wsTawAdQQDE9qyl',
    'VZ4abLAOLCqtIOTE6XfRP',
    'HOaHQicH9xuUIU4WkHTT3',
    '4RrlOnI5x8w0YUAS8w2a1',
    'NeNjiKgfJ1jWKODfmQ0xq',
    'vJLgYg0rKInLk89amlRpa',
    'JNtyFBIGpii12w9XImWt4',
    'YKO9npvgKzK1Q64mkn1Bf',
    'AXdRQIqxqy9lGTodwAlX5',
    'RYSSb1gHAxSOdJg4Bfjy9',
    'jlAtxFg1ENZIsPX3DE9uB'
]

# Combine both lists of IDs to remove
all_ids_to_remove = set(text_ids + additional_ids_to_remove)

# Read manifestation_status_log.csv and filter out instance_ids that are in text_ids
input_file = 'manifestation_status_log.csv'
output_file = 'manifestation_status_log.csv'

# Read all instance_ids from the manifestation_status_log.csv
with open(input_file, 'r', encoding='utf-8') as f:
    manifestation_ids = [line.strip() for line in f if line.strip()]

# Filter out instance_ids that are in all_ids_to_remove
filtered_ids = [instance_id for instance_id in manifestation_ids if instance_id not in all_ids_to_remove]

# Write the filtered results back to the file
with open(output_file, 'w', encoding='utf-8') as f:
    for instance_id in filtered_ids:
        f.write(f"{instance_id}\n")

print(f"\nRemoved {len(manifestation_ids) - len(filtered_ids)} instance_ids from {input_file}")
print(f"Remaining instance_ids: {len(filtered_ids)}")
