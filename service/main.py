#lambda function that calls the other two lambda functions

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('lambda')

    song_name = event['song_name']
    outputFormat = event['format']
    lyricsFlag = event['lyrics']
    
    #call microservice 1
    lyrics = ''
    if lyricsFlag != 'OFF':
        response1 = client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:118741195192:function:GetLyricsFunction',
            InvocationType='RequestResponse',
            Payload=json.dumps({'song_name': song_name})
        )
        lyrics = json.loads(response1['Payload'].read().decode("utf-8"))['body']

    #call microservice 2

    response2 = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:118741195192:function:GetSongInfo',
        InvocationType='RequestResponse',
        Payload=json.dumps({'song_name': song_name})
    )

    #parse response
    info = json.loads(response2['Payload'].read().decode("utf-8"))['body']

    result = {
        "lyrics": lyrics,
        "release_date": info['release_date'],
        "duration_ms": info['duration_ms'],
        "artists": info['artists']
    }

    if outputFormat == 'XML':
        result = '<lyrics>' + lyrics + '</lyrics>' + '<release_date>' + info['release_date'] + '</release_date>' + '<duration_ms>' + info['duration_ms'] + '</duration_ms>' + '<artists>' + info['artists'] + '</artists>'
    elif outputFormat == 'CSV':
        result = lyrics + ',' + info['release_date'] + ',' + info['duration_ms'] + ',' + info['artists']


    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }



