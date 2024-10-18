from datetime import datetime, timedelta


class Clock():
    
    def __init__(self) -> None:
        self.timestamps: list[dict[str, str | datetime]] = []
    
    def add_timestamp(self, label:str) -> None:
        timestamp = {'time': datetime.now(), 'label':label}
        self.timestamps.append(timestamp)
        
    def time_since_last(self, label: str) -> timedelta | None:
        for timestamp in reversed(self.timestamps):
            if timestamp['label'] == label:
                time_diff = datetime.now() - timestamp['time']
                return time_diff
        return None