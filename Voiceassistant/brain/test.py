import requests
import json

url = "https://www.aivinya.education/auth/confirmedemail/?key=SG7ByXehmJA-MdxvlDwp2&isInviteFlow=undefined&invite_key=undefined"

payload = json.dumps({
"text": "Hey how are you doing ?"
})
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)