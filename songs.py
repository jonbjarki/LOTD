import json
import random
JSONFILE = "songs.json"
LYRICSDIR = "lyrics/"


def get_all_songs():
    songs = []
    with open(JSONFILE, "r", encoding="UTF-8") as jFile:
        songsInfo = json.load(jFile)["songs"]

    for song in songsInfo:
        with open(LYRICSDIR + song["lyricsFile"], "r", encoding="UTF-8") as f:
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
        self.todays_song = self.get_todays_song()
        self.lyric = self.get_lyric()

    def get_random_lyric(self):
        """
        Gets two random lines from a random song
        """
        self.refresh_songs()
        song = self.songs[random.randint(0, len(self.songs)-1)]
        songLyric = song["lyrics"]
        lyricIndex = random.randint(0, len(songLyric)-2)
        todaysLyric = " ".join(songLyric[lyricIndex:lyricIndex+2])

        self.set_todays_song(song["ID"])
        self.set_lyric(todaysLyric)
        return todaysLyric

    def get_data(self) -> dict:
        """
        Gets data from json file
        """
        with open(JSONFILE, "r") as f:
            return json.load(f)

    def set_data(self, data: dict) -> None:
        """
        Uploads new data to json file
        """
        with open(JSONFILE, "w") as f:
            json.dump(data, f, indent=2)

    def set_todays_song(self, songID):
        data = self.get_data()
        data["todaysSong"] = songID
        self.todays_song = songID
        self.set_data(data)

    def get_todays_song(self):
        data = self.get_data()["todaysSong"]

    def get_lyric(self):
        return self.get_data()["lyric"]

    def set_lyric(self, lyric):
        data = self.get_data()
        data["lyric"] = lyric
        self.set_data(data)

    def refresh_songs(self):
        """
        Fetches all songs from files
        """
        self.songs = get_all_songs()

    def get_answer(self):
        for song in self.songs:
            if song["ID"] == self.todays_song:
                return song
