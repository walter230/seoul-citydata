import requests
import json
import logging
from typing import Dict, Any, Optional
from urllib.parse import quote
from .config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CityDataAPIClient:
    """Client for fetching Seoul City Real-Time Data"""

    def __init__(self):
        Config.validate()
        self.api_key = Config.SEOUL_API_KEY
        self.base_url = Config.SEOUL_API_BASE_URL

    def fetch_city_data(self, area_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real-time data for a specific area.
        
        Args:
            area_name (str): Name of the area (e.g., "강남역")
            
        Returns:
            dict: Parsed JSON data or None if failed
        """
        try:
            # URL Encoding for the area name
            encoded_area_name = quote(area_name)
            
            # Construct URL: http://openapi.seoul.go.kr:8088/(key)/json/citydata/1/100/(area_name)
            # Using JSON for easier parsing in Python.
            # Updated range to 1/100 as per user request for better data coverage.
            url = f"{self.base_url}/{self.api_key}/json/citydata/1/100/{encoded_area_name}"
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            logger.info(f"Successfully fetched data for {area_name}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching data for {area_name}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {area_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {area_name}: {e}")
            return None

    def get_data_for_all_targets(self) -> Dict[str, Any]:
        """Fetch data for all target areas defined in Config"""
        results = {}
        for area in Config.TARGET_AREAS:
            data = self.fetch_city_data(area)
            if data:
                results[area] = data
        return results
