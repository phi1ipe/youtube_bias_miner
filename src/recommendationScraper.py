import requests
from bs4 import BeautifulSoup
import json

class RecommendationScraper:
    """
    A class to scrape recommended videos from YouTube based on a given video ID.
    """
    def __init__(self):
        self.base_url = "https://www.youtube.com/watch?v="

    def fetch_html(self, video_id: str) -> str:
        """
        Fetches the HTML content of the YouTube video page.
        Args:
            video_id (str): The ID of the YouTube video.
        Returns:
            str: The HTML content of the video page.
        Raises:
            Exception: If the request to fetch the HTML fails.
        """
        url = f"{self.base_url}{video_id}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch video page, status code: {response.status_code}")

    def parse_recommended_videos(self, html: str) -> list:
        """
        Parses the HTML content to extract recommended videos.
        Args:
            html (str): The HTML content of the video page.
        Returns:
            list: A list of dictionaries containing recommended video information.
        Raises:
            Exception: If the parsing fails or the expected data structure changes.
        """
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        recommended_videos = []
        yt_initial_data = None
        for script in scripts:
            if "var ytInitialData =" in script.text:
                start = script.text.find("var ytInitialData =") + len("var ytInitialData =")
                end = script.text.rfind(";")
                yt_initial_data = script.text[start:end].strip()
                break

        if not yt_initial_data:
            raise Exception("Could not find the ytInitialData script in the page.")
        data = json.loads(yt_initial_data)

        try:
            items = data["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]
            for item in items:
                if "compactVideoRenderer" in item:
                    video_data = item["compactVideoRenderer"]
                    video_id = video_data.get("videoId")
                    title = video_data.get("title", {}).get("simpleText", "")
                    channel_info = video_data.get("longBylineText", {}).get("runs", [{}])[0]
                    channel_name = channel_info.get("text", "")
                    channel_id = channel_info.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId", "")
                    
                    recommended_videos.append({
                        "video_id": video_id,
                        "title": title,
                        "channel_name": channel_name,
                        "channel_id": channel_id
                    })
            return recommended_videos
        except KeyError:
            raise Exception("Failed to parse recommended videos. The structure might have changed.")

    def get_recommended_videos(self, video_id: str) -> list:
        """
        Gets the recommended videos for a given video ID.
        Args:
            video_id (str): The ID of the YouTube video.
        Returns:
            list: A list of dictionaries containing recommended video information.
        """
        html = self.fetch_html(video_id)
        recommended_videos = self.parse_recommended_videos(html)
        return recommended_videos
        

if __name__ == "__main__":
    example_video_id = "dQw4w9WgXcQ"  
    scraper = RecommendationScraper()
    try:
        fetched_recommended_videos = scraper.get_recommended_videos(example_video_id)
        for idx, video in enumerate(fetched_recommended_videos):
            print(f"{idx + 1}. {video['title']} by {video['channel_name']} (Channel ID: {video['channel_id']}) (Video ID: {video['video_id']})")
    except Exception as e:
        print(str(e))
