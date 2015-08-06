import requests

server_path = r'http://127.0.0.1:5000'
users = {
    "admin": "tomo_admin",
    "user": "tomo_user",
    "hacker": "admin"
}


def main():
    for user_name in users:
        r = requests.get(server_path, auth=(user_name, users[user_name]))
        print r.text


if __name__ == '__main__':
    main()
