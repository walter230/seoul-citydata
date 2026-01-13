from supabase import create_client, Client
from typing import Dict, Any, List, Optional
import logging
import json
from .config import Config

logger = logging.getLogger(__name__)

class DBClient:
    """Client for interacting with Supabase - Comprehensive Multi-table version"""
    
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
        """Safely extract a list of items from data, handling cases where data is a list itself"""
        # If data is a list, take the first element (common in Seoul City API)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
            
        if not isinstance(data, dict):
            return []
            
        val = data.get(key)
        if isinstance(val, list): return val
        if isinstance(val, dict) and val: return [val]
        return []

    def get_first(self, data: Any, key: str) -> Dict[str, Any]:
        """Safely extract the first item from a list or object"""
        lst = self.get_list(data, key)
        return lst[0] if lst else {}

    def transform_master(self, data: Dict[str, Any]) -> Dict[str, Any]:
        live_ppltn = self.get_first(data, "LIVE_PPLTN_STTS")
        
        # Ensure sub-objects are dicts even if they come back as lists
        road_traffic = self.get_first(data, "ROAD_TRAFFIC_STTS")
        subway_obj = self.get_first(data, "SUB_STTS")
        bus_obj = self.get_first(data, "BUS_STN_STTS")
        weather_info = self.get_first(data, "WEATHER_STTS")
        
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
            "road_traffic_stts": self.clean_val(road_traffic.get("ROAD_TRAFFIC_STTS")),
            "road_traffic_spd": self.clean_val(road_traffic.get("ROAD_TRAFFIC_SPD"), float),
            "road_traffic_idx": self.clean_val(road_traffic.get("ROAD_TRAFFIC_IDX")),
            "road_traffic_time": self.clean_val(road_traffic.get("ROAD_TRAFFIC_TIME")),
            "road_msg": self.clean_val(road_traffic.get("ROAD_MSG")),
            "sub_stn_cnt": self.clean_val(subway_obj.get("SUB_STN_CNT"), int),
            "sub_stn_time": self.clean_val(subway_obj.get("SUB_STN_TIME")),
            "bus_stn_cnt": self.clean_val(bus_obj.get("BUS_STN_CNT"), int),
            "bus_stn_time": self.clean_val(bus_obj.get("BUS_STN_TIME")),
            "temp": self.clean_val(weather_info.get("TEMP"), float),
            "sensible_temp": self.clean_val(weather_info.get("SENSIBLE_TEMP"), float),
            "max_temp": self.clean_val(weather_info.get("MAX_TEMP"), float),
            "min_temp": self.clean_val(weather_info.get("MIN_TEMP"), float),
            "humidity": self.clean_val(weather_info.get("HUMIDITY"), float),
            "wind_dirct": self.clean_val(weather_info.get("WIND_DIRCT")),
            "wind_spd": self.clean_val(weather_info.get("WIND_SPD"), float),
            "precipitation": self.clean_val(weather_info.get("PRECIPITATION"), float),
            "precept_type": self.clean_val(weather_info.get("PRECPT_TYPE")),
            "pcp_msg": self.clean_val(weather_info.get("PCP_MSG")),
            "sunrise": self.clean_val(weather_info.get("SUNRISE")),
            "sunset": self.clean_val(weather_info.get("SUNSET")),
            "uv_index_lvl": self.clean_val(weather_info.get("UV_INDEX_LVL")),
            "uv_index": self.clean_val(weather_info.get("UV_INDEX"), float),
            "uv_msg": self.clean_val(weather_info.get("UV_MSG")),
            "pm25_index": self.clean_val(weather_info.get("PM25_INDEX")),
            "pm25": self.clean_val(weather_info.get("PM25"), float),
            "pm10_index": self.clean_val(weather_info.get("PM10_INDEX")),
            "pm10": self.clean_val(weather_info.get("PM10"), float),
            "air_idx": self.clean_val(weather_info.get("AIR_IDX")),
            "air_idx_mvl": self.clean_val(weather_info.get("AIR_IDX_MVL"), float),
            "air_idx_main": self.clean_val(weather_info.get("AIR_IDX_MAIN")),
            "air_msg": self.clean_val(weather_info.get("AIR_MSG")),
            "weather_time": self.clean_val(weather_info.get("WEATHER_TIME"))
        }

    def process_and_save(self, raw_data_map: Dict[str, Any]):
        for area, raw_data in raw_data_map.items():
            try:
                if "CITYDATA" not in raw_data: continue
                data = raw_data["CITYDATA"]
                
                # Insert MASTER
                master_payload = self.transform_master(data)
                res = self.supabase.table("city_master").insert(master_payload).execute()
                master_id = res.data[0]["id"]
                
                # Helper to bulk insert
                def bulk_insert(table, items, mapping_fn):
                    if not items: return
                    payloads = [mapping_fn(item) for item in items]
                    filtered = [{k: v for k, v in p.items() if v is not None} for p in payloads]
                    if filtered: self.supabase.table(table).insert(filtered).execute()

                # Process all sub-lists
                bulk_insert("city_road_details", self.get_list(self.get_first(data, "ROAD_TRAFFIC_STTS"), "AVG_ROAD_DATA"),
                    lambda x: { "master_id": master_id, "link_id": x.get("LINK_ID"), "road_nm": x.get("ROAD_NM"), "start_nd_cd": x.get("START_ND_CD"), "start_nd_nm": x.get("START_ND_NM"), "start_nd_xy": x.get("START_ND_XY"), "end_nd_cd": x.get("END_ND_CD"), "end_nd_nm": x.get("END_ND_NM"), "end_nd_xy": x.get("END_ND_XY"), "dist": self.clean_val(x.get("DIST"), int), "spd": self.clean_val(x.get("SPD"), int), "idx": x.get("IDX"), "xylist": x.get("XYLIST") })

                bulk_insert("city_parking_details", self.get_list(self.get_first(data, "PRK_STTS"), "PRK_STTS"),
                    lambda x: { "master_id": master_id, "prk_nm": x.get("PRK_NM"), "prk_cd": x.get("PRK_CD"), "prk_type": x.get("PRK_TYPE"), "cpcty": self.clean_val(x.get("CPCTY"), int), "cur_prk_cnt": self.clean_val(x.get("CUR_PRK_CNT"), int), "cur_prk_time": self.clean_val(x.get("CUR_PRK_TIME")), "cur_prk_yn": x.get("CUR_PRK_YN"), "pay_yn": x.get("PAY_YN"), "rates": x.get("RATES"), "time_rates": self.clean_val(x.get("TIME_RATES"), int), "add_rates": self.clean_val(x.get("ADD_RATES"), int), "add_time_rates": self.clean_val(x.get("ADD_TIME_RATES"), int), "road_addr": x.get("ROAD_ADDR"), "address": x.get("ADDRESS"), "lat": self.clean_val(x.get("LAT"), float), "lng": self.clean_val(x.get("LNG"), float) })

                bulk_insert("city_subway_status", self.get_list(self.get_first(data, "SUB_STTS"), "SUB_STTS"),
                    lambda x: { "master_id": master_id, "sub_stn_nm": x.get("SUB_STN_NM"), "sub_stn_line": x.get("SUB_STN_LINE"), "sub_stn_raddr": x.get("SUB_STN_RADDR"), "sub_stn_jibun": x.get("SUB_STN_JIBUN"), "sub_stn_x": self.clean_val(x.get("SUB_STN_X"), float), "sub_stn_y": self.clean_val(x.get("SUB_STN_Y"), float), "sub_nt_stn": x.get("SUB_NT_STN"), "sub_bf_stn": x.get("SUB_BF_STN"), "sub_route_nm": x.get("SUB_ROUTE_NM"), "sub_line": x.get("SUB_LINE"), "sub_ord": self.clean_val(x.get("SUB_ORD"), int), "sub_dir": x.get("SUB_DIR"), "sub_terminal": x.get("SUB_TERMINAL"), "sub_arvtime": self.clean_val(x.get("SUB_ARVTIME")), "sub_armg1": x.get("SUB_ARMG1"), "sub_armg2": x.get("SUB_ARMG2"), "sub_arvinfo": x.get("SUB_ARVINFO") })

                bulk_insert("city_subway_fac", self.get_list(self.get_first(data, "SUB_STTS"), "SUB_FACINFO"),
                    lambda x: { "master_id": master_id, "elvtr_nm": x.get("ELVTR_NM"), "opr_sec": x.get("OPR_SEC"), "instl_pstn": x.get("INSTL_PSTN"), "use_yn": x.get("USE_YN"), "elvtr_se": x.get("ELVTR_SE") })

                bulk_insert("city_subway_ppltn", self.get_list(self.get_first(data, "SUB_STTS"), "LIVE_SUB_PPLTN"),
                    lambda x: { "master_id": master_id, "sub_acml_gton_ppltn_min": self.clean_val(x.get("SUB_ACML_GTON_PPLTN_MIN"), int), "sub_acml_gton_ppltn_max": self.clean_val(x.get("SUB_ACML_GTON_PPLTN_MAX"), int), "sub_acml_gtoff_ppltn_min": self.clean_val(x.get("SUB_ACML_GTOFF_PPLTN_MIN"), int), "sub_acml_gtoff_ppltn_max": self.clean_val(x.get("SUB_ACML_GTOFF_PPLTN_MAX"), int), "sub_30wthn_gton_ppltn_min": self.clean_val(x.get("SUB_30WTHN_GTON_PPLTN_MIN"), int), "sub_30wthn_gton_ppltn_max": self.clean_val(x.get("SUB_30WTHN_GTON_PPLTN_MAX"), int), "sub_30wthn_gtoff_ppltn_min": self.clean_val(x.get("SUB_30WTHN_GTOFF_PPLTN_MIN"), int), "sub_30wthn_gtoff_ppltn_max": self.clean_val(x.get("SUB_30WTHN_GTOFF_PPLTN_MAX"), int), "sub_10wthn_gton_ppltn_min": self.clean_val(x.get("SUB_10WTHN_GTON_PPLTN_MIN"), int), "sub_10wthn_gton_ppltn_max": self.clean_val(x.get("SUB_10WTHN_GTON_PPLTN_MAX"), int), "sub_10wthn_gtoff_ppltn_min": self.clean_val(x.get("SUB_10WTHN_GTOFF_PPLTN_MIN"), int), "sub_10wthn_gtoff_ppltn_max": self.clean_val(x.get("SUB_10WTHN_GTOFF_PPLTN_MAX"), int), "sub_5wthn_gton_ppltn_min": self.clean_val(x.get("SUB_5WTHN_GTON_PPLTN_MIN"), int), "sub_5wthn_gton_ppltn_max": self.clean_val(x.get("SUB_5WTHN_GTON_PPLTN_MAX"), int), "sub_5wthn_gtoff_ppltn_min": self.clean_val(x.get("SUB_5WTHN_GTOFF_PPLTN_MIN"), int), "sub_5wthn_gtoff_ppltn_max": self.clean_val(x.get("SUB_5WTHN_GTOFF_PPLTN_MAX"), int) })

                bulk_insert("city_bus_status", self.get_list(self.get_first(data, "BUS_STN_STTS"), "BUS_STN_STTS"),
                    lambda x: { "master_id": master_id, "bus_stn_id": x.get("BUS_STN_ID"), "bus_ars_id": x.get("BUS_ARS_ID"), "bus_stn_nm": x.get("BUS_STN_NM"), "bus_stn_x": self.clean_val(x.get("BUS_STN_X"), float), "bus_stn_y": self.clean_val(x.get("BUS_STN_Y"), float), "bus_acml_gton_ppltn_min": self.clean_val(x.get("BUS_ACML_GTON_PPLTN_MIN"), int), "bus_acml_gton_ppltn_max": self.clean_val(x.get("BUS_ACML_GTON_PPLTN_MAX"), int), "bus_acml_gtoff_ppltn_min": self.clean_val(x.get("BUS_ACML_GTOFF_PPLTN_MIN"), int), "bus_acml_gtoff_ppltn_max": self.clean_val(x.get("BUS_ACML_GTOFF_PPLTN_MAX"), int), "bus_30wthn_gton_ppltn_min": self.clean_val(x.get("BUS_30WTHN_GTON_PPLTN_MIN"), int), "bus_30wthn_gton_ppltn_max": self.clean_val(x.get("BUS_30WTHN_GTON_PPLTN_MAX"), int), "bus_30wthn_gtoff_ppltn_min": self.clean_val(x.get("BUS_30WTHN_GTOFF_PPLTN_MIN"), int), "bus_30wthn_gtoff_ppltn_max": self.clean_val(x.get("BUS_30WTHN_GTOFF_PPLTN_MAX"), int), "bus_10wthn_gton_ppltn_min": self.clean_val(x.get("BUS_10WTHN_GTON_PPLTN_MIN"), int), "bus_10wthn_gton_ppltn_max": self.clean_val(x.get("BUS_10WTHN_GTON_PPLTN_MAX"), int), "bus_10wthn_gtoff_ppltn_min": self.clean_val(x.get("BUS_10WTHN_GTOFF_PPLTN_MIN"), int), "bus_10wthn_gtoff_ppltn_max": self.clean_val(x.get("BUS_10WTHN_GTOFF_PPLTN_MAX"), int), "bus_5wthn_gton_ppltn_min": self.clean_val(x.get("BUS_5WTHN_GTON_PPLTN_MIN"), int), "bus_5wthn_gton_ppltn_max": self.clean_val(x.get("BUS_5WTHN_GTON_PPLTN_MAX"), int), "bus_5wthn_gtoff_ppltn_min": self.clean_val(x.get("BUS_5WTHN_GTOFF_PPLTN_MIN"), int), "bus_5wthn_gtoff_ppltn_max": self.clean_val(x.get("BUS_5WTHN_GTOFF_PPLTN_MAX"), int) })

                bulk_insert("city_accidents", self.get_list(self.get_first(data, "ACDNT_CNTRL_STTS"), "ACDNT_CNTRL_STTS"),
                    lambda x: { "master_id": master_id, "acdnt_occr_dt": self.clean_val(x.get("ACDNT_OCCR_DT")), "exp_clr_dt": self.clean_val(x.get("EXP_CLR_DT")), "acdnt_type": x.get("ACDNT_TYPE"), "acdnt_dtype": x.get("ACDNT_DTYPE"), "acdnt_info": x.get("ACDNT_INFO"), "acdnt_x": self.clean_val(x.get("ACDNT_X"), float), "acdnt_y": self.clean_val(x.get("ACDNT_Y"), float), "acdnt_time": self.clean_val(x.get("ACDNT_TIME")) })

                bulk_insert("city_ev_chargers", self.get_list(self.get_first(data, "CHARGER_STTS"), "CHARGER_STTS"),
                    lambda x: { "master_id": master_id, "stat_nm": x.get("STAT_NM"), "stat_id": x.get("STAT_ID"), "stat_addr": x.get("STAT_ADDR"), "stat_x": self.clean_val(x.get("STAT_X"), float), "stat_y": self.clean_val(x.get("STAT_Y"), float), "stat_usetime": x.get("STAT_USETIME"), "stat_parkpay": x.get("STAT_PARKPAY"), "stat_limityn": x.get("STAT_LIMITYN"), "stat_limitdetail": x.get("STAT_LIMITDETAIL"), "stat_kinddetail": x.get("STAT_KINDDETAIL"), "charger_id": x.get("CHARGER_ID"), "charger_type": x.get("CHARGER_TYPE"), "charger_stat": x.get("CHARGER_STAT"), "statupddt": self.clean_val(x.get("STATUPDDT")), "lasttsdt": self.clean_val(x.get("LASTTSDT")), "lasttedt": self.clean_val(x.get("LASTTEDT")), "nowtsdt": self.clean_val(x.get("NOWTSDT")), "output": self.clean_val(x.get("OUTPUT"), float), "method": x.get("METHOD") })

                bulk_insert("city_sbike", self.get_list(self.get_first(data, "SBIKE_STTS"), "SBIKE_STTS"),
                    lambda x: { "master_id": master_id, "sbike_spot_nm": x.get("SBIKE_SPOT_NM"), "sbike_spot_id": x.get("SBIKE_SPOT_ID"), "sbike_shared": self.clean_val(x.get("SBIKE_SHARED"), float), "sbike_parking_cnt": self.clean_val(x.get("SBIKE_PARKING_CNT"), int), "sbike_rack_cnt": self.clean_val(x.get("SBIKE_RACK_CNT"), int), "sbike_x": self.clean_val(x.get("SBIKE_X"), float), "sbike_y": self.clean_val(x.get("SBIKE_Y"), float) })

                bulk_insert("city_weather_alerts", self.get_list(self.get_first(data, "WEATHER_STTS"), "NEWS_LIST"),
                    lambda x: { "master_id": master_id, "warn_val": x.get("WARN_VAL"), "warn_stress": x.get("WARN_STRESS"), "announce_time": self.clean_val(x.get("ANNOUNCE_TIME")), "command": x.get("COMMAND"), "cancel_yn": x.get("CANCEL_YN"), "warn_msg": x.get("WARN_MSG") })

                bulk_insert("city_weather_fcst", self.get_list(self.get_first(data, "WEATHER_STTS"), "FCST24HOURS"),
                    lambda x: { "master_id": master_id, "fcst_dt": self.clean_val(x.get("FCST_DT")), "temp": self.clean_val(x.get("TEMP"), float), "precipitation": self.clean_val(x.get("PRECIPITATION"), float), "precept_type": x.get("PRECPT_TYPE"), "rain_chance": self.clean_val(x.get("RAIN_CHANCE"), float) })

                bulk_insert("city_cultural_events", self.get_list(data, "CULTURALEVENTINFO"),
                    lambda x: { "master_id": master_id, "event_nm": x.get("EVENT_NM"), "event_period": x.get("EVENT_PERIOD"), "event_place": x.get("EVENT_PLACE"), "event_x": self.clean_val(x.get("EVENT_X"), float), "event_y": self.clean_val(x.get("EVENT_Y"), float), "pay_yn": x.get("PAY_YN"), "thumbnail": x.get("THUMBNAIL"), "url": x.get("URL"), "event_etc_detail": x.get("EVENT_ETC_DETAIL") })

                # 14. COMMERCIAL DETAILS (217-240) - One row per industry record
                bulk_insert("city_commercial_details", self.get_list(data, "LIVE_CMRCL_STTS"),
                    lambda x: { "master_id": master_id, "live_cmrcl_stts": x.get("LIVE_CMRCL_STTS"), "area_cmrcl_lvl": x.get("AREA_CMRCL_LVL"), "area_sh_payment_cnt": self.clean_val(x.get("AREA_SH_PAYMENT_CNT"), float), "area_sh_payment_amt_min": self.clean_val(x.get("AREA_SH_PAYMENT_AMT_MIN"), float), "area_sh_payment_amt_max": self.clean_val(x.get("AREA_SH_PAYMENT_AMT_MAX"), float), "rsb_lrg_ctgr": x.get("RSB_LRG_CTGR"), "rsb_mid_ctgr": x.get("RSB_MID_CTGR"), "rsb_payment_lvl": x.get("RSB_PAYMENT_LVL"), "rsb_sh_payment_cnt": self.clean_val(x.get("RSB_SH_PAYMENT_CNT"), float), "rsb_sh_payment_amt_min": self.clean_val(x.get("RSB_SH_PAYMENT_AMT_MIN"), float), "rsb_sh_payment_amt_max": self.clean_val(x.get("RSB_SH_PAYMENT_AMT_MAX"), float), "rsb_mct_cnt": self.clean_val(x.get("RSB_MCT_CNT"), int), "rsb_mct_time": x.get("RSB_MCT_TIME"), "cmrcl_male_rate": self.clean_val(x.get("CMRCL_MALE_RATE"), float), "cmrcl_female_rate": self.clean_val(x.get("CMRCL_FEMALE_RATE"), float), "cmrcl_10_rate": self.clean_val(x.get("CMRCL_10_RATE"), float), "cmrcl_20_rate": self.clean_val(x.get("CMRCL_20_RATE"), float), "cmrcl_30_rate": self.clean_val(x.get("CMRCL_30_RATE"), float), "cmrcl_40_rate": self.clean_val(x.get("CMRCL_40_RATE"), float), "cmrcl_50_rate": self.clean_val(x.get("CMRCL_50_RATE"), float), "cmrcl_60_rate": self.clean_val(x.get("CMRCL_60_RATE"), float), "cmrcl_personal_rate": self.clean_val(x.get("CMRCL_PERSONAL_RATE"), float), "cmrcl_corporation_rate": self.clean_val(x.get("CMRCL_CORPORATION_RATE"), float), "cmrcl_time": self.clean_val(x.get("CMRCL_TIME")) })

                bulk_insert("city_disaster_msgs", self.get_list(data, "LIVE_DST_MESSAGE"),
                    lambda x: { "master_id": master_id, "dst_se_nm": x.get("DST_SE_NM"), "emrg_step_nm": x.get("EMRG_STEP_NM"), "msg_cn": x.get("MSG_CN"), "crt_dt": self.clean_val(x.get("CRT_DT")) })

                bulk_insert("city_news", self.get_list(data, "LIVE_YNA_NEWS"),
                    lambda x: { "master_id": master_id, "yna_step_nm": x.get("YNA_STEP_NM"), "yna_ttl": x.get("YNA_TTL"), "yna_cn": x.get("YNA_CN"), "yna_ymd": x.get("YNA_YMD"), "yna_wrtr_nm": x.get("YNA_WRTR_NM") })

                logger.info(f"Successfully processed all 251 fields for {area}")
                
            except Exception as e:
                logger.error(f"Failed to process area {area}: {e}")
                continue
