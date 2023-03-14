import json
import random
jsonFile = "songs.json"
songsDir = "lyrics/"

def get_all_songs():
    songs = []
    with open(jsonFile,"r") as jFile:
        songsInfo = json.load(jFile)["songs"]

    for song in songsInfo:
        with open(songsDir + song["lyricsFile"],"r") as f:
            lines = [x for x in f.read().split("\n") if x != ""]
            songs.append({
                "ID": song["ID"],
                "name": song["name"],
                "lyrics": lines 
            })

    return songs

class Songs:
    def __init__(self) -> None:
        self.songs = get_all_songs()
        self.todays_song = None

    def get_random_lyric(self):
        """
        Gets two random lines from a random song
        """
        self.refresh_songs()
        song = self.songs[random.randint(0,len(self.songs)-1)]
        songLyric = song["lyrics"]
        lyricIndex = random.randint(0,len(songLyric)-2)
        
        self.todays_song = song["ID"]
        return " ".join(songLyric[lyricIndex:lyricIndex+2])
    
    def refresh_songs(self):
        """
        Fetches all songs from files
        """
        self.songs = get_all_songs()

    def get_answer(self):
        for song in self.songs:
            if song["ID"] == self.todays_song:
                return song