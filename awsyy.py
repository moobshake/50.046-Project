import boto3
import json

#to download, <bucket, obj name, file path to dl to>
# s3.download_file(
#     "iot-fastgame-proj-ads","beard.jpg","downloads/beard.jpg"
# )

#to upload <file path to upload from, bucket, obj name>
# s3.upload_file('images/pokemon.jpg','iot-fastgame-proj-ads','pokemon.jpg'
# )

#download_all_ads --> save img name and tags into a file, json?
#choose_ad --> check file, choose best match according to tags, display ad
#

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
                s3.download_file(adbucketname,i.key,downloadpath+i.key)
            elif filter in objtopiclist:
                s3.download_file(adbucketname,i.key,downloadpath+i.key)

            tofile={"name":i.key,"tags":objtopiclist}
            tosave.append(tofile)
        except:
            pass

    with open("tags.json", "w") as outfile:
        json.dump(tosave, outfile)
