from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from datetime import datetime


platforms = {
    "spotify": {"base_url": "https://spotifycharts.com/regional/"},
    "youtube": {"base_url": "https://charts.youtube.com/charts/TopSongs/"},
}


# Spotify stuff
async def get_regions_spotify(url):
    asession = AsyncHTMLSession()
    html = await asession.get(url)
    await html.html.arender(sleep=3)
    soup = BeautifulSoup(html.text, "html.parser")
    drop_down = soup.find_all(
        "div", {"class": "responsive-select", "data-type": "country"}
    )[0]
    countries = {}
    lists = drop_down.find_all("li")
    for l in lists:
        countries[l.text] = {
            "tag": l.attrs.get("data-value", None),
            "url": url + l.attrs.get("data-value", None),
        }

    return countries


async def get_country_spotify(url):
    final = []
    asession = AsyncHTMLSession()
    html = await asession.get(url)
    await html.html.arender(sleep=3)
    soup = BeautifulSoup(html.text, "html.parser")
    date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    for tr in soup.find("tbody").findAll("tr"):
        position = tr.find("td", {"class": "chart-table-position"}).text
        artist = tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist = artist.replace("by ", "").strip()
        title = tr.find("td", {"class": "chart-table-track"}).find("strong").text
        songid = tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid = songid.split("track/")[1]
        streams = tr.find("td", {"class": "chart-table-streams"}).text.replace(",", "")
        link = tr.find("a").get("href")
        img_link = tr.find("img").get("src")
        data_date = date

        final.append(
            {
                "position": position,
                "title": title,
                "artist": artist,
                "songid": songid,
                "url_date": data_date,
                "streams": streams,
                "link": link,
                "img_link": img_link,
            }
        )
    return final


# Youtube stuff
async def get_regions_youtube(url):
    asession = AsyncHTMLSession()
    html = await asession.get(url)
    await html.html.arender(timeout=15, sleep=3)
    soup = BeautifulSoup(html.html.raw_html, "html.parser")
    drop_down = soup.find_all("paper-dropdown-menu")[0]
    drop_down = drop_down.find_all("paper-item")
    countries = {}
    for c in drop_down:
        countries[c.attrs.get("aria-label")] = {
            "tag": c.attrs.get("option-id", None),
            "url": url + c.attrs.get("option-id", None),
        }
    return countries


async def get_country_youtube(url):
    final = []
    asession = AsyncHTMLSession()
    html = await asession.get(url)
    await html.html.arender(timeout=15, sleep=3)
    soup = BeautifulSoup(html.html.raw_html, "html.parser")
    date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    records = soup.find_all(class_="chart-table-row style-scope ytmc-chart-table")
    for record in records:
        record
        final.append(
            {
                "position": record.attrs.get("id"),
                "prev_position": record.find(
                    "div", {"class": "chart-table style-scope ytmc-chart-table"}
                ).span.text,
                "title": record.find(
                    "div", {"class": "ytmc-ellipsis-text style-scope"}
                ).span.text,
                "artist": record.find_all(
                    "div",
                    {
                        "class": "ytmc-artist-name clickable style-scope ytmc-artists-list",
                        "id": "ytmc-artists-list",
                    },
                )[1].text.strip(),
                "songid": record.attrs.get("track-video-id"),
                "url_date": date,
                "streams": record.find("div", {"class": "style-scope ytmc-chart-table"})
                .find("span")
                .text,
                "link": f"https://www.youtube.com/watch?v={record.attrs.get('track-video-id')}",
                "img_link": record.find(
                    "div",
                    {
                        "class": "chart-entry-thumbnail clickable style-scope ytmc-chart-table"
                    },
                ).img.attrs.get("src"),
            }
        )

    return final
