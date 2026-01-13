-- Comprehensive Seoul City Data Schema
-- Normalized structure to store all 251 fields as individual columns

BEGIN;

-- 1. Master Table: Common Info, Population, Weather Summary, etc.
CREATE TABLE IF NOT EXISTS city_master (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 1-2. 공통 정보
    area_nm VARCHAR(255) NOT NULL,
    area_cd VARCHAR(50),
    
    -- 3-21. 실시간 인구 현황
    live_ppltn_stts VARCHAR(50),
    area_congest_lvl VARCHAR(50),
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
    replace_yn VARCHAR(1),
    ppltn_time TIMESTAMP,
    
    -- 22-27. 인구 예측 현황
    fcst_yn VARCHAR(1),
    fcst_ppltn INTEGER,
    fcst_time TIMESTAMP,
    fcst_congest_lvl VARCHAR(50),
    fcst_ppltn_min INTEGER,
    fcst_ppltn_max INTEGER,
    
    -- 28-32. 도로 소통 요약
    road_traffic_stts VARCHAR(50),
    road_traffic_spd NUMERIC,
    road_traffic_idx VARCHAR(50),
    road_traffic_time TIMESTAMP,
    road_msg TEXT,
    
    -- 103-104. 지하철 요약
    sub_stn_cnt INTEGER,
    sub_stn_time VARCHAR(50),
    
    -- 129-130. 버스 요약
    bus_stn_cnt INTEGER,
    bus_stn_time VARCHAR(50),
    
    -- 168-192. 날씨 현황
    temp NUMERIC,
    sensible_temp NUMERIC,
    max_temp NUMERIC,
    min_temp NUMERIC,
    humidity NUMERIC,
    wind_dirct VARCHAR(50),
    wind_spd NUMERIC,
    precipitation NUMERIC,
    precept_type VARCHAR(50),
    pcp_msg TEXT,
    sunrise VARCHAR(20),
    sunset VARCHAR(20),
    uv_index_lvl VARCHAR(50),
    uv_index NUMERIC,
    uv_msg TEXT,
    pm25_index VARCHAR(50),
    pm25 NUMERIC,
    pm10_index VARCHAR(50),
    pm10 NUMERIC,
    air_idx VARCHAR(50),
    air_idx_mvl NUMERIC,
    air_idx_main VARCHAR(50),
    air_msg TEXT,
    weather_time TIMESTAMP
);

-- 2. 도로 상세 정보 (33-44)
CREATE TABLE IF NOT EXISTS city_road_details (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    link_id VARCHAR(50),
    road_nm VARCHAR(100),
    start_nd_cd VARCHAR(50),
    start_nd_nm VARCHAR(100),
    start_nd_xy VARCHAR(100),
    end_nd_cd VARCHAR(50),
    end_nd_nm VARCHAR(100),
    end_nd_xy VARCHAR(100),
    dist INTEGER,
    spd INTEGER,
    idx VARCHAR(50),
    xylist TEXT
);

-- 3. 주차장 현황 (45-61)
CREATE TABLE IF NOT EXISTS city_parking_details (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    prk_nm VARCHAR(255),
    prk_cd VARCHAR(50),
    prk_type VARCHAR(50),
    cpcty INTEGER,
    cur_prk_cnt INTEGER,
    cur_prk_time TIMESTAMP,
    cur_prk_yn VARCHAR(1),
    pay_yn VARCHAR(1),
    rates VARCHAR(100),
    time_rates INTEGER,
    add_rates INTEGER,
    add_time_rates INTEGER,
    road_addr TEXT,
    address TEXT,
    lat NUMERIC,
    lng NUMERIC
);

