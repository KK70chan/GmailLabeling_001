import requests

# Access Token 
access_token = "your access token"

# Common Header
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Google Sheets API
sheet_id = "your sheet id"
# Range of cells to get from Google Sheets
sheet_range = "Sheet1!A1:D190"
sheet_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_range}"

sheet_response = requests.get(sheet_url, headers=headers)
sheet_values = sheet_response.json().get('values', [])

# Debugging Info
print(f"HTTP Status Code: {sheet_response.status_code}")
print(f"HTTP Response: {sheet_response.json()}")
print(f"Google Sheet Count: {len(sheet_values)}")
# Check Data
for i, value in enumerate(sheet_values):
    print(f"{i+1}th value {value}")
print(f"Google Sheet Count: {len(sheet_values)}")


print("[STEP1] Googel Sheet Access has done")


# Gmail Label Creation Function
def create_label(name, parent_id=None):
    create_label_url = "https://www.googleapis.com/gmail/v1/users/me/labels"
    label_body = {'name': name}
    if parent_id:
        label_body['parentLabelIds'] = [parent_id]
    create_label_response = requests.post(create_label_url, headers=headers, json=label_body)
    return create_label_response.json()


# Gmail API
gmail_url = "https://www.googleapis.com/gmail/v1/users/me/labels"
gmail_response = requests.get(gmail_url, headers=headers)
gmail_labels = []
next_page_token = None
while True:
    params = {}
    if next_page_token:
        params['pageToken'] = next_page_token
    gmail_response = requests.get(gmail_url, headers=headers, params=params)
    gmail_data = gmail_response.json()
    gmail_labels.extend(gmail_data.get('labels', []))
    next_page_token = gmail_data.get('nextPageToken')
    if not next_page_token:
        break

# Debugging Info
print(f"HTTP Status Code: {gmail_response.status_code}")
print(f"HTTP Response Text: {gmail_response.text}")
try:
    gmail_data = gmail_response.json()
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON")
# Check Data
for i, label in enumerate(gmail_labels):
    print(f"{i+1}th Label => ID: {label['id']}, Name: {label['name'][:20]}")
print(f"Label Count: {len(gmail_labels)}")


print("[STEP2] Gmail Access has done")



# Process for Gmail label creation
for row in sheet_values:
    label_path = ""
    for label_name in row:
        if not label_name.strip():  # Pass empty string
            continue
        if label_path:
            label_path += f"/{label_name}"
        else:
            label_path = label_name

        existing_label = next((label for label in gmail_labels if label.get('name') == label_path), None)
        if existing_label is None:
            created_label = create_label(label_path)
            gmail_labels.append(created_label)
            print(f'Label created: {created_label}')



print("[STEP3] Gmail Label has created")