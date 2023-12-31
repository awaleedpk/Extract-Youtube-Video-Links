# -*- coding: utf-8 -*-
"""Extract Youtube Video Links.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RnMiU0D1-US0A0oBmegIaK3ImtChfG3M
"""

import os
import csv
from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_links(channel_name):
    request = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id'
    )
    response = request.execute()
    channel_id = response['items'][0]['id']['channelId']

    video_links = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            channelId=channel_id,
            maxResults=50,
            order='date',
            type='video',
            part='id',
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_links

def save_to_csv(video_links, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for link in video_links:
            writer.writerow([link])

# Example usage
# Change YOUR_CHANNEL_NAME
channel_name = 'YOUR_CHANNEL_NAME'
video_links = get_video_links(channel_name)
save_to_csv(video_links, 'video_links.csv')