-- 4. 지하철 상세 현황 (62-79)
CREATE TABLE IF NOT EXISTS city_subway_status (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    sub_stn_nm VARCHAR(100),
    sub_stn_line VARCHAR(50),
    sub_stn_raddr TEXT,
    sub_stn_jibun TEXT,
    sub_stn_x NUMERIC,
    sub_stn_y NUMERIC,
    sub_nt_stn VARCHAR(50),
    sub_bf_stn VARCHAR(50),
    sub_route_nm VARCHAR(100),
    sub_line VARCHAR(50),
    sub_ord INTEGER,
    sub_dir VARCHAR(50),
    sub_terminal VARCHAR(100),
    sub_arvtime TIMESTAMP,
    sub_armg1 TEXT,
    sub_armg2 TEXT,
    sub_arvinfo VARCHAR(50)
);

-- 5. 지하철 편의시설 (80-85)
CREATE TABLE IF NOT EXISTS city_subway_fac (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    elvtr_nm VARCHAR(100),
    opr_sec TEXT,
    instl_pstn TEXT,
    use_yn VARCHAR(1),
    elvtr_se VARCHAR(50)
);

-- 6. 지하철 실시간 인원 (86-102)
CREATE TABLE IF NOT EXISTS city_subway_ppltn (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    sub_acml_gton_ppltn_min INTEGER,
    sub_acml_gton_ppltn_max INTEGER,
    sub_acml_gtoff_ppltn_min INTEGER,
    sub_acml_gtoff_ppltn_max INTEGER,
    sub_30wthn_gton_ppltn_min INTEGER,
    sub_30wthn_gton_ppltn_max INTEGER,
    sub_30wthn_gtoff_ppltn_min INTEGER,
    sub_30wthn_gtoff_ppltn_max INTEGER,
    sub_10wthn_gton_ppltn_min INTEGER,
    sub_10wthn_gton_ppltn_max INTEGER,
    sub_10wthn_gtoff_ppltn_min INTEGER,
    sub_10wthn_gtoff_ppltn_max INTEGER,
    sub_5wthn_gton_ppltn_min INTEGER,
    sub_5wthn_gton_ppltn_max INTEGER,
    sub_5wthn_gtoff_ppltn_min INTEGER,
    sub_5wthn_gtoff_ppltn_max INTEGER
);

-- 7. 버스 정류소 현황 (105-128)
CREATE TABLE IF NOT EXISTS city_bus_status (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    bus_stn_id VARCHAR(50),
    bus_ars_id VARCHAR(50),
    bus_stn_nm VARCHAR(100),
    bus_stn_x NUMERIC,
    bus_stn_y NUMERIC,
    bus_acml_gton_ppltn_min INTEGER,
    bus_acml_gton_ppltn_max INTEGER,
    bus_acml_gtoff_ppltn_min INTEGER,
    bus_acml_gtoff_ppltn_max INTEGER,
    bus_30wthn_gton_ppltn_min INTEGER,
    bus_30wthn_gton_ppltn_max INTEGER,
    bus_30wthn_gtoff_ppltn_min INTEGER,
    bus_30wthn_gtoff_ppltn_max INTEGER,
    bus_10wthn_gton_ppltn_min INTEGER,
    bus_10wthn_gton_ppltn_max INTEGER,
    bus_10wthn_gtoff_ppltn_min INTEGER,
    bus_10wthn_gtoff_ppltn_max INTEGER,
    bus_5wthn_gton_ppltn_min INTEGER,
    bus_5wthn_gton_ppltn_max INTEGER,
    bus_5wthn_gtoff_ppltn_min INTEGER,
    bus_5wthn_gtoff_ppltn_max INTEGER
);

-- 8. 사고통제현황 (131-139)
CREATE TABLE IF NOT EXISTS city_accidents (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    acdnt_occr_dt TIMESTAMP,
    exp_clr_dt TIMESTAMP,
    acdnt_type VARCHAR(100),
    acdnt_dtype VARCHAR(100),
    acdnt_info TEXT,
    acdnt_x NUMERIC,
    acdnt_y NUMERIC,
    acdnt_time TIMESTAMP
);

