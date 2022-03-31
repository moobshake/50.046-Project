import climage, os, sys
import boto3

adbucketname = 'iot-fastgame-proj-ads'
viewerbucketname = 'iot-fastgame-proj-viewers'

# Let's use Amazon S3
s3 = boto3.client("s3")
s3buckets = boto3.resource("s3")
adsbucket = s3buckets.Bucket(adbucketname)

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

def download_images(filter='all'):
    object_summary_iterator = adsbucket.objects.all()
    for i in object_summary_iterator:
        print(i.key)
        object = s3buckets.Object(adbucketname,i.key)
        try:
            objtopics = object.metadata['topics']
            objtopiclist = [x.strip() for x in objtopics.split(',')]
            print(objtopiclist)
            #if filter == 'all':

        except:
            pass

def display(image_name):
    image_folder = os.path.abspath("images")
    output = climage.convert(os.path.join(image_folder, image_name), is_unicode=True, is_256color=True)
    print(output)



display("mario.jpg")