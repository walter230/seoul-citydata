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
        if "CITYDATA" not in raw_data:
            logger.warning("Invalid data format: CITYDATA key missing")
            return {}
        data = raw_data["CITYDATA"]
        
        def clean_val(val, cast_func=None):
            if val is None or str(val).strip() in ["", "-", "None", "undefined"]:
                return None
            if cast_func:
                try:
                    return cast_func(val)
                except (ValueError, TypeError):
                    return None
            return val

        live_ppltn_list = data.get("LIVE_PPLTN_STTS", [{}])
        live_ppltn = live_ppltn_list[0] if isinstance(live_ppltn_list, list) and live_ppltn_list else {}
        weather_list = data.get("WEATHER_STTS", [{}])
        weather = weather_list[0] if isinstance(weather_list, list) and weather_list else {}

        payload = {
            "area_nm": clean_val(data.get("AREA_NM")),
            "area_cd": clean_val(data.get("AREA_CD")),
            "live_ppltn_stts": clean_val(live_ppltn.get("LIVE_PPLTN_STTS")),
            "area_congest_lvl": clean_val(live_ppltn.get("AREA_CONGEST_LVL")),
            "area_congest_msg": clean_val(live_ppltn.get("AREA_CONGEST_MSG")),
            "area_ppltn_min": clean_val(live_ppltn.get("AREA_PPLTN_MIN"), int),
            "area_ppltn_max": clean_val(live_ppltn.get("AREA_PPLTN_MAX"), int),
            "male_ppltn_rate": clean_val(live_ppltn.get("MALE_PPLTN_RATE"), float),
            "female_ppltn_rate": clean_val(live_ppltn.get("FEMALE_PPLTN_RATE"), float),
            "ppltn_time": clean_val(live_ppltn.get("PPLTN_TIME")),
            "weather_stts": clean_val(weather.get("WEATHER_STTS")),
            "temp": clean_val(weather.get("TEMP"), float),
            "sensible_temp": clean_val(weather.get("SENSIBLE_TEMP"), float),
            "humidity": clean_val(weather.get("HUMIDITY"), float),
            "wind_dirct": clean_val(weather.get("WIND_DIRCT")),
            "wind_spd": clean_val(weather.get("WIND_SPD"), float),
            "precipitation": clean_val(weather.get("PRECIPITATION"), float),
            "weather_time": clean_val(weather.get("WEATHER_TIME")),
            "raw_data": json.dumps(raw_data) 
        }
        return payload

    def insert_data(self, payload: Dict[str, Any]):
        try:
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            data, count = self.supabase.table(self.table_name).insert(filtered_payload).execute()
            logger.info(f"Successfully inserted data for {filtered_payload.get('area_nm')}")
            return data
        except Exception as e:
            logger.error(f"Error inserting data into Supabase: {e}")
            raise

    def process_and_save(self, raw_data_list: Dict[str, Any]):
        for area, raw_data in raw_data_list.items():
            try:
                payload = self.transform_data(raw_data)
                if payload and payload.get("area_nm"):
                    self.insert_data(payload)
            except Exception as e:
                logger.error(f"Failed to process area {area}: {e}")
                continue
