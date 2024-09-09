import requests

# Define the URL
url = "http://localhost:5000/"

# Create the form data
data = {
    'lecture_count': '2',
    'course_1': 'Mathematics',
    'teacher_1': 'John Doe',
    'duration_1': '2',
    'course_2': 'Physics',
    'teacher_2': 'Jane Doe',
    'duration_2': '3',
    'rooms': 'Room101,Room102',
    'time_slots': '5'
}

# Send POST request
response = requests.post(url, data=data)

# Check response for errors
if response.status_code != 200:
    # Get the last 500 characters of the response text
    error_snippet = response.text[-500:]
    print(f"ERROR: Status code {response.status_code}\nResponse snippet:\n{error_snippet}")
else:
    print("Request was successful!")
