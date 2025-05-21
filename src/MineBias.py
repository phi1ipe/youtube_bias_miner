from youTubeApiRepository import YoutubeApiRepository
from recommendationScraper import RecommendationScraper
from biasRepository import BiasRepository
import datetime
import random
import time
import json
import os

class BiasMiner:
    """
    A class to mine YouTube videos and their recommendations for bias analysis.
    """
    def __init__(self):
        """
        Initializes the BiasMiner with instances of YoutubeApiRepository, RecommendationScraper, and BiasRepository.
        """
        self.youtube_api = YoutubeApiRepository()
        self.recommendation_scraper = RecommendationScraper()
        self.bias_repository = BiasRepository()

    def mine_channel_videos(self, channel_id: str, start_date=datetime.datetime.now() - datetime.timedelta(days=5), end_date=datetime.datetime.now()):
        """
        Mines the videos from a YouTube channel within a specified date range.
        Args:
            channel_id (str): The ID of the YouTube channel.
            start_date (datetime): The start date for the video mining.
            end_date (datetime): The end date for the video mining.
        Returns:
            list: A list of videos from the channel within the specified date range.
        """
        videos = self.youtube_api.get_channel_videos_in_timeframe(channel_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        return videos
    
    def mine_channel_recommendations(self, video_ids:list):
        """
        Mines the recommendations for a list of video IDs.
        Args:
            video_ids (list): A list of video IDs to fetch recommendations for.
        Returns:
            dict: A dictionary containing video IDs as keys and their respective recommendations as values.
        """
        recommendations = {}
        progress = 0
        total = len(video_ids)
        for video_id in video_ids:
            progress += 1
            if progress % 100 == 0:	
                print(f"Progress: {progress}/{total} videos processed", end="\r")
            try:
                recommendations[video_id] = self.recommendation_scraper.get_recommended_videos(video_id)
            except Exception as e1:
                try:
                    recommendations[video_id] = self.recommendation_scraper.get_recommended_videos(video_id)
                except Exception as e2:
                    print(f"Error fetching recommendations for video {video_id}: {e1} | {e2}")
            time.sleep(random.randint(1, 3))
        return recommendations
    

    def save_channel_bias_to_json(self, channel_id:str, bias_data:dict):
        """
        Saves the channel bias data to a JSON file.
        Args:
            channel_id (str): The ID of the channel.
            bias_data (dict): The bias data to save.
        """
        if not os.path.exists("channel_bias"):
            os.makedirs("channel_bias")
        with open(f"channel_bias/{channel_id}.json", "w", encoding="UTF-8") as f:
            json.dump(bias_data, f, indent=4)
    
    def load_channel_bias_from_json(self, channel_id:str) -> dict:
        """
        Loads the channel bias data from a JSON file.
        Args:
            channel_id (str): The ID of the channel.
        Returns:
            dict: The bias data loaded from the JSON file.
        """
        try:
            with open(f"channel_bias/{channel_id}.json", "r", encoding="UTF-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found for channel {channel_id}, returning empty data.")
            return {}
    
    def mine_videos(self, start_date=datetime.datetime.now() - datetime.timedelta(days=5), end_date=datetime.datetime.now()):
        channels = self.bias_repository.get_all_outlets()
        channel_videos = {}
        for channel_id in channels:
            try:
                print(f"Mining videos for channel: {self.bias_repository.get_outlet_name_by_id(channel_id)}")
                videos = self.mine_channel_videos(channel_id, start_date, end_date)
                print(f"Fetched {len(videos)} videos for channel: {self.bias_repository.get_outlet_name_by_id(channel_id)}")
                channel_videos[channel_id] = videos
            except Exception as e:
                print(f"Error fetching videos for channel {channel_id}: {e}")
                channel_videos[channel_id] = []
                continue
        return channel_videos
    
    def mine_recommendation_bias(self, channel_videos:dict):
        """
        Mines the recommendation bias for each channel's videos.
        Args:
            channel_videos (dict): A dictionary containing channel IDs and their respective videos.
        Returns:
            dict: A dictionary containing the recommendation bias for each channel.
        """
        recommendation_bias = {}
        for channel_id in channel_videos:
            # Check if recommendation bias already exists in JSON file
            bias_data = self.load_channel_bias_from_json(channel_id)	
            if bias_data:
                print(f"Recommendation bias already exists for channel: {self.bias_repository.get_outlet_name_by_id(channel_id)}")
                recommendation_bias[channel_id] = bias_data
                continue
            # If not, mine the recommendation bias  
            try:
                print(f"Mining recommendations for channel: {self.bias_repository.get_outlet_name_by_id(channel_id)}")
                recommendations = self.mine_channel_recommendations([video['snippet']['resourceId']['videoId'] for video in channel_videos[channel_id]])
                recommendation_bias[channel_id] = recommendations
                self.save_channel_bias_to_json(channel_id, recommendations)
            except Exception as e:
                print(f"Error fetching recommendations for channel {channel_id}: {e}")
                recommendation_bias[channel_id] = {}
                continue
        return recommendation_bias
    

if __name__ == "__main__":
    DAY_OFFSET = 100
    bias = BiasMiner()
    mine_start_date = datetime.datetime.now() - datetime.timedelta(days=DAY_OFFSET)
    mine_end_date = datetime.datetime.now()
    try:
        print("Try loading channel videos from JSON file...")
        with open("channel_videos.json", "r", encoding="UTF-8") as f:
            mined_channel_videos = json.load(f)
    except FileNotFoundError:
        print("File not found, mining channel videos...")
        mined_channel_videos = bias.mine_videos(mine_start_date, mine_end_date)
        print("Saving channel videos to JSON file...")
        with open("channel_videos.json", "w", encoding="UTF-8") as f:
            json.dump(mined_channel_videos, f, indent=4)
    print("Mining recommendation bias...")
    mined_recommendation_bias = bias.mine_recommendation_bias(mined_channel_videos)
    print("Saving recommendation bias to JSON file...")
    with open("recommendation_bias.json", "w", encoding="UTF-8") as f:
        json.dump(mined_recommendation_bias, f, indent=4)
