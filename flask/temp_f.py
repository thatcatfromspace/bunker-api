from flask import Flask, request, render_template,jsonify
from bs4 import BeautifulSoup
import requests
import pandas as pd
# import TableIt

app = Flask(__name__)

def return_attedence(username,pwd):
    session = requests.Session()
    r = session.get('https://ecampus.psgtech.ac.in/studzone2/')

    # print ("STATUS 1:",r.status_code)
    # print (r.history)
    # print ("REDIRECT 1: ",r.url)

    loginpage = session.get(r.url)

    soup = BeautifulSoup(loginpage.text,"html.parser")

    viewstate = soup.select("#__VIEWSTATE")[0]['value']
    eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
    viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]['value']


    item_request_body  = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategen,
        '__EVENTVALIDATION': eventvalidation,
        'rdolst': 'S',
        'txtusercheck': username,
        'txtpwdcheck': pwd,
        'abcd3': 'Login',
    }
    response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})

    if response.status_code == 200:

        defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'
    
        page = session.get(defaultpage)
        soup = BeautifulSoup(page.text,"html.parser")
    
        data = []
        column = []
        table = soup.find('table', attrs={'class':'cssbody'})
    
        try:
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty val
        
            # df = pd.DataFrame(data, columns=column)
            # res = df.to_json(orient="split")
            # return res
            return data
        except:
            return "Invalid password"
    else:
        return "Try again after some time"
    
    



# @app.route('/',methods=['GET'])
# def home():
#     return render_template('home.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        username = request.form.get("fname")
        pwd = request.form.get("lname")
        # print(TableIt.printTable(return_attedence(username,pwd)))
        return str((return_attedence(username,pwd)))
        
    return render_template("home.html")





if __name__=="__main__":
    app.run(host='0.0.0.0',port=4000,debug=True)