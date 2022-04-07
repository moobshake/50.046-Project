# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import awsyy

CONST_ADVERT_PATH = "./advertisements/"
CONST_AD_BUCKET_NAME = "iot-fastgame-proj-ads"

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "azwea5zu3qfbc-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "iot-fastgame-rpi"
PATH_TO_CERTIFICATE = "./certs/iot-fastgame-rpi.cert.pem"
PATH_TO_PRIVATE_KEY = "./certs/iot-fastgame-rpi.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./certs/root-CA.crt"
MESSAGE = "Hello World"
TOPIC = "iot-fastgame/aduploads"


# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
        )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    payload_string = payload.decode()[1:-1]
    awsyy.download_image(CONST_AD_BUCKET_NAME, CONST_ADVERT_PATH, payload_string)

# Subscribe
print("Subscribing to topic '{}'...".format(TOPIC))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received)

while True:
    # subscribe_result = subscribe_future.result()
    # print("Subscribed with {}".format(str(subscribe_result)))
    t.sleep(1)