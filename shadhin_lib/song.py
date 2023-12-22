from pathlib import Path
import requests
from datetime import datetime


class Song:
    def __init__(self, content_id, image, title, play_url, artist_name, duration, label_name, release_date, album_name):
        self.content_id = content_id
        self.image = image.replace("<$size$>", "300")
        self.title = title
        self.play_url = play_url
        self.artist_name = artist_name
        self.duration = duration
        self.label_name = label_name
        self.release_date = release_date
        self.album_name = album_name
    
    def download(self, base_url: str):
        url = base_url + "/streaming/getpth?ptype=S&type=null&ttype=null&name=" + self.play_url
        
        filename = Path.home() / "Downloads" / f"{self.title}.mp3"

        with requests.get(url) as music_response:
            music_url = music_response.json()["Data"]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
            }

            with requests.get(music_url, headers=headers, stream=True) as dl_response:
                file_size = int(dl_response.headers['Content-Length'])

                if file_size >= 1_000_000:
                    file_size /= 1_000_000
                    print(f"Downloading {self.title}, size: {file_size:.2f} Mega Bytes")
                elif file_size >= 1000:
                    file_size /= 1000
                    print(f"Downloading {self.title}, size: {file_size:.2f} Kilo Bytes")
                else:
                    print(f"Downloading {self.title}, size: {file_size:.2f} Bytes")


                with open(filename, mode="wb") as file:
                    for chunk in dl_response.iter_content(chunk_size=10240):
                        file.write(chunk)
                
        print("Download complete")
        
        return filename
