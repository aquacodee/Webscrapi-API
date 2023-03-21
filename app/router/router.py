from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from .helpers import (
    get_regions_spotify,
    get_regions_youtube,
    get_country_spotify,
    get_country_youtube,
    platforms,
)

platforms = {
    "spotify": {"base_url": "https://spotifycharts.com/regional/"},
    "youtube": {"base_url": "https://charts.youtube.com/charts/TopSongs/"},
}


router = APIRouter(tags=["Route"])


@router.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@router.get("/regions")
async def regions():
    spot_countries = await get_regions_spotify(platforms["spotify"]["base_url"])
    youtube_countries = await platforms["youtube"]["base_url"]
    return {"spotify_countries": spot_countries, "youtube_countries": youtube_countries}


@router.post("/country")
async def country(request: Request):
    r = await request.json()
    url = r["https://charts.youtube.com/charts/TopSongs/"]
    if "spotify" in url:
        top = await get_country_spotify(url)
        return {"status": "SUCCESS", "data": top}
    elif "youtube" in url:
        top = await get_country_youtube(url)
        return {"status": "SUCCESS", "data": top}
    else:
        return {"status": "FAILED", "msg": "url not recognized"}
