import yaml, tkinter

with open("config.yml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

DB_USER = config["database"]["user"]
DB_PASSWORD = config["database"]["password"]
DB_HOST = config["database"]["host"]
DB_PORT = config["database"]["port"]
DB_NAME = config["database"]["name"]

print(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, sep="\n")