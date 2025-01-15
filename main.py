import asyncio
import json
from api_calls import PalworldAPI


async def main():
   # Load the JSON file
   with open('auth.json', 'r') as file:
      auth_data = json.load(file)
   server_url = auth_data.get("server")
   username = auth_data.get("username")
   password = auth_data.get("password")
   api = PalworldAPI(server_url, username, password)

   server_info = await api.get_server_info()
   print("Server Info:", server_info)


if __name__ == "__main__":
   asyncio.run(main())