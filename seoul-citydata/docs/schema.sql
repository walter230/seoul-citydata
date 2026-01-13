-- Simplified Single Table Schema
-- Optimized for Population (1-27) and Commercial (217-240) data only
BEGIN;

DROP TABLE IF EXISTS city_road_details, city_parking_details, city_subway_status, city_subway_fac, city_subway_ppltn, city_bus_status, city_accidents, city_ev_chargers, city_sbike, city_weather_alerts, city_weather_fcst, city_cultural_events, city_commercial_details, city_disaster_msgs, city_news, city_master;
DROP TABLE IF EXISTS seoul_city_data;

CREATE TABLE seoul_city_data (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 1-2. 공통 정보
    area_nm VARCHAR(255),
    area_cd VARCHAR(100),
    
    -- 3-21. 실시간 인구 현황
    live_ppltn_stts VARCHAR(255),
    area_congest_lvl VARCHAR(100),
    area_congest_msg TEXT,
    area_ppltn_min INTEGER,
    area_ppltn_max INTEGER,
    male_ppltn_rate NUMERIC,
    female_ppltn_rate NUMERIC,
    ppltn_rate_0 NUMERIC,
    ppltn_rate_10 NUMERIC,
    ppltn_rate_20 NUMERIC,
    ppltn_rate_30 NUMERIC,
    ppltn_rate_40 NUMERIC,
    ppltn_rate_50 NUMERIC,
    ppltn_rate_60 NUMERIC,
    ppltn_rate_70 NUMERIC,
    resnt_ppltn_rate NUMERIC,
    non_resnt_ppltn_rate NUMERIC,
    replace_yn VARCHAR(10),
    ppltn_time TIMESTAMP,
    
    -- 22-27. 인구 예측 현황
    fcst_yn VARCHAR(10),
    fcst_ppltn INTEGER,
    fcst_time TIMESTAMP,
    fcst_congest_lvl VARCHAR(100),
    fcst_ppltn_min INTEGER,
    fcst_ppltn_max INTEGER,
    
    -- 217-240. 실시간 상권 현황
    live_cmrcl_stts VARCHAR(255),
    area_cmrcl_lvl VARCHAR(100),
    area_sh_payment_cnt NUMERIC,
    area_sh_payment_amt_min NUMERIC,
    area_sh_payment_amt_max NUMERIC,
    rsb_lrg_ctgr VARCHAR(255),
    rsb_mid_ctgr VARCHAR(255),
    rsb_payment_lvl VARCHAR(100),
    rsb_sh_payment_cnt NUMERIC,
    rsb_sh_payment_amt_min NUMERIC,
    rsb_sh_payment_amt_max NUMERIC,
    rsb_mct_cnt INTEGER,
    rsb_mct_time VARCHAR(100),
    cmrcl_male_rate NUMERIC,
    cmrcl_female_rate NUMERIC,
    cmrcl_10_rate NUMERIC,
    cmrcl_20_rate NUMERIC,
    cmrcl_30_rate NUMERIC,
    cmrcl_40_rate NUMERIC,
    cmrcl_50_rate NUMERIC,
    cmrcl_60_rate NUMERIC,
    cmrcl_personal_rate NUMERIC,
    cmrcl_corporation_rate NUMERIC,
    cmrcl_time TIMESTAMP
);

COMMIT;

CREATE INDEX IF NOT EXISTS idx_seoul_city_data_area_nm ON seoul_city_data(area_nm);
CREATE INDEX IF NOT EXISTS idx_seoul_city_data_created_at ON seoul_city_data(created_at);
