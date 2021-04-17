from google.cloud import storage
import urllib.request, json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\\高振偉\\KaoFile\\畢業專題\\LifeWithFace-07fa08c0b57e.json"

client = storage.Client()

'''
bucket = client.get_bucket('lifewithface-33f15.appspot.com')
blob = bucket.blob('image')
blob.upload_from_filename('images.jpg')
'''
#print(blob._properties["updated"])

with urllib.request.urlopen("https://firebasestorage.googleapis.com/v0/b/lifewithface-33f15.appspot.com/o/model%2Fhhh.mp4") as url:
    data = json.loads(url.read().decode())
    global keytoken
    keytoken = data['downloadTokens']

urllib.request.urlretrieve("https://firebasestorage.googleapis.com/v0/b/lifewithface-33f15.appspot.com/o/model%2Fhhh.mp4?alt=media&token="+ keytoken, "fff.mp4")


#blob.download('images.jpg')

#downloadBlob = bucket.get_blob('images.jpg')
#downloadBlob.download_as_filename()