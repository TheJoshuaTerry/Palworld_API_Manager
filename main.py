import asyncio
import tkinter as tk
import json
from api_calls import PalworldAPI
from GUI import PalworldGUI


if __name__ == "__main__":
   with open('auth.json', 'r') as file:
      auth_data = json.load(file)
   with open('serverInfo.json', 'r') as file:
      server_data = json.load(file)
   with open('whitelist.json', 'r') as file:
      whitelist_data = json.load(file)
   server_url = auth_data.get("server")
   username = auth_data.get("username")
   password = auth_data.get("password")
   server_name = server_data.get("name")
   whitelist = whitelist_data.get("whitelist")
   api = PalworldAPI(server_url, username, password)
   root = tk.Tk()
   gui = PalworldGUI(root, api, server_name, whitelist)
   root.mainloop()