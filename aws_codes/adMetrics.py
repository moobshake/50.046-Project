import json
import boto3

mqttclient = boto3.client('iot-data')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    topub = event['Records'][0]['s3']['object']['key']
    #print(topub)
    table = dynamodb.Table('viewerCount_byAds')
    table.put_item(
        Item = {
            'advertisement-name' : topub,
            'viewCount' : 0
        }
    )
    mqttclient.publish(topic='cciot-fastgame/aduploads',
            qos=1,
            payload=str(topub))
    return 
