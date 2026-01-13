-- Seoul City Real-time City Data Schema
-- This schema stores real-time data from the Seoul City OpenAPI.

CREATE TABLE IF NOT EXISTS seoul_city_data (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 기본 정보 (Common Info)
    area_nm VARCHAR(255) NOT NULL,      -- 핫스팟 장소명
    area_cd VARCHAR(50),                -- 핫스팟 코드명
    
    -- 실시간 인구 현황 (REAL-TIME POPULATION)
    live_ppltn_stts VARCHAR(50),        -- 실시간 인구현황
    area_congest_lvl VARCHAR(50),       -- 장소 혼잡도 지표 (여유, 보통, 약간 붐빔, 붐빔)
    area_congest_msg TEXT,              -- 장소 혼잡도 지표 관련 메세지
    area_ppltn_min INTEGER,             -- 실시간 인구 지표 최소값
    area_ppltn_max INTEGER,             -- 실시간 인구 지표 최대값
    male_ppltn_rate NUMERIC,            -- 남성 인구 비율
    female_ppltn_rate NUMERIC,          -- 여성 인구 비율
    ppltn_rate_0 NUMERIC,               -- 0~10세 인구 비율
    ppltn_rate_10 NUMERIC,              -- 10대 실시간 인구 비율
    ppltn_rate_20 NUMERIC,              -- 20대 실시간 인구 비율
    ppltn_rate_30 NUMERIC,              -- 30대 실시간 인구 비율
    ppltn_rate_40 NUMERIC,              -- 40대 실시간 인구 비율
    ppltn_rate_50 NUMERIC,              -- 50대 실시간 인구 비율
    ppltn_rate_60 NUMERIC,              -- 60대 실시간 인구 비율
    ppltn_rate_70 NUMERIC,              -- 70대 실시간 인구 비율
    resnt_ppltn_rate NUMERIC,           -- 상주 인구 비율
    non_resnt_ppltn_rate NUMERIC,       -- 비상주 인구 비율
    ppltn_time TIMESTAMP,               -- 실시간 인구 데이터 업데이트 시간
    
    -- 인구 예측 현황 (POPULATION FORECAST)
    fcst_yn VARCHAR(1),                 -- 예측값 제공 여부 (Y/N)
    fcst_time TIMESTAMP,                -- 인구 예측 시점
    fcst_ppltn_min INTEGER,             -- 예측 실시간 인구 지표 최소값
    fcst_ppltn_max INTEGER,             -- 예측 실시간 인구 지표 최대값
    fcst_congest_lvl VARCHAR(50),       -- 장소 예측 혼잡도 지표
    
    -- 도로 소통 현황 (ROAD TRAFFIC STATUS)
    road_traffic_stts VARCHAR(50),      -- 도로소통현황
    road_traffic_spd NUMERIC,           -- 전체도로소통평균속도
    road_traffic_idx NUMERIC,           -- 전체도로소통평균현황 지수
    road_traffic_time TIMESTAMP,        -- 도로소통현황 업데이트 시간
    road_msg TEXT,                      -- 전체도로소통평균현황 메세지
    
    -- 날씨 현황 (WEATHER STATUS)
    weather_stts VARCHAR(50),           -- 날씨 현황
    temp NUMERIC,                       -- 기온
    sensible_temp NUMERIC,              -- 체감온도
    max_temp NUMERIC,                   -- 일 최고온도
    min_temp NUMERIC,                   -- 일 최저온도
    humidity NUMERIC,                   -- 습도
    wind_dirct VARCHAR(50),             -- 풍향
    wind_spd NUMERIC,                   -- 풍속
    precipitation NUMERIC,              -- 강수량
    precpt_type VARCHAR(50),            -- 강수형태
    pm25_index VARCHAR(50),             -- 초미세먼지지표
    pm25 NUMERIC,                       -- 초미세먼지농도
    pm10_index VARCHAR(50),             -- 미세먼지지표
    pm10 NUMERIC,                       -- 미세먼지농도
    air_idx VARCHAR(50),                -- 통합대기환경등급
    uv_index_lvl INTEGER,               -- 자외선지수 단계
    weather_time TIMESTAMP,             -- 날씨 데이터 업데이트 시간
    
    -- 상권 현황 (COMMERCIAL STATUS)
    area_cmrcl_lvl VARCHAR(50),         -- 장소 실시간 상권 현황
    cmrcl_time TIMESTAMP,               -- 실시간 상권 현황 업데이트 시간

    -- 원본 데이터 (JSON Storage)
    raw_data JSONB                       -- 전체 raw response 저장
);

-- Indexing for performance
CREATE INDEX idx_seoul_city_data_area_nm ON seoul_city_data(area_nm);
CREATE INDEX idx_seoul_city_data_created_at ON seoul_city_data(created_at);
CREATE INDEX idx_seoul_city_data_ppltn_time ON seoul_city_data(ppltn_time);
