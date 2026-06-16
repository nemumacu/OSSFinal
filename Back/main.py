from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="Anime Recommendation API")


with open("anime_data.json", "r", encoding="utf-8") as f:
    anime_db = json.load(f)


class UserPreferences(BaseModel):
    genres: List[str]
    styles: List[str]
    purposes: List[str]
    otaRate: str
    tag: Optional[str] = None


@app.post("/recommend")
def get_recommendations(prefs: UserPreferences):
    recommendations = []

    for anime in anime_db:
        
        if not anime["tag"] or anime["tag"] == [""] or anime["tag"] == []:
            continue

        
        anime_ota = int(anime["otaRate"][0])
        user_ota = int(prefs.otaRate)
        
        if anime_ota > user_ota:
            continue
            
        
        if prefs.tag and prefs.tag not in anime["tag"]:
            continue

        
        if not set(prefs.genres) & set(anime["genre"]):
            continue

       
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

    recommendations.sort(key=lambda x: x["score"], reverse=True)

  
    top_3_animes = recommendations[:3]
    
    if not top_3_animes:
        return {"status": "success", "message": "조건에 딱 맞는 애니메이션이 없습니다.", "recommendations": []}
    
    return {"status": "success", "recommendations": top_3_animes}
