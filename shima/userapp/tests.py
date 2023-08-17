import requests
import json

# Assuming the Django server is running on http://localhost:8000

# Define the URL for the leave_applicationListCreateView
url = 'http://localhost:8000/user/leave-applications/'

# Define the data for the leave application
data = {
    'user': 1,  # Assuming the user ID is 1
    'start': '2023-07-20',
    'end': '2023-07-22',
    'reasone': 'Vacation',
    'is_approved': False
}

# Convert the data to JSON
json_data = json.dumps(data)

# Set the headers to specify the content type as JSON and include the JWT token
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NzU0ODUxLCJpYXQiOjE2ODk3NTM5NTEsImp0aSI6ImIyOTEzOThmNTMxNzQ5YThiYzg2Y2RlZGVhNjM2MzQwIiwidXNlcl9pZCI6Mjl9.3Nrr2ghfJ6UoVN5wOfsmBhHJS_O4EeBDVHANwMg2aok'
}

# Make the POST request
response = requests.get(url, data=json_data, headers=headers)

# Print the response status code and content
print(response.status_code)
print(response.content)