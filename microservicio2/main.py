import io
import boto3
import json
import csv
from collections import defaultdict
#find song name and return lyrics
def get_info(song_name, csv_reader):
    for song in csv_reader:
        if song['name'] == song_name:
            release_date = song['release_date']
            duration_ms = song['duration_ms']
            arrayArtist = song['artists']
            info = {
                "release_date": release_date,
                "duration_ms": duration_ms,
                "artists": arrayArtist
            }
            return info
    return {
        "release_date": "",
        "duration_ms": "",
        "artists": "[]"
    }         
            


def lambda_handler(event, context):
    # TODO implement
    song_name = event['song_name']
    #read from s3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='lab3-spotify', Key='spotify-data.csv')
    csv_reader = csv.DictReader(io.StringIO(obj['Body'].read().decode('utf-8')))
    return {
        'statusCode': 200,
        'body': get_info(song_name, csv_reader)
    }

