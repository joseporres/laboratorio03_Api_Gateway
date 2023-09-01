import io
import boto3
import json
import csv
from collections import defaultdict
#find song name and return lyrics
def get_lyrics(song_name, csv_reader):
    for song in csv_reader:
        if song['song'] == song_name:
            return song['text']
    
    return ""


def lambda_handler(event, context):
    # TODO implement
    song_name = event['song_name']
    #read from s3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='lab3-spotify', Key='spotify_millsongdata.csv')
    csv_reader = csv.DictReader(io.StringIO(obj['Body'].read().decode('utf-8')))
    return {
        'statusCode': 200,
        'body': get_lyrics(song_name, csv_reader)
    }

