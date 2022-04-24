import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error

print('Loading function')

rekognition = boto3.client('rekognition')
mqttclient = boto3.client('iot-data')


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}},Attributes=['ALL'])
    return response

def process_response(response):
    print(response["FaceDetails"][0]["AgeRange"])
    print("hello")
    wanted_labels =["AgeRange","Smile","Eyeglasses","Sunglasses","Gender","Beard","Mustache","EyesOpen","Emotions"]
    
    toreturn = []
    for i in wanted_labels:
        toappend = ""
        if i == "AgeRange":
            aveage  = (response["FaceDetails"][0][i]["Low"] + response["FaceDetails"][0][i]["High"])/2
            if aveage < 12:
                toappend = "Child"
            elif aveage < 21:
                toappend = "Teenager"
            elif aveage < 50:
                toappend =  "Adult"
            else:
                toappend = "Elderly"
            toreturn.append(toappend)
        
        elif i == "Gender":
            toappend = response["FaceDetails"][0][i]["Value"]
            toreturn.append(toappend)
            
        elif i == "Emotions":
            for emotion in response["FaceDetails"][0][i]:
                if emotion["Confidence"] > 90.0:
                    toreturn.append(emotion["Type"].capitalize())
                    
        elif i =="Beard" or i=="Mustache":
            if response["FaceDetails"][0][i]["Confidence"]>7.0 :
                if response["FaceDetails"][0][i]["Value"]==True:
                    if "FacialHair" not in toreturn:
                        toreturn.append("FacialHair")
        
        else:
            if response["FaceDetails"][0][i]["Confidence"]>90.0 :
                if response["FaceDetails"][0][i]["Value"]==True:
                    toreturn.append(i)
                    
    if len(toreturn) ==0:
        toreturn.append("Default")
    return toreturn
        
        

# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        response = detect_faces(bucket, key)
        topub = process_response(response)
      
        print(topub)
        # Print response to console.
        #print(response)
        mqttclient.publish(topic='cciot-fastgame/viewerdemos',
            qos=1,
            payload=str(topub))

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
