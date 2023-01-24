import requests_html
from rich import console
import webbrowser
import nltk
from prettytable import PrettyTable
from colorama import init 
from termcolor import colored
import sys,os
from toks import STokens

init()
ses = requests_html.HTMLSession()
language = 'en'
console = console.Console()
# search_term = console.input("Insert the search term: ")
def TOK(text):
    s = nltk.word_tokenize(str(text).lower())
    ss = nltk.pos_tag(s)
    s = [token for (token, tag) in ss if (len(token) > 1) and ((tag == 'CD') or (tag == 'NN') or (tag == 'NNP') or (tag == 'VBG') or (tag =='VBZ') or (tag =='JJ') or (tag =='WP')or (tag =='RB'))]
    s = [token.replace('.', '').replace('\'','').replace('=','').lower() for token in s]
    return (s)

def get_details_percent(link_no):
    try:
        res_det = ses.get(urls[int(link_no)][1])
    except : return(-1,-1)
    results_det = res_det.html.find('body')[0]
    try: 
        chk_list = [k in str(results_det.text) for k in s]
        chk_true = [k for k in chk_list if k == True]
        chk_percent = int(len(chk_true) / len(chk_list) * 100)
        chk_list_stok = [k in results_det.text for k in STokens]
        chk_true_stok = [k for k in chk_list_stok if k == True]
        chk_percent_stok = int(len(chk_true_stok) / len(chk_list_stok) * 100)
    except: return(-1,-1) 
    # print (chk_list_stok , chk_true_stok)
    return (chk_percent,chk_percent_stok)

ser =  str(' '.join( sys.argv[1:]))
url = u'https://www.google.com/search?q=' + ser

print ( colored('searching for ','light_grey') , colored( ser ,'light_yellow' ) )
# url = f'https://{language}.wikipedia.org/w/index.php?search={search_term}&fulltext=1&ns0=1'
res = ses.get(url)


s = TOK(ser)
results = res.html.find('body')[0].find('span')
desc = []
for num,result in enumerate(results):
    if any([k in str(result.text) for k in s]):
        if len(str(result.text)) > 90 :
            if not(str(result.text)  in desc): 
                desc.append(result.text)
                print (colored(str(result.text),'light_yellow','on_black'))

urls = ['']
descs = ['']
table = PrettyTable()
table.field_names = ['#', 'Link', '% found','% leared'] #,'spider found %' , 'spider learn %']
x = 0
results = res.html.find('a')
for num,result in enumerate(results):
    if (str(result.links).startswith('{\'https://')) :
         if not("google.com" in str(result.links)):
             x+=1
             aref = str(result.find('a')[0].links)[2:-2]
             adesc = str(result.text).split(aref[0:5])[0]
             chk_str = TOK ( aref.replace("-"," ").lower() + " " + adesc.lower())
             chk_list = [k in chk_str for k in s]
             chk_true = [k for k in chk_list if k == True]
             chk_percent = int(len(chk_true) / len(chk_list) * 100)
             chk_list_stok = [k in chk_str for k in STokens]
             chk_true_stok = [k for k in chk_list_stok if k == True]
             chk_percent_stok = int(len(chk_true_stok) / len(chk_list_stok) * 100)             
             # print (x, str(result.find('a')[0].links)[2:-2],"  ", str(chk_percent) , "%")
             # print (x, str(results[num].text))
             # print (chk_str , chk_list , chk_true , chk_percent)
             # chk_percent_det, chk_percent_stok_det = get_details_percent(x)
             urls.append([x,aref,chk_percent,chk_percent_stok])
             if len(aref) > 100 : aref = aref[0:100]
             descs.append(adesc.strip())
             if len (adesc.replace('ي','').strip()) > 100 : adesc = adesc [0:100]
             table.add_row([x, colored(aref,'light_magenta'), colored(str(chk_percent) + "%",'green'),colored(str(chk_percent_stok) + "%",'green') ,])
             # colored(str(chk_percent_det) + "%",'red'),colored(str(chk_percent_stok_det) + "%",'red')])
             table.add_row(["",colored(adesc,'yellow') ,"",""])

print (table)
go_web = 100
while go_web != 0:
    go_web = console.input("enter link number to look for, 0 to exit, 99 to spider search : ")
    if int(go_web) == 0 : sys.exit()

    if int(go_web) == 99 :
        table = PrettyTable()
        table.field_names = ['#', 'Link', '% found','% leared','spider found %' , 'spider learn %']
        x = 0
        for x,link in enumerate(urls):
                    if x == 0 : continue   
                    chk_percent_det, chk_percent_stok_det = get_details_percent(x)
                    os.system("cls")
                    urls[x]= urls[x] + [chk_percent,chk_percent_stok]
                    print (desc)
                    if len(link[1]) > 100 : link[1] = link[1][0:100]
                    if len(descs[x]) > 100 : descs[x] = descs[x][0:100].replace('ي','').strip()
                    table.add_row([x, colored(link[1],'light_magenta'), colored(str(urls[x][2]) + "%",'green'),colored(str(urls[x][3]) + "%",'green') ,
                    colored(str(chk_percent_det) + "%",'red'),colored(str(chk_percent_stok_det) + "%",'red')])
                    table.add_row(["",colored(descs[x],'yellow') ,"","",'',''])
                    print (table)

    else : 
        webbrowser.open(urls[int(go_web)][1])





