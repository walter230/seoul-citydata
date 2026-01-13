import os
from dotenv import load_dotenv

# Load environment variables
# Try loading from project root first, then from Airflow root
load_dotenv()
if not os.getenv("SEOUL_API_KEY"):
    load_dotenv("/home/airflow-dev/Apache_Airflow/.env")

class Config:
    """Project Configuration Class"""
    
    # API Settings
    SEOUL_API_KEY = os.getenv("SEOUL_API_KEY")
    SEOUL_API_BASE_URL = "http://openapi.seoul.go.kr:8088"
    
    # Supabase Settings
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Target Areas (Example list, can be expanded)
    # 서울시 주요 120개 장소 중 일부 예시
    TARGET_AREAS = [
        "광화문·덕수궁",
        "경복궁·서촌마을",
        "명동·남대문·북창동",
        "동대문관광특구",
        "이태원 관광특구",
        "가로수길·세로수길",
        "강남 MICE 관광특구",
        "잠실 관광특구",
        "홍대 관광특구",
        "서울식물원",
        "여의도"
    ]

    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        if not cls.SEOUL_API_KEY:
            raise ValueError("SEOUL_API_KEY is not set in .env")
        if not cls.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is not set in .env")
        if not cls.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is not set in .env")
