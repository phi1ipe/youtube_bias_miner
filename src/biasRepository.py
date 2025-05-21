import json
import os

class BiasRepository:
    """
    BiasRepository provides methods to access and query media bias information from a JSON file.
    Attributes:
        bias_file_path (str): Path to the JSON file containing media bias data.
        bias_data (dict): Dictionary holding the loaded bias data.
    """

    def __init__(self, bias_file_path=os.path.join('src', 'media-bias.json')):
        """
        Initializes the BiasRepository with the path to the bias data file.
        Args:
            bias_file_path (str): Path to the JSON file containing media bias data.
        """
        self.bias_file_path = bias_file_path
        self.bias_data = self._load_bias_data()

    def _load_bias_data(self) -> dict:
        """
        Loads bias data from the JSON file and returns it as a dictionary.
        Returns:
            dict: Dictionary containing the bias data.
        """
        with open(self.bias_file_path, encoding='UTF-8') as bias_file:
            bias_data = json.load(bias_file)
        return bias_data
    
    def get_bias(self, channel_id: str) -> str:
        """
        Retrieves the bias of a specific channel by its ID.
        Args:
            channel_id (str): The ID of the channel to retrieve bias for.
        Returns:
            str: The bias of the channel (left, lean-left, center, lean-right or right), or None if the channel ID is not found.
        """
        if channel_id not in self.bias_data:
            return None
        return self.bias_data[channel_id]['bias']
    
    def get_outlet_by_bias(self, bias: str) -> list:
        """
        Retrieves a list of outlets that match a specific bias.
        Args:
            bias (str): The bias to filter outlets by (left, lean-left, center, lean-right or right).
        Returns:
            list: A list of outlet IDs that match the specified bias.
        """
        return [source for source, data in self.bias_data.items() if data['bias'] == bias]
    
    def get_all_outlets(self) -> list:
        """
        Retrieves a list of all outlet IDs in the bias data.
        Returns:
            list: A list of all outlet IDs.
        """
        return list(self.bias_data.keys())
    
    def get_outlet_name_by_id(self, source_id: str) -> str:
        """
        Retrieves the name of an outlet by its ID.
        Args:
            source_id (str): The ID of the outlet to retrieve the name for.
        Returns:
            str: The name of the outlet, or None if the outlet ID is not found.
        """
        return self.bias_data[source_id]['name']
    
if __name__ == '__main__':
    the_american_conservative = "UCiM2qJsoY5oNZuYrh3pZAsg"
    bias_repo = BiasRepository()
    print(bias_repo.get_bias(the_american_conservative))
    print(bias_repo.get_outlet_by_bias('right')[0:3])
    print(bias_repo.get_all_outlets()[0:3])
    print(bias_repo.get_outlet_name_by_id(the_american_conservative))