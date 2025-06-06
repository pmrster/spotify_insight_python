
class TransformSpotifyResponse:
    def __init__(self, data):
        self.data = data

    def transform_top_track_data(self):
        top_track_list = []
        counter = 0
        
        for item in self.data["items"]:
            counter += 1
            # print(item)
            top_track_list.append(
                {
                "no" : counter,
                "track_name" : item["name"],
                "artist_name" : item["artists"][0]["name"],
                "album_name" : item["album"]["name"],
                "album_img" : item["album"]["images"][1]["url"],
                "album_release_date" : item["album"]["release_date"],
                "track_preview_player" : item["preview_url"],
                "track_duration_ms" : convert_ms_to_mmss(item["duration_ms"]),
                "track_id" : item["id"]
                
            })
        
            
            ## ไม่มี track genres ต้องใช้ artist genres แทน
        print("transformed top track: ", top_track_list)
        
        return top_track_list
            
            
    def transform_top_artist(self):
        top_artist_list = []
        counter = 0
        
        for item in self.data["items"]:
            counter += 1
            # print(item)
            top_artist_list.append(
                {
                "no" : counter,
                "artist_name" : item["name"],
                "artist_genres" : item["genres"],
                "artist_img" : item["images"][1]["url"],
                "artist_id" : item["id"]
                
            })
        
        print("transformed top artist : ", top_artist_list)
        
        return top_artist_list
    
    
    def transform_saved_tracks(self):
        saved_track_list = []
        counter = 0
        
        for item in self.data["items"]:
            counter += 1
            # print(item)
            saved_track_list.append({
                "no" : counter,
                "added_at" : item["added_at"],
                "track_name" : item["track"]["name"],
                "track_id" : item["track"]["id"],
                "artists": [i["name"] for i in item["track"]["artists"]],
                "duration_ms": convert_ms_to_mmss(item["track"]["duration_ms"]),
                "track_uri" : item["track"]["uri"],
                "album_img" : item["track"]["album"]["images"][1]["url"],
                
            })
        
        print("transformed saved tracks : ", saved_track_list)
        
        return saved_track_list



def convert_ms_to_mmss(duration_ms):
    seconds = duration_ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"
