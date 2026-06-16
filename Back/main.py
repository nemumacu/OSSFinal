from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="Anime Recommendation API")

# 1. 데이터 불러오기
with open("anime_data.json", "r", encoding="utf-8") as f:
    anime_db = json.load(f)

# 2. 프론트엔드에서 넘어오는 사용자 입력 데이터 구조
class UserPreferences(BaseModel):
    genres: List[str]
    styles: List[str]
    purposes: List[str]
    otaRate: str
    tag: Optional[str] = None

# 3. 추천 로직 엔드포인트
@app.post("/recommend")
def get_recommendations(prefs: UserPreferences):
    recommendations = []

    for anime in anime_db:
        # [절대 지표 0] 태그가 아예 없는 작품은 무조건 튕겨냄
        if not anime["tag"] or anime["tag"] == [""] or anime["tag"] == []:
            continue

        # 🔥 [핵심 수정: 절대 지표 1] 씹덕지수(항마력) 상한선 필터링
        # 애니메이션의 지수가 내가 선택한 지수보다 '크면(높으면)' 내보냄(탈락)
        anime_ota = int(anime["otaRate"][0])
        user_ota = int(prefs.otaRate)
        
        if anime_ota > user_ota:
            continue
            
        # [절대 지표 2] 태그(tag) 필터링 (선택했을 경우에만)
        if prefs.tag and prefs.tag not in anime["tag"]:
            continue

        # [절대 지표 3] 장르 필터링 (최소 1개는 겹쳐야 함)
        if not set(prefs.genres) & set(anime["genre"]):
            continue

        # --- 여기까지 살아남은 작품만 점수 계산 ---
        score = 0
        
        for genre in prefs.genres:
            if genre in anime["genre"]:
                score += 1
                
        for style in prefs.styles:
            if style in anime["style"]:
                score += 2
                
        for purpose in prefs.purposes:
            if purpose in anime["purpose"]:
                score += 2
            
        if score > 0:
            recommendations.append({
                "title": anime["title"],
                "score": score,
                "genre": anime["genre"],
                "tag": anime["tag"]
            })

    # 점수가 가장 높은 순으로 정렬 (내림차순)
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # 상위 3개만 반환
    top_3_animes = recommendations[:3]
    
    if not top_3_animes:
        return {"status": "success", "message": "조건에 딱 맞는 애니메이션이 없습니다.", "recommendations": []}
    
    return {"status": "success", "recommendations": top_3_animes}