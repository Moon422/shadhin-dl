from shadhin_lib.album import Album

base_url = "https://coreapi.shadhinmusic.com/api/v5"

album = Album("203")
album.fetch_songs(base_url)
album.download_album(base_url)
