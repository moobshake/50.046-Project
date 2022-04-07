import boto3
import json
from datetime import datetime

#to download, <bucket, obj name, file path to dl to>
# s3.download_file(
#     "iot-fastgame-proj-ads","beard.jpg","downloads/beard.jpg"
# )

#to upload <file path to upload from, bucket, obj name>
# s3.upload_file('images/pokemon.jpg','iot-fastgame-proj-ads','pokemon.jpg')

#download_all_ads --> save img name and tags into a file, json?
#choose_ad --> check file, choose best match according to tags, display ad
#

def upload_images(viewerbucketname, imagepath, imagename):
    # Declare
    s3 = boto3.client("s3")
    s3buckets = boto3.resource("s3")
    adsbucket = s3buckets.Bucket(viewerbucketname)
    name = datetime.now().strftime("%H:%M:%S") + ".png"
    s3.upload_file(imagepath + imagename, viewerbucketname, name)

def download_images(adbucketname, download_path ,filter='all'):

    # Declare
    s3 = boto3.client("s3")
    s3buckets = boto3.resource("s3")
    adsbucket = s3buckets.Bucket(adbucketname)

    object_summary_iterator = adsbucket.objects.all()
    tosave=[]
    for i in object_summary_iterator: #iterate thru all objs
        print(i.key)
        object = s3buckets.Object(adbucketname,i.key)
        try:
            objtopics = object.metadata['topics']
            objtopiclist = [x.strip() for x in objtopics.split(',')]
            print(objtopiclist)
            #maybe can check if downloaded alr
            if filter == 'all':
                s3.download_file(adbucketname,i.key,download_path+i.key)
            elif filter in objtopiclist:
                s3.download_file(adbucketname,i.key,download_path+i.key)

            tofile={"name":i.key,"tags":objtopiclist}
            tosave.append(tofile)
        except:
            pass

    with open("tags.json", "w") as outfile:
        json.dump(tosave, outfile)


def download_image(adbucketname, download_path, img_name):
    s3 = boto3.client("s3")
    s3buckets = boto3.resource("s3")

    f = open("tags.json") 
    tosave = json.load(f)
    print(tosave)
    object = s3buckets.Object(adbucketname,img_name) # get the bucket :)
    try:
        objtopics = object.metadata['topics']
        objtopiclist = [x.strip() for x in objtopics.split(',')]
        tofile={"name":img_name,"tags":objtopiclist}
        if tofile not in tosave:
            print("Save file")
            tosave.append(tofile)
            s3.download_file(adbucketname,img_name,download_path+img_name)
    except:
            pass
    
    with open("tags.json", "w") as outfile:
        json.dump(tosave, outfile)
