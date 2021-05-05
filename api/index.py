import requests
from bs4 import BeautifulSoup
from re import search
from flask import Flask ,jsonify,request

app = Flask(__name__)
app.url_map.strict_slashes = False

def findDawnloadUrl(link):
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content,features='lxml')
    articals = soup.find_all('a',class_="typo_large typo_green typo_rounded")
    for anc in articals:
        return {'durl':anc['href']}

def getNotesAndBooks(pageNo):
    url = f'https://freebiesui.com/page/{pageNo}/'

    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content,features='lxml')
    articals = soup.find_all('article')
    complete_json = []
    data = []
    page_no = []
    for l in soup.find_all('a', class_='page-numbers' ):
        if(l.text!=''):
            page_no.append(l.text)

    for item in articals:
        data.append(
            {
                'name':item.find('h4').text,
                'categories':item.find('span', class_='categories' ).text,
                # 'dauwnloadurl':findDawnloadUrl(item.find('a' )['href']),
                'imgurl':item.find('img' )['src'],
                'url':item.find('a' )['href'],
            }
        )
    complete_json.append({'data':data,'pages':page_no})
    return complete_json



@app.route('/', methods=['GET'])
def home_page():
    query_parameters = request.args
    # return "Welcome to https://freebiesui.com/ unofficial API"
    q = query_parameters.get('q',default=1)
    print(q)
    return jsonify(findDawnloadUrl(q))
# http://127.0.0.1:5000/?q=https://freebiesui.com/illustrator-freebies/12-tech-free-icons-ai

@app.route('/<query>')
def home(query):
    

    return jsonify(getNotesAndBooks(query))
# http://127.0.0.1:5000/1

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404    

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
    