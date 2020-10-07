import boto3
import urllib3
import json
import os

http = urllib3.PoolManager()

ACCESS_TOKEN = None


def get_access_token():
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        kms = boto3.client('kms')
        encrypted = os.environ['ACCESS_TOKEN']
        key_id = os.environ['KMS_KEY_ID']
        res = kms.decrypt(
            KeyId=key_id, CiphertextBlob=bytes.fromhex(encrypted))
        ACCESS_TOKEN = res['Plaintext'].decode()

    return ACCESS_TOKEN


def lambda_handler(event, context):
    url = "https://hooks.slack.com/services/" + get_access_token()
    msg_obj = json.loads(event['Records'][0]['Sns']['Message'])
    message = 'CodeBuild triggered\n'
    message += 'Build number: {}\n'.format(
        msg_obj['detail']['additional-information']['build-number'])
    message += 'Phase: {}\n'.format(msg_obj['detail']['current-phase'])
    message += 'Status: {}\n'.format(msg_obj['detail']['build-status'])

    msg = {
        "channel": "#aws",
        "username": "Slack Bot",
        "text": message,
        "icon_emoji": ""
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print(resp)
