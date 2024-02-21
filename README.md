# inventory_system
Inventory system for pre-made mysql database due for a school project.
Made by Kim André, Even and Simen.


## How to use
To use this software you need to create a config.yml file and put it in the project root directory.

config.yml should have the following syntax (update using your credentials): 
```yaml
# config.yaml


# Database information, input your credentials here before running in production!
database:
  user: your_db_user
  password: your_db_password
  host: your_db_host
  port: your_db_port
  name: your_db_name

  ```