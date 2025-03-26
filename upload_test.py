import requests

# === Configuration ===
url = "http://127.0.0.1:5000/notes/upload"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0Mjk2MjczMCwianRpIjoiNTgxNTE1MjYtYTdkNi00NjY0LWFiMjQtNWNkMjY0YTkzYmJlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6IkluZHJheWFuaSIsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc0Mjk2MjczMCwiY3NyZiI6IjMzZGQxYmExLWE0OGEtNDI2Ni1iYjI2LTNhNGYyYTQ2NTQ1MiIsImV4cCI6MTc0Mjk2MzYzMH0.vT_bgpNlPQB_GjaoLZH9mv_QN8eucpCbSBXir-MHwYw"
file_path = "/Users/janyajaiswal/Desktop/Non_Tech_Resume_Janya_Jan2025.pdf"

# === Prepare Headers and File ===
headers = {
    "Authorization": f"Bearer {token}"
}

with open(file_path, "rb") as f:
    files = {
        "file": (file_path.split("/")[-1], f, "application/pdf")
    }

    # === Send POST Request ===
    response = requests.post(url, headers=headers, files=files)

# === Output ===
print("Status Code:", response.status_code)
print("Response:", response.json())
