# insert your application KEY and SECRET
from bs4 import BeautifulSoup
import requests
import webbrowser
from linkedin import LinkedIn, LinkedInApi
import mongodb

database_ip = "52.208.8.144"
database_port = 27017
database_ofertas = "ofertas"
database_usuarios = "Users"
API_KEY = "776iq1i9wuca2b"
SECRET_KEY = "GYasmOX4Zgcjn9N2"

def conect_to_linkedin():
    li = LinkedIn(API_KEY, SECRET_KEY)
    token = li.getRequestToken(None)
    # prompt user in the web browser to login to LinkedIn and then enter a code that LinkedIn gives to the user
    auth_url = li.getAuthorizeUrl(token)
    webbrowser.open(auth_url)
    validator = input("Enter token: ")
    access_token = li.getAccessToken(token, validator)
    return li,access_token

def get_skills_linkedin(li,access_token):
    skills_list = []
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(public-profile-url)", access_token)
    soup = BeautifulSoup(response)
    public_url = soup.find('public-profile-url').string
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req=requests.request('GET',public_url,headers=headers)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'skill'}):
            skills = div.find_all('a')
            for skill in skills:
                skills_list.append(skill.get('title').lower())
    return skills_list

def get_email(li,access_token):
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(email-address)", access_token)
    soup = BeautifulSoup(response)
    email = soup.find('email-address').string
    return email

def get_estudios(li,access_token):
    estudios_list = []
    liapi = LinkedInApi(li)
    response = liapi.doApiRequest("https://api.linkedin.com/v1/people/~:(public-profile-url)", access_token)
    soup = BeautifulSoup(response)
    public_url = soup.find('public-profile-url').string
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req=requests.request('GET',public_url,headers=headers)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text)
        for div in html.find_all('li', {'class': 'school'}):
            schools = div.find_all('h5', {'class': 'item-subtitle'})
            for school in schools:
                school_name = school.find_all('span', {'class': 'translation'})
                for name in school_name:
                    print name.getText()
                    estudios_list.append(name.get('data-text-toggle').lower())
    return estudios_list


#def user_actualizacion_skills():
linkedin_conection,access_token = conect_to_linkedin()
skill_list = get_skills_linkedin(linkedin_conection,access_token)
email = get_email(linkedin_conection,access_token)
studios = get_estudios(linkedin_conection,access_token)
print studios
db_user = mongodb.get_db(database_ip, database_port, database_usuarios)