-- 9. 전기차충전소 현황 (140-159)
CREATE TABLE IF NOT EXISTS city_ev_chargers (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    stat_nm VARCHAR(255),
    stat_id VARCHAR(50),
    stat_addr TEXT,
    stat_x NUMERIC,
    stat_y NUMERIC,
    stat_usetime VARCHAR(100),
    stat_parkpay VARCHAR(10),
    stat_limityn VARCHAR(1),
    stat_limitdetail TEXT,
    stat_kinddetail VARCHAR(100),
    charger_id VARCHAR(50),
    charger_type VARCHAR(50),
    charger_stat VARCHAR(50),
    statupddt TIMESTAMP,
    lasttsdt TIMESTAMP,
    lasttedt TIMESTAMP,
    nowtsdt TIMESTAMP,
    output NUMERIC,
    method VARCHAR(100)
);

-- 10. 따릉이 현황 (160-167)
CREATE TABLE IF NOT EXISTS city_sbike (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    sbike_spot_nm VARCHAR(255),
    sbike_spot_id VARCHAR(50),
    sbike_shared NUMERIC,
    sbike_parking_cnt INTEGER,
    sbike_rack_cnt INTEGER,
    sbike_x NUMERIC,
    sbike_y NUMERIC
);

-- 11. 기상특보 (193-199)
CREATE TABLE IF NOT EXISTS city_weather_alerts (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    warn_val VARCHAR(100),
    warn_stress VARCHAR(50),
    announce_time TIMESTAMP,
    command VARCHAR(50),
    cancel_yn VARCHAR(1),
    warn_msg TEXT
);

-- 12. 24시간 예보 (200-206)
CREATE TABLE IF NOT EXISTS city_weather_fcst (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    fcst_dt TIMESTAMP,
    temp NUMERIC,
    precipitation NUMERIC,
    precept_type VARCHAR(50),
    rain_chance NUMERIC,
    sky_stts VARCHAR(50)
);

-- 13. 문화행사 현황 (207-216)
CREATE TABLE IF NOT EXISTS city_cultural_events (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    event_nm TEXT,
    event_period TEXT,
    event_place TEXT,
    event_x NUMERIC,
    event_y NUMERIC,
    pay_yn VARCHAR(1),
    thumbnail TEXT,
    url TEXT,
    event_etc_detail TEXT
);

-- 14. 실시간 상권 현황 상세 (217-240)
CREATE TABLE IF NOT EXISTS city_commercial_details (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    
    -- 217-221. Summary (In each industry object)
    live_cmrcl_stts VARCHAR(50),
    area_cmrcl_lvl VARCHAR(50),
    area_sh_payment_cnt NUMERIC,
    area_sh_payment_amt_min NUMERIC,
    area_sh_payment_amt_max NUMERIC,
    
    -- 222-229. Industry Details
    rsb_lrg_ctgr VARCHAR(100),
    rsb_mid_ctgr VARCHAR(100),
    rsb_payment_lvl VARCHAR(50),
    rsb_sh_payment_cnt NUMERIC,
    rsb_sh_payment_amt_min NUMERIC,
    rsb_sh_payment_amt_max NUMERIC,
    rsb_mct_cnt INTEGER,
    rsb_mct_time VARCHAR(50),
    
    -- 230-240. Demographic Stats (In each industry object)
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

-- 15. 실시간 재난문자 (241-245)
CREATE TABLE IF NOT EXISTS city_disaster_msgs (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    dst_se_nm VARCHAR(100),
    emrg_step_nm VARCHAR(50),
    msg_cn TEXT,
    crt_dt TIMESTAMP
);

-- 16. 연합뉴스 (246-251)
CREATE TABLE IF NOT EXISTS city_news (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES city_master(id) ON DELETE CASCADE,
    yna_step_nm VARCHAR(50),
    yna_ttl TEXT,
    yna_cn TEXT,
    yna_ymd VARCHAR(50),
    yna_wrtr_nm VARCHAR(100)
);

COMMIT;

-- Indexing
CREATE INDEX IF NOT EXISTS idx_city_master_area_nm ON city_master(area_nm);
CREATE INDEX IF NOT EXISTS idx_city_master_created_at ON city_master(created_at);
