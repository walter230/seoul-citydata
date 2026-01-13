from supabase import create_client, Client
from typing import Dict, Any, List, Optional
import logging
from .config import Config

logger = logging.getLogger(__name__)

class DBClient:
    """Simplified Client for interacting with Supabase - Single Table version (Population & Commercial Only)"""
    
    def __init__(self):
        Config.validate()
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

    def clean_val(self, val, cast_func=None):
        if val is None or str(val).strip() in ["", "-", "None", "undefined", "데이터 없음"]:
            return None
        if cast_func:
            try:
                if cast_func in [float, int] and isinstance(val, str):
                    val = val.replace(',', '').replace('건', '').replace('원', '')
                return cast_func(val)
            except (ValueError, TypeError):
                return None
        return val

    def get_list(self, data: Any, key: str) -> List[Dict[str, Any]]:
        # Handle the case where the parent node might be a list
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        if not isinstance(data, dict):
            return []
        val = data.get(key)
        if isinstance(val, list): return val
        if isinstance(val, dict) and val: return [val]
        return []

    def get_first(self, data: Any, key: str) -> Dict[str, Any]:
        lst = self.get_list(data, key)
        return lst[0] if lst else {}

    def extract_area_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract population fields (1-27)"""
        live_ppltn = self.get_first(data, "LIVE_PPLTN_STTS")
        
        return {
            "area_nm": self.clean_val(data.get("AREA_NM")),
            "area_cd": self.clean_val(data.get("AREA_CD")),
            "live_ppltn_stts": self.clean_val(live_ppltn.get("LIVE_PPLTN_STTS")),
            "area_congest_lvl": self.clean_val(live_ppltn.get("AREA_CONGEST_LVL")),
            "area_congest_msg": self.clean_val(live_ppltn.get("AREA_CONGEST_MSG")),
            "area_ppltn_min": self.clean_val(live_ppltn.get("AREA_PPLTN_MIN"), int),
            "area_ppltn_max": self.clean_val(live_ppltn.get("AREA_PPLTN_MAX"), int),
            "male_ppltn_rate": self.clean_val(live_ppltn.get("MALE_PPLTN_RATE"), float),
            "female_ppltn_rate": self.clean_val(live_ppltn.get("FEMALE_PPLTN_RATE"), float),
            "ppltn_rate_0": self.clean_val(live_ppltn.get("PPLTN_RATE_0"), float),
            "ppltn_rate_10": self.clean_val(live_ppltn.get("PPLTN_RATE_10"), float),
            "ppltn_rate_20": self.clean_val(live_ppltn.get("PPLTN_RATE_20"), float),
            "ppltn_rate_30": self.clean_val(live_ppltn.get("PPLTN_RATE_30"), float),
            "ppltn_rate_40": self.clean_val(live_ppltn.get("PPLTN_RATE_40"), float),
            "ppltn_rate_50": self.clean_val(live_ppltn.get("PPLTN_RATE_50"), float),
            "ppltn_rate_60": self.clean_val(live_ppltn.get("PPLTN_RATE_60"), float),
            "ppltn_rate_70": self.clean_val(live_ppltn.get("PPLTN_RATE_70"), float),
            "resnt_ppltn_rate": self.clean_val(live_ppltn.get("RESNT_PPLTN_RATE"), float),
            "non_resnt_ppltn_rate": self.clean_val(live_ppltn.get("NON_RESNT_PPLTN_RATE"), float),
            "replace_yn": self.clean_val(live_ppltn.get("REPLACE_YN")),
            "ppltn_time": self.clean_val(live_ppltn.get("PPLTN_TIME")),
            "fcst_yn": self.clean_val(live_ppltn.get("FCST_YN")),
            "fcst_ppltn": self.clean_val(live_ppltn.get("FCST_PPLTN"), int),
            "fcst_time": self.clean_val(live_ppltn.get("FCST_TIME")),
            "fcst_congest_lvl": self.clean_val(live_ppltn.get("FCST_CONGEST_LVL")),
            "fcst_ppltn_min": self.clean_val(live_ppltn.get("FCST_PPLTN_MIN"), int),
            "fcst_ppltn_max": self.clean_val(live_ppltn.get("FCST_PPLTN_MAX"), int),
        }

    def process_and_save(self, raw_data_map: Dict[str, Any]):
        all_payloads = []
        
        for area, raw_data in raw_data_map.items():
            try:
                if "CITYDATA" not in raw_data: continue
                data = raw_data["CITYDATA"]
                
                # Extract Population Data (1-27)
                base_info = self.extract_area_data(data)
                
                # Extract Commercial Data (217-240)
                cmrcl_list = self.get_list(data, "LIVE_CMRCL_STTS")
                
                if not cmrcl_list:
                    # Save at least the population data if no commercial data
                    all_payloads.append(base_info)
                else:
                    # Flatten: One row per industry (rsb) record
                    for item in cmrcl_list:
                        payload = base_info.copy()
                        payload.update({
                            "live_cmrcl_stts": self.clean_val(item.get("LIVE_CMRCL_STTS")),
                            "area_cmrcl_lvl": self.clean_val(item.get("AREA_CMRCL_LVL")),
                            "area_sh_payment_cnt": self.clean_val(item.get("AREA_SH_PAYMENT_CNT"), float),
                            "area_sh_payment_amt_min": self.clean_val(item.get("AREA_SH_PAYMENT_AMT_MIN"), float),
                            "area_sh_payment_amt_max": self.clean_val(item.get("AREA_SH_PAYMENT_AMT_MAX"), float),
                            "rsb_lrg_ctgr": self.clean_val(item.get("RSB_LRG_CTGR")),
                            "rsb_mid_ctgr": self.clean_val(item.get("RSB_MID_CTGR")),
                            "rsb_payment_lvl": self.clean_val(item.get("RSB_PAYMENT_LVL")),
                            "rsb_sh_payment_cnt": self.clean_val(item.get("RSB_SH_PAYMENT_CNT"), float),
                            "rsb_sh_payment_amt_min": self.clean_val(item.get("RSB_SH_PAYMENT_AMT_MIN"), float),
                            "rsb_sh_payment_amt_max": self.clean_val(item.get("RSB_SH_PAYMENT_AMT_MAX"), float),
                            "rsb_mct_cnt": self.clean_val(item.get("RSB_MCT_CNT"), int),
                            "rsb_mct_time": self.clean_val(item.get("RSB_MCT_TIME")),
                            "cmrcl_male_rate": self.clean_val(item.get("CMRCL_MALE_RATE"), float),
                            "cmrcl_female_rate": self.clean_val(item.get("CMRCL_FEMALE_RATE"), float),
                            "cmrcl_10_rate": self.clean_val(item.get("CMRCL_10_RATE"), float),
                            "cmrcl_20_rate": self.clean_val(item.get("CMRCL_20_RATE"), float),
                            "cmrcl_30_rate": self.clean_val(item.get("CMRCL_30_RATE"), float),
                            "cmrcl_40_rate": self.clean_val(item.get("CMRCL_40_RATE"), float),
                            "cmrcl_50_rate": self.clean_val(item.get("CMRCL_50_RATE"), float),
                            "cmrcl_60_rate": self.clean_val(item.get("CMRCL_60_RATE"), float),
                            "cmrcl_personal_rate": self.clean_val(item.get("CMRCL_PERSONAL_RATE"), float),
                            "cmrcl_corporation_rate": self.clean_val(item.get("CMRCL_CORPORATION_RATE"), float),
                            "cmrcl_time": self.clean_val(item.get("CMRCL_TIME")),
                        })
                        all_payloads.append(payload)
                        
            except Exception as e:
                logger.error(f"Failed to process area {area}: {e}")
                continue

        # Bulk insert to Supabase seoul_city_data table
        if all_payloads:
            try:
                cleaned_payloads = [{k: v for k, v in p.items() if v is not None} for p in all_payloads]
                # Split into chunks of 100
                for i in range(0, len(cleaned_payloads), 100):
                    self.supabase.table("seoul_city_data").insert(cleaned_payloads[i:i+100]).execute()
                logger.info(f"Successfully saved {len(cleaned_payloads)} records to seoul_city_data")
            except Exception as e:
                logger.error(f"Database insert failed: {e}")
