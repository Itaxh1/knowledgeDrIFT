import json
import urllib.request

def scraping(s):
    urlData = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyBpQAYG2qdzDsq3WJwmBkD_4L46rkDkvQ4&textFormat=plainText&part=snippet,replies&topLevelComment&maxResults=100&videoId={}".format(s)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    decode_data=json.loads(data.decode(encoding))
    return decode_data
