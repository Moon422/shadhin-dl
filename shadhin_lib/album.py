from datetime import datetime
from pathlib import Path
import requests

from shadhin_lib.song import Song

class Album:
    def __init__(self, album_id: str):
        self.album_id = album_id
    
    def fetch_songs(self, base_url: str):
        url = f"{base_url}/Album/GetAlbumContentV6?id={self.album_id}"

        response = requests.get(url)

        if response.ok:
            songs_json = response.json()["data"]
            self.songs = [Song(song["ContentID"], song["image"], song["title"], song["PlayUrl"], song["ArtistName"], song["duration"], song["labelname"], datetime.strptime(song["releaseDate"], '%Y-%m-%dT%H:%M:%SZ'), song["AlbumName"]) for song in songs_json]
            self.songs.sort(key=lambda s: s.content_id)
            return True
        else:
            return False
        
    def download_album(self, base_url):
        output = Path.home() / "Downloads" / self.songs[0].album_name
        
        if not Path.exists(output):
            Path.mkdir(output)

        with requests.get(self.songs[0].image) as img_res:
            if img_res.ok:
                with open(output / "cover.jpg", "wb") as img_file:
                    img_file.write(img_res.content)
        
        for idx, song in enumerate(self.songs):
            song_file = song.download(base_url)
            filename = output / f"{idx + 1} - {song.title}.mp3"
            Path.rename(song_file, filename)
        
