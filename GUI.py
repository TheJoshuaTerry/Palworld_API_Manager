import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel
import asyncio


class PalworldGUI:
    def __init__(self, root, api, server_name, whitelist):
        self.root = root
        self.api = api
        self.whitelist = whitelist
        self.root.title(server_name)
        self.root.geometry("600x400")

        tk.Label(root, text=server_name, font=("Arial", 16)).pack()

        self.status_frame = tk.Frame(root)
        self.status_frame.pack()
        tk.Label(self.status_frame, text="Server Status: ").pack(side=tk.LEFT)
        self.status_canvas = tk.Canvas(self.status_frame, width=20, height=20)
        self.status_canvas.pack(side=tk.LEFT)
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")

        tk.Button(root, text="Players", command=self.display_players_window).pack()

        self.broadcast_entry = tk.Entry(root, width=50)
        self.broadcast_entry.pack()
        tk.Button(root, text="Broadcast", command=self.send_broadcast).pack()

        tk.Button(root, text="Start Server", command=self.start_server).pack()
        tk.Button(root, text="Shutdown Server", command=self.shutdown_server).pack()

        self.output_area = scrolledtext.ScrolledText(root, width=50, height=10)
        self.output_area.pack()

        tk.Button(root, text="Statistics", command=self.display_statistics).pack()
        tk.Button(root, text="Metrics", command=self.display_metrics).pack()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.update_server_status()

    def start_server(self):
        self.api.start_server()
        messagebox.showinfo("Info", "Server started.")

    async def shutdown_server_async(self):
        if await self.api.shutdown_server(30, "Server shutting down in 10 seconds.") == 1:
            messagebox.showinfo("Info", "Server shutdown initiated.")
        else:
            messagebox.showinfo("Info", "Server shutdown not initiated.")

    def shutdown_server(self):
        self.loop.run_until_complete(self.shutdown_server_async())

    async def fetch_data(self, fetch_func, type):
        data = await fetch_func()
        if type == 'metrics':
            formatted_data = self.format_metrics(data)
        elif type == 'statistics':
            formatted_data = self.format_statistics(data)
        else:
            formatted_data = data
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, formatted_data)

    def display_players_window(self):
        self.loop.run_until_complete(self.show_players())

    async def show_players(self):
        players = await self.api.get_players()
        players = players.get('players')
        player_window = Toplevel(self.root)
        player_window.title("Players")
        # print(players)

        for index, player in enumerate(players):
            # print(player)
            frame = tk.Frame(player_window)
            frame.pack(fill=tk.X)

            details = (f"Name: {player['name']}\n"
                       f"Account: {player['accountName']}\n"
                       f"Player ID: {player['playerId']}\n"
                       f"Steam ID: {player['userId']}\n"
                       f"IP: {player['ip']}\n"
                       f"Ping: {player['ping']}\n"
                       f"Level: {player['level']}\n")
            tk.Label(frame, text=details, font=("Arial", 16), justify=tk.LEFT).pack(side=tk.LEFT)
            if player['userId'] not in self.whitelist:
                tk.Button(frame, text="Kick", command=lambda p=player['playerId']: self.kick_player(p)).pack(side=tk.RIGHT)
                tk.Button(frame, text="Ban", command=lambda p=player['playerId']: self.ban_player(p)).pack(side=tk.RIGHT)

    async def kick_player_async(self, player_id):
        await self.api.kick_players(player_id)
        messagebox.showinfo("Info", f"Player {player_id} kicked.")

    def kick_player(self, player_id):
        self.loop.run_until_complete(self.kick_player_async(player_id))

    async def ban_player_async(self, player_id):
        await self.api.ban_players(player_id)
        messagebox.showinfo("Info", f"Player {player_id} banned.")

    def ban_player(self, player_id):
        self.loop.run_until_complete(self.ban_player_async(player_id))

    def display_players(self):
        self.loop.run_until_complete(self.fetch_data(self.api.get_players, 'players'))

    def display_statistics(self):
        self.loop.run_until_complete(self.fetch_data(self.api.get_server_info, 'statistics'))

    def display_metrics(self):
        self.loop.run_until_complete(self.fetch_data(self.api.get_server_metrics, 'metrics'))

    def format_metrics(self, data):
        return (f"Current Player Number = {data.get('currentplayernum', 'N/A')}\n"
                f"Server FPS = {data.get('serverfps', 'N/A')}\n"
                f"Server Frame Time = {data.get('serverframetime', 'N/A')}\n"
                f"Days = {data.get('days', 'N/A')}\n"
                f"Max Player Number = {data.get('maxplayernum', 'N/A')}\n"
                f"Uptime = {data.get('uptime', 'N/A')}")

    def format_statistics(self, data):
        return (f"Server Version = {data.get('version', 'N/A')}\n"
                f"Server Name = {data.get('servername', 'N/A')}\n"
                f"Server Description = {data.get('description', 'N/A')}\n"
                f"World GUI ID = {data.get('worldguid', 'N/A')}\n")

    async def send_broadcast_async(self):
        message = self.broadcast_entry.get()
        await self.api.send_broadcast(message)
        messagebox.showinfo("Info", "Broadcast sent.")

    def send_broadcast(self):
        self.loop.run_until_complete(self.send_broadcast_async())

    async def check_server_status(self):
        try:
            data = await self.api.get_server_settings()
            if data:
                self.status_canvas.itemconfig(self.status_indicator, fill="green")
            else:
                self.status_canvas.itemconfig(self.status_indicator, fill="red")
        except:
            self.status_canvas.itemconfig(self.status_indicator, fill="red")

    def update_server_status(self):
        self.loop.run_until_complete(self.check_server_status())