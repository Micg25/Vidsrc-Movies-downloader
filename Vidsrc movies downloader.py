import requests
import re
from selenium import webdriver
from browsermobproxy import Server
import time
import json
import asyncio
import aiohttp

#setting selenium and browsermob-proxy
server = Server("...\\Browsermob\\bin\\browsermob-proxy") #add your own browsermob's bin path here
server.start()
proxy = server.create_proxy() 

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", str(proxy.proxy).split(':')[0])
profile.set_preference("network.proxy.http_port", int(str(proxy.proxy).split(':')[1]))
profile.set_preference("network.proxy.ssl", str(proxy.proxy).split(':')[0])
profile.set_preference("network.proxy.ssl_port", int(str(proxy.proxy).split(':')[1]))
profile.update_preferences()
options=webdriver.FirefoxOptions()
options.profile = profile


#setting the proxy in order to make it receive http/https traffic
proxy.new_har("LOG:", options={'captureHeaders': True, 'captureContent': True})

#getting to stream link
movieinput=input("Insert the movie name: ")


with open ("Movies_vidsrc.json", "r", encoding="utf-8") as file:
    moviesjson=json.load(file)

moviematch=[]
for movie in moviesjson:
    for result in movie["result"]:
        if movieinput in result["title"].lower():
            moviematch.append({"title":result["title"],"url":result["embed_url"]})


for n,movie in enumerate(moviematch):
    print(f"{n}. {movie}")

choice=int(input("Choose a movie: "))
url=moviematch[choice]["url"]
print(f"You chose:{moviematch[choice]["title"]}, {url} ")
#getting to stream link
browser = webdriver.Firefox(options=options)
browser.get(url) #insert the url of the movie you want to download
time.sleep(8)
result = proxy.har
browser.quit()
entries = result['log']['entries']

with open("resulthar.txt", "w", encoding="utf8") as file:
    file.write(json.dumps(result, indent=2))

pattern = r'https?://[^\s]+\.m3u8'

urls=[]
#finding best quality m3u8 url
for entry in entries:
    request = entry.get('request', {})
    urls.append(request.get('url'))  


match=[]
for url in urls:
    if(url!=""):
        if(re.search(pattern, url)):
            match.append(url)          
        
print(f"URL trovato: {match[-1]}")
url=match[-1]

resp=requests.get(url)
print(resp.status_code)

with open ("masterplaylist.m3u8","wb") as file:
    file.write(resp.content)

#finding chunks url
pattern = r'https?://[a-zA-Z0-9./_-]+\.html'
chunks=re.findall(pattern,str(resp.content))

with open ("chunks.txt","w") as file:
    for chunk in chunks:
        file.write(chunk+"\n")

async def download_chunk(n, url_, session):
    print(f"Downloading chunk {n}: {url_}")
    while True:
        try:
            # Downloading the chunks
            async with session.get(url_, timeout=30) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    if len(content) > 0:  
                        print(f"Downloaded chunk {n} (size: {len(content)} bytes)")
                        break
                else:
                    pass
        except Exception as e:
            print(f"Error downloading chunk {n}: {e}")
            print(resp.status)
            await asyncio.sleep(5)  # Waits 5 seconds if the previous request failed, and retries
    return (n, content)

async def main():
    batch_size = 35  
    delay = 5  

    async with aiohttp.ClientSession() as session:
        video_results = []

        for i in range(0, len(chunks), batch_size):
            
            batch = chunks[i:i+batch_size]
            video_tasks = [download_chunk(n, url_, session) for n, url_ in enumerate(batch, start=i)]  
            results = await asyncio.gather(*video_tasks)

            # Add results to main list
            video_results.extend(results)

            print(f"Waiting {delay} seconds before starting the next batch...")
            await asyncio.sleep(delay)
        
        # Sorting chunks
        video_results = sorted(video_results, key=lambda x: int(x[0]))
        
        # Saving .mp4 video
        with open("Movie.mp4", "wb") as merged_file:
            print("SAVING mp4 IN A FILE....")
            for n, content in video_results:
                merged_file.write(content)

asyncio.run(main())
