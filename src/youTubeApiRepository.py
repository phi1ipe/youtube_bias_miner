from dotenv import load_dotenv
import googleapiclient.discovery
import os
import datetime

class YoutubeApiRepository:
    """
    A class to interact with the YouTube Data API v3.
    This class provides methods to fetch video and channel information, including
    subscriber counts, view counts, and video statistics.
    """
    def __init__(self):
        """
        Initializes the YoutubeApiRepository class and sets up the YouTube API client.
        It loads the API key from environment variables and creates a YouTube API client.
        """
        load_dotenv()
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.yt = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.api_key)
    
    def get_videos_by_channel_id(self, channel_id: str, maximum=1000) -> list:
        """
        Fetches the latest videos from a channel by its ID.
        Args:
            channel_id (str): The ID of the YouTube channel.
            maximum (int): The maximum number of videos to fetch.
        Returns:
            list: A list of dictionaries containing video information.
        """
        upload_playlist = self.get_channel_upload_playlist(channel_id)
        return self.get_new_videos_from_playlist(upload_playlist, maximum=maximum)[0:maximum]

    def is_channel_deleted(self, channel_id: str) -> bool:
        """
        Checks if a channel is deleted by its ID.
        Args:
            channel_id (str): The ID of the YouTube channel.
        Returns:
            bool: True if the channel is deleted, False otherwise.
        """
        result = self.yt.channels().list(part="snippet", id=channel_id).execute()
        if result['pageInfo']['totalResults'] == 0:
            return True
        return False
    
    def get_country_code_by_channel_ids(self, channel_ids: list) -> dict:
        """
        Fetches the country codes for a list of channel IDs.
        Args:
            channel_ids (list): A list of YouTube channel IDs.
        Returns:
            dict: A dictionary mapping channel IDs to their country codes.
        """
        result = self.yt.channels().list(part="snippet", id=channel_ids).execute()
        country_codes = {}
        for item in result['items']:
            if 'country' in item['snippet']:
                country_codes[item['id']] = item['snippet']['country']
            else:
                country_codes[item['id']] = None
        return country_codes
    
    def get_number_of_subscribers_by_channel_ids(self, channel_ids: list) -> dict:
        """
        Fetches the number of subscribers for a list of channel IDs.
        Args:
            channel_ids (list): A list of YouTube channel IDs.
        Returns:
            dict: A dictionary mapping channel IDs to their subscriber counts.
        """
        result = self.yt.channels().list(part="statistics", id=channel_ids).execute()
        subscribers = {}
        for item in result['items']:
            if 'subscriberCount' in item['statistics']:
                subscribers[item['id']] = item['statistics']['subscriberCount']
            else:
                subscribers[item['id']] = None
        return subscribers
    
    def get_number_of_video_views_by_video_ids(self, video_ids: list) -> dict:
        """
        Fetches the number of views for a list of video IDs.
        Args:
            video_ids (list): A list of YouTube video IDs.
        Returns:
            dict: A dictionary mapping video IDs to their view counts.
        """
        result = self.yt.videos().list(part="statistics", id=video_ids).execute()
        views = {}
        for item in result['items']:
            if 'viewCount' in item['statistics']:
                views[item['id']] = item['statistics']['viewCount']
            else:
                views[item['id']] = None
        return views
    
    def get_number_of_likes_and_comments_by_video_ids(self, video_ids: list) -> dict:
        """
        Fetches the number of likes and comments for a list of video IDs.
        Args:
            video_ids (list): A list of YouTube video IDs.
        Returns:
            dict: A dictionary mapping video IDs to their like and comment counts.
        """
        result = self.yt.videos().list(part="statistics", id=video_ids).execute()
        likes_and_comments = {}
        for item in result['items']:
            if 'id' in item and 'statistics' in item and 'likeCount' in item['statistics'] and 'commentCount' in item['statistics']:
                likes_and_comments[item['id']] = {
                    'likes': item['statistics']['likeCount'],
                    'comments': item['statistics']['commentCount']
                }
        return likes_and_comments

    def get_channel_upload_playlist(self, channel_id: str) -> str:
        """
        Fetches the upload playlist ID for a channel by its ID.
        Args:
            channel_id (str): The ID of the YouTube channel.
        Returns:
            str: The ID of the upload playlist.
        """
        return self.yt.channels().list(part="contentDetails", id=channel_id).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def get_new_videos_from_playlist(self, playlist_id: str, maximum=10000) -> list:
        """
        Fetches the latest videos from a playlist by its ID.
        Args:
            playlist_id (str): The ID of the YouTube playlist.
            maximum (int): The maximum number of videos to fetch.
        Returns:
            list: A list of dictionaries containing video information.
        """
        next_page_token = None
        i = 0
        videos = []
        while True:
            response = self.get_videos_from_playlist(playlist_id, next_page_token)
            for item in response['items']:
                i += 1
                videos.append(item)
            if response.keys().__contains__('nextPageToken'):
                next_page_token = response['nextPageToken']
            else:
                break
            if i >= maximum:
                print("Failsafe: Stopped at " + str(i) + " videos")
                break
        return videos
    
    def get_channel_videos_in_timeframe(self, channel_id: str, start_date="2024-01-01", end_date="2024-12-31") -> list:
        """
        Fetches videos from a channel within a specified timeframe.
        Args:
            channel_id (str): The ID of the YouTube channel.
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.
        Returns:
            list: A list of dictionaries containing video information.
        """
        upload_playlist = self.get_channel_upload_playlist(channel_id)
        return self.get_videos_in_timeframe(upload_playlist, start_date, end_date)
    
    def get_channel_information_by_id(self, channel_id: str) -> dict:
        """
        Fetches information about a channel by its ID.
        Args:
            channel_id (str): The ID of the YouTube channel.
        Returns:
            dict: A dictionary containing channel information.
        """
        return self.yt.channels().list(part="snippet, statistics", id=channel_id).execute()['items'][0]
    
    def get_videos_in_timeframe(self, playlist_id: str, start_date="2024-01-01", end_date="2024-12-31") -> list:
        """
        Fetches videos from a playlist within a specified timeframe.
        Args:
            playlist_id (str): The ID of the YouTube playlist.
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.
        Returns:
            list: A list of dictionaries containing video information.
        """
        next_page_token = None
        i = 0
        videos = []

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)


        while True:
            response = self.get_videos_from_playlist(playlist_id, next_page_token)
            if i > 10000:
                print("Failsafe: Stopped at " + str(i) + " videos")
                break
            for item in response['items']:
                i += 1
                published_at = datetime.datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                if published_at < start_date:
                    return videos
                if published_at < end_date:
                    videos.append(item)
            if response.keys().__contains__('nextPageToken'):
                next_page_token = response['nextPageToken']
            else:
                break
        return videos
    
    def get_videos_from_playlist(self, playlist_id: str, token=None):
        """
        Fetches videos from a playlist by its ID.
        Args:
            playlist_id (str): The ID of the YouTube playlist.
            token (str): The page token for pagination.
        Returns:
            dict: A dictionary containing video information.
        """
        if token is None:
            result = self.yt.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50).execute()
        else:
            result = self.yt.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50, pageToken=token).execute()
        return result
    
    def get_last_50_videos_from_channel(self, channel_id):
        """
        Fetches the last 50 videos from a channel by its ID.
        Args:
            channel_id (str): The ID of the YouTube channel.
        Returns:
            list: A list of dictionaries containing video information.
        """
        upload_playlist = self.get_channel_upload_playlist(channel_id)
        return self.get_new_videos_from_playlist(upload_playlist, 50)[0:50]

if __name__ == '__main__':
    example_channel = "UCupvZG-5ko_eiXAupbDfxWw"
    yt = YoutubeApiRepository()
    videos = yt.get_channel_videos_in_timeframe(example_channel, "2025-03-10", "2025-03-13")
    for video in videos:
       print(video['snippet']['title'], " - ", video['snippet']['publishedAt'])
    print("Fetched " + str(len(videos)) + " videos")    
    example_video_ids = ['9bZkp7q19f0', 'dQw4w9WgXcQ']
    print(yt.get_number_of_likes_and_comments_by_video_ids(example_video_ids))

