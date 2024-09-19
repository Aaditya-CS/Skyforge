import requests

url = "https://api.opendota.com/api/publicMatches?min_rank=80"

res = requests.get(url)

print(res.status_code)
print(res.content)

f = open("public.txt", "a")
f.write(str(res.content))
f.close()
