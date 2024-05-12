import urequests # type: ignore

class Station:
    def __init__(self, api_url, station_name, api_key, direction):
        self.api_url = api_url
        self.station_name = station_name
        self.query = "?$filter=stationLocation eq '{station}'".format(station = station_name).replace(" ", "%20")
        self.direction = direction
        self.api_key = api_key
        self.last_update = ""

    def set_destination(self, direction):
        self.direction = direction

    def get(self):
        response = urequests.get(self.api_url + self.query, headers = { "Ocp-Apim-Subscription-Key": self.api_key })
        data = response.json()
        response.close()

        trams_data = data["value"]
        filtered_trams = [tram for tram, tram in enumerate(trams_data) if tram["Direction"] == self.direction]

        trams_data = filtered_trams[0]
        if trams_data["LastUpdated"] != self.last_update:
            self.last_update = trams_data["LastUpdated"]
            trams = []

            message_data = trams_data["MessageBoard"]
            message = message_data if message_data != "<no message>" else "Displaying {direction} trams for {station}".format(direction=self.direction, station=self.station_name)
            
            if trams_data["Dest0"]: trams.append({
                "destination": trams_data["Dest0"],
                "wait": trams_data["Wait0"],
                "status": trams_data["Status0"]
            })
                
            if trams_data["Dest1"]: trams.append({
                "destination": trams_data["Dest1"],
                "wait": trams_data["Wait1"],
                "status": trams_data["Status1"]
            })

            if trams_data["Dest2"]: trams.append({
                "destination": trams_data["Dest2"],
                "wait": trams_data["Wait2"],
                "status": trams_data["Status2"]
            })
                
            return {
                "trams": trams,
                "message": message
            }
                
        return {
            "trams": [],
            "message": ""
        }

