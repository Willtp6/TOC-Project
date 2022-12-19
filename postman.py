import requests

url = "https://accounts.spotify.com/api/token"

payload='grant_type=refresh_token&refresh_token=AQBN54O4AESWkKps7tpkQ27S3laWd0_7-VGOQK6IXAqohTbiOXWGLcHklxhfAZVlkZlfRCSaC0wdKBsSrkbw9ov7FQleZOI-GPgAPIUNOpIvs35WUORIjQOcT-KRVzDFUh8'
headers = {
  'Authorization': 'Basic NWVjOGNiNWU4ZmM2NDk3YmE4M2FiNTg1MDYwMjMxMTA6MmY4YjJhZGMzNDZiNDc1YWI3ZWRmYjczNTkyN2M5NGY=',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__Host-device_id=AQAwPPZ7i6N2Keb8MEA-PRvaHk2wfwJLOZYj3ijWTYjsPJqJgIbLbIwhgKYQIUWLDg4yqsZwwF2GF9cxBoAMeulZHF-xbnNBP0A; sp_tr=false'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
