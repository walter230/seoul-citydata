import os
from dotenv import load_dotenv

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
    
    # Target Areas (Cleaned & Deduplicated)
    TARGET_AREAS = [
        "서대문독립공원", "뚝섬한강공원", "광나루한강공원", "이촌한강공원", "청계산",
        "구로역", "양화한강공원", "월드컵공원", "가산디지털단지역", "충정로역",
        "서울식물원·마곡나루역", "연신내역", "잠실한강공원", "보라매공원", "망원한강공원",
        "서리풀공원·몽마르뜨공원", "난지한강공원", "대림역", "노량진", "DMC(디지털미디어시티)",
        "응봉산", "동대문역", "반포한강공원", "김포공항", "신도림역",
        "총신대입구(이수)역", "사당역", "구로디지털단지역", "발산역", "서울 암사동 유적",
        "강서한강공원", "장한평역", "여의도한강공원", "교대역", "양재역",
        "고척돔", "잠원한강공원", "안양천", "노들섬", "삼각지역",
        "군자역", "가락시장", "어린이대공원", "쌍문역", "장지역",
        "서촌", "동대문 관광특구", "여의도", "남산공원", "서울역",
        "청량리 제기동 일대 전통시장", "창덕궁·종묘", "선릉역", "서울숲공원", "덕수궁길·정동길",
        "회기역", "뚝섬역", "홍제폭포", "성신여대입구역", "서울대입구역",
        "경복궁", "신논현역·논현역", "역삼역", "신촌·이대역", "천호역",
        "왕십리역", "종로·청계 관광특구", "건대입구역", "창동 신경제 중심지", "잠실종합운동장",
        "청담동 명품거리", "고속터미널역", "북촌한옥마을", "성수카페거리", "강남역",
        "광화문광장", "합정역", "신림역", "아차산", "미아사거리역",
        "가로수길", "신정네거리역", "올림픽공원", "여의서로", "용산역",
        "용리단길", "청와대", "강남 MICE 관광특구", "국립중앙박물관·용산가족공원", "오목교역·목동운동장",
        "이태원 관광특구", "광화문·덕수궁", "혜화역", "수유역", "서울대공원",
        "잠실 관광특구", "잠실롯데타워 일대", "잠실역", "영등포 타임스퀘어", "북서울꿈의숲",
        "고덕역", "송리단길·호수단길", "명동 관광특구", "홍대 관광특구", "잠실새내역",
        "이태원역", "서울광장", "보신각", "연남동", "DDP(동대문디자인플라자)",
        "북창동 먹자골목", "해방촌·경리단길", "익선동", "인사동", "남대문시장",
        "광장(전통)시장", "홍대입구역", "압구정로데오거리", "신촌 스타광장", "이태원 앤틱가구거리",
        "당산역", "동대문역사문화공원역", "명동역", "성수역", "신촌역", 
        "이수역", "잠실나루역", "종각역", "종로3가역", "충무로역", 
        "덕수궁 돌담길"
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
