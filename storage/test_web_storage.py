import requests
from pprint import pprint
server_url = r'http://127.0.0.1:5000'
server_paths_get = ['/', '/test/', '/phantoms', '/phantoms/611']


users = {
    "admin": "tomo_admin",
    "user": "tomo_user",
    "hacker": "admin"
}


def main():
    for user_name in users:
        for server_path in server_paths_get:
            r = requests.get(server_url + server_path,
                             auth=(user_name, users[user_name])
                             )
            res = {'server_path': server_path,
                   'user_name': user_name,
                   'code': r.status_code,
                   'text': r.text
                   }
            pprint(res['code'])

    for user_name in users:
        r = requests.post(server_url + '/upload',
                          files={'file': (user_name + '.txt', user_name)},
                          # headers={'content-type': 'multipart/form-data'},
                          auth=(user_name, users[user_name])
                          )
        print r.text
        res = {'server_path': '/upload',
               'user_name': user_name,
               'code': r.status_code,
               'text': r.text
               }
        pprint(res)

if __name__ == '__main__':
    main()
