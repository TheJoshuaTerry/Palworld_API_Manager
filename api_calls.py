import requests
import json
import subprocess
import time


class PalworldAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url + "/v1/api"
        self.auth = (username, password)


    async def get_server_info(self):
        url = f"{self.base_url}/info"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def get_players(self):
        url = f"{self.base_url}/players"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def get_server_settings(self):
        url = f"{self.base_url}/settings"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def get_server_metrics(self):
        url = f"{self.base_url}/metrics"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def save_server(self):
        url = f"{self.base_url}/save"
        response = requests.post(url, auth=self.auth)
        response.raise_for_status()
        await self.send_broadcast("Server has been saved")
        return 1

    async def send_broadcast(self, message):
        url = f"{self.base_url}/announce"
        payload = {"message": message}
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        # return response.json()

    async def kick_player(self, playerID):
        payload = json.dumps({
            "userid": playerID,
            "message": "You are kicked."
        })
        url = f"{self.base_url}/kick"
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def ban_player(self, playerID):
        payload = json.dumps({
            "userid": playerID,
            "message": "You are banned."
        })
        url = f"{self.base_url}/ban"
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def unban_player(self, playerID):
        payload = json.dumps({
            "userid": playerID
        })
        url = f"{self.base_url}/unban"
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()

    async def shutdown_server(self, waittime, message):
        payload = json.dumps({
            "waittime": waittime,
            "message": message
        })
        headers = {
            'Content-Type': 'application/json'
        }
        if await self.save_server() == 1:
            url = f"{self.base_url}/shutdown"
            print(url)

            response = requests.request("POST", url, headers=headers, data=payload)
            return 1

        else:
            await self.send_broadcast("Server hasn't been  and will not shut down")
            return 0
        # return response.json()

    async def stop_server(self):
        url = f"{self.base_url}/stop"
        response = requests.post(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def send_command(self, command):
        url = f"{self.base_url}/command"
        payload = {"command": command}
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def start_server(self):
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "start_server.ps1"])
