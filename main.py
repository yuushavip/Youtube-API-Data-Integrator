from models import youtube_channel_videos
from utils import csvhandler
import concurrent.futures

def main():
    all_fetch_functions = [
        (youtube_channel_videos.get_channel_videos_data_items, 'youtube_channel_videos.csv')
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        for func, file_name in all_fetch_functions:
            future = executor.submit(csvhandler.fetch_and_write, func, file_name)
            futures.append(future)
            
        for future in concurrent.futures.as_completed(futures):
            result = future.result()

if __name__ == "__main__":
    main()