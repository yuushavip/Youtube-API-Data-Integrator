from googleapiclient.discovery import build
from utils import confighandler
import concurrent.futures

TASK_MAIN_KEY = 'channel_videos'

def fetch_video_details_data(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet,statistics,contentDetails'
        ).execute()
    
    if video_response['items']:
        video_details = video_response['items'][0]
        
        return video_details
    
    return None

def fetch_channel_videos_data(api_key, channel_id, params):
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(
        id=channel_id, 
        part='contentDetails'
        ).execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    channel_videos_data_items = []
    
    while True:
        batch_params = params.copy()
        batch_params['playlistId'] = playlist_id
        batch_params['part'] = 'snippet'
        batch_params['pageToken'] = next_page_token
        res = youtube.playlistItems().list(**batch_params).execute()
        channel_videos_data = res['items']
        merged_data_list = []
        
        for data_item in channel_videos_data:
            merged_data = data_item.copy()
            video_id = data_item['snippet']['resourceId']['videoId']
            video_data = fetch_video_details_data(api_key, video_id)
            merged_data.update(video_data)
            merged_data['playlistId'] = playlist_id
            merged_data['channelTitle'] = data_item['snippet']['channelTitle']
            
            merged_data_list.append(merged_data)
            
        channel_videos_data_items += merged_data_list
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break

    return channel_videos_data_items

def fetch_channel_videos_data_list():
    data_api_config = confighandler.get_data_api_config()
    channel_ids = confighandler.get_task_channel_ids(TASK_MAIN_KEY)
    params = confighandler.get_params(TASK_MAIN_KEY)
    videos_items = []

    if channel_ids:
        api_key = data_api_config['api_key']
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for channel_id in channel_ids:
                future = executor.submit(fetch_channel_videos_data, api_key, channel_id, params)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                videos_items.extend(future.result())

    return videos_items

def get_channel_videos_data_items():
    columns = confighandler.get_columns(TASK_MAIN_KEY)
    all_channel_videos_json = fetch_channel_videos_data_list()
    base_channel_videos_data = {key: None for key in columns}
    channel_videos_data_items = []

    for channel_videos_item in all_channel_videos_json:
        channel_videos_data = base_channel_videos_data.copy()
        
        for key in columns:
            if key.startswith("snippet_"):
                item_key = key.replace("snippet_", "")
                channel_videos_data[key] = channel_videos_item['snippet'].get(item_key, None)
                
            elif key.startswith("contentDetails_"):
                item_key = key.replace("contentDetails_", "")
                channel_videos_data[key] = channel_videos_item['contentDetails'].get(item_key, None)
                
            elif key.startswith("statistics_"):
                item_key = key.replace("statistics_", "")
                channel_videos_data[key] = channel_videos_item['statistics'].get(item_key, None)
                
            else:
                channel_videos_data[key] = channel_videos_item.get(key, None)
        
        channel_videos_data_items.append(channel_videos_data)
    
    return channel_videos_data_items