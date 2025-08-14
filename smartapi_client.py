import json, time, threading, websocket

class SmartWSClient:
    """
    Minimal wrapper to connect to Angel One SmartAPI websocket.
    Expects an Access Token string. Uses a default WS_URL which may need updating.
    """
    def __init__(self, access_token, api_key=None):
        self.access_token = access_token
        self.api_key = api_key or ""
        # NOTE: endpoint may change; update if connection fails.
        self.WS_URL = "wss://apia2.tradestation.angelbroking.com/SmartAPIRealtimeService/"
        self.ws = None
        self.running = False
        self.tick_callback = None

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
        except Exception:
            return
        tick = {}
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], dict):
                d = data["data"]
                tick['timestamp'] = d.get('timestamp') or d.get('time') or time.time()
                tick['ltp'] = d.get('ltp') or d.get('last_traded_price') or d.get('ltPrice') or d.get('ltp')
                tick['change'] = d.get('change') or d.get('pChange') or ""
                tick['raw'] = d
            else:
                tick['raw'] = data
        if self.tick_callback and callable(self.tick_callback):
            try:
                self.tick_callback(tick)
            except Exception:
                pass

    def _on_error(self, ws, error):
        print("WebSocket error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed", close_status_code, close_msg)
        self.running = False

    def _on_open(self, ws):
        print("WebSocket opened, sending auth/subscription if required")
        auth_msg = {
            "action": "auth",
            "params": {"token": self.access_token, "api_key": self.api_key}
        }
        try:
            ws.send(json.dumps(auth_msg))
        except Exception:
            pass
        try:
            sub_msg = {"action": "subscribe", "params": {"symbols": ["NIFTY 50"]}}
            ws.send(json.dumps(sub_msg))
        except Exception:
            pass

    def connect_and_subscribe_nifty(self, on_tick_callback=None):
        self.tick_callback = on_tick_callback
        self.running = True
        def run():
            self.ws = websocket.WebSocketApp(self.WS_URL,
                                             on_open=self._on_open,
                                             on_message=self._on_message,
                                             on_error=self._on_error,
                                             on_close=self._on_close)
            self.ws.run_forever()
        t = threading.Thread(target=run, daemon=True)
        t.start()
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False