from supabase import create_client, Client
from typing import Dict, Any, List
import logging
import json
from .config import Config

logger = logging.getLogger(__name__)

class DBClient:
    """Client for interacting with Supabase"""
    
    def __init__(self):
        Config.validate()
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.table_name = "seoul_city_data"

    def transform_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform API raw data (JSON keys) to Database Schema (snake_case)
        The structure of raw_data is expected to be the 'CITYDATA' object or the root.
        Based on Seoul API, the root has 'CITYDATA'.
        """
        if 'CITYDATA' not in raw_data:
            logger.warning("Invalid data format: 'CITYDATA' key missing")
            return {}

        data = raw_data['CITYDATA']
        
        # Helper to safely get value or None
        def clean_val(val, cast_func=None):
            pass
            if val is None or str(val).strip() in ['', '-', 'None']:
                return None
            if cast_func:
                try:
                    return cast_func(val)
                except:
                    return None
            return val

        # Extract nested objects if they exist
        # Note: Some fields like LIVE_PPLTN_STTS might be a list or object inside.
        # The sample structure typically has flat top-level fields OR nested.
        # Let's assume the API returns the fields directly under CITYDATA or we handle the nesting.
        # Actually LIVE_PPLTN_STTS is usually a valid key returning an array/object.
        
        live_ppltn = data.get('LIVE_PPLTN_STTS', [{}])
        if isinstance(live_ppltn, list) and len(live_ppltn) > 0:
            live_ppltn = live_ppltn[0] # Take first item if list
            
        weather = data.get('WEATHER_STTS', [{}])
        if isinstance(weather, list) and len(weather) > 0:
            weather = weather[0]

        # Construct payload
        payload = {
            # Common
            'area_nm': clean_val('AREA_NM'),
            'area_cd': clean_val('AREA_CD'),
            
            # Live Population
            'live_ppltn_stts': live_ppltn.get('LIVE_PPLTN_STTS'),
            'area_congest_lvl': live_ppltn.get('AREA_CONGEST_LVL'),
            'area_congest_msg': live_ppltn.get('AREA_CONGEST_MSG'),
            'area_ppltn_min': clean_val('AREA_PPLTN_MIN', int) or live_ppltn.get('AREA_PPLTN_MIN'), # sometimes duplicated
            'area_ppltn_max': clean_val('AREA_PPLTN_MAX', int),
            'male_ppltn_rate': clean_val('MALE_PPLTN_RATE', float),
            'female_ppltn_rate': clean_val('FEMALE_PPLTN_RATE', float),
            # ... Add other population rates as needed (omitted for brevity but can be added)
            'ppltn_time': live_ppltn.get('PPLTN_TIME'),
            
            # Weather
            'weather_stts': weather.get('WEATHER_STTS'),
            'temp': weather.get('TEMP'),
            'sensible_temp': weather.get('SENSIBLE_TEMP'),
            'humidity': weather.get('HUMIDITY'),
            'wind_dirct': weather.get('WIND_DIRCT'),
            'wind_spd': weather.get('WIND_SPD'),
            'precipitation': weather.get('PRECIPITATION'),
            'weather_time': weather.get('WEATHER_TIME'),
            
            # Store raw data for debugging/completeness if schema allows
            'raw_data': json.dumps(raw_data) 
        }
        
        # Clean up None values if necessary, or let DB handle nulls
        return payload

    def insert_data(self, payload: Dict[str, Any]):
        """Insert transformed data into Supabase"""
        try:
            data, count = self.supabase.table(self.table_name).insert(payload).execute()
            logger.info(f"Successfully inserted data for {payload.get('area_nm')}")
            return data
        except Exception as e:
            logger.error(f"Error inserting data into Supabase: {e}")
            raise

    def process_and_save(self, raw_data_list: Dict[str, Any]):
        """Process a dictionary of area->data and save to DB"""
        for area, raw_data in raw_data_list.items():
            payload = self.transform_data(raw_data)
            if payload:
                self.insert_data(payload)
