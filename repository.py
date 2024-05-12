import urequests # type: ignore

class Station:
    def __init__(self, api_url, station_name, api_key, direction):
        self.api_url = api_url
        self.query = "?$filter=stationLocation eq '{station}'".format(station = station_name).replace(" ", "%20")
        self.direction = direction
        self.api_key = api_key
        self.trams = []
        self.message = ""

    def set_destination(self, direction):
        self.direction = direction

    def get(self):
        response = urequests.get(self.api_url + self.query, headers = { "Ocp-Apim-Subscription-Key": self.api_key })
        data = response.json()
        response.close()

        trams = data["value"]
        filtered_trams = [tram for tram, tram in enumerate(trams) if tram["Direction"] == self.direction]

        trams = filtered_trams[0]
        self.trams = []

        self.message = trams["MessageBoard"]

        if trams["Dest0"]: self.trams.append({
            "destination": trams["Dest0"],
            "wait": trams["Wait0"],
            "status": trams["Status0"]
        })
            
        if trams["Dest1"]: self.trams.append({
            "destination": trams["Dest1"],
            "wait": trams["Wait1"],
            "status": trams["Status1"]
        })

        if trams["Dest2"]: self.trams.append({
            "destination": trams["Dest2"],
            "wait": trams["Wait2"],
            "status": trams["Status2"]
        })

