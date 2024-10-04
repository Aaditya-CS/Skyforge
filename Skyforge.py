import requests

url = "https://api.opendota.com/api/publicMatches?min_rank=80"

i = 0

while i < 2000:
      res = requests.get(url)

      #print(res.status_code)
      #print(res.content)

      f = open("public.txt", "a")
      f.write(str(res.content))
      f.close()

      import json

      data = json.loads(res.content)
      print("Datatype after deserialization : "
            + str(type(data)))
      
      i+=1
      print("Count : ", i)

      print(len(data))

      L1 = list(data.values())
      print(L1)
