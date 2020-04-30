import configparser
from pathlib import Path


class Config:
    def __init__(self):
        config_file = configparser.ConfigParser()
        config_path = Path("./config/config.ini")
        config_file.read(config_path)
        self.player_main_path = Path(config_file.get("PLAYER", "main_path"))
        self.player_sub_path = Path(config_file.get("PLAYER", "sd_path"))
        self.backup_path = Path(config_file.get("BACKUP", "path"))

    def update_location(self):
        pass


if __name__ == "__main__":
    cf = Config()
    print(cf.player_main_path)
    print(cf.player_sub_path)
    print(cf.backup_path)
