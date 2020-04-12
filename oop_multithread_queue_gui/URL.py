
from urllib.request import urlopen
link = 'http://www.baidu.com/'
def getHtml():
    try:
        f = urlopen(link)
        #print(f)
        html = f.read()
        #print(html)
        htmldecoded = html.decode()
        #print(htmldecoded)     
    except Exception as ex:
        print('*** Failed to get Html! ***\n\n' + str(ex))   
    else:
        return htmldecoded             

if __name__ == "__main__":
    getHtml()
