import csv

class LoginTestDataManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = []
        self._read_data()

    def _read_data(self):
        """อ่านข้อมูลจาก CSV แล้วเก็บไว้ใน list ของ dict"""
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            self._data = [row for row in reader]

    def get_all(self):
        """คืนค่าทุกชุดข้อมูลในรูปแบบ list ของ dict"""
        return self._data

    def get_by_index(self, index):
        """คืนค่าชุดข้อมูลตาม index (ใช้กรณีอยากรันเฉพาะเคสบางเคส)"""
        return self._data[index]

    def __len__(self):
        """ให้สามารถใช้ len(data_manager) ได้"""
        return len(self._data)
