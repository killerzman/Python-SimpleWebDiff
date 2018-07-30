import re
import requests
import subprocess
import sys
import time
import warnings
import webbrowser

def open_link_in_broswer(url):
    
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)
    #via https://stackoverflow.com/a/16514719/7787441

def is_positive_integer(integer):
    
    regex = re.compile(r'^[1-9]\d*$')
    return re.match(regex, str(integer))
    #via https://stackoverflow.com/a/7036361/7787441

def is_url(url):
    
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, str(url))
    #via https://stackoverflow.com/a/7160778/7787441

def is_diff(r1, r2):
    
    return not (r1 == r2)
    
def parse_args(args):
    
    i = 1                 #skip script name and go for the important args
    correct = True        #bool assume valid input until proven otherwise
    link = ''             #string for link
    link_found = False    #bool if link has been found in args
    r = False             #bool if checking again
    o = False             #bool if opening web browser
    t = 60                #int interval between checks in seconds
    w = False             #bool to suppress warnings
    v = True              #bool if checking the ssl cert
    t_flag_found = False  #bool if -t was found
    t_nr_found = False    #bool if -t has a value

    while i < len(args):
        if not link_found:
            if is_url(args[i]):
                link = str(args[i])
                link_found = True
        if args[i] == '-r':
            r = True
        elif args[i] == '-o':
            o = True
        elif ( (not t_flag_found) and (args[i] == '-t') ):
            t_flag_found = True
            if (i+1 != len(args)) and is_positive_integer(args[i+1]):
                t = int(args[i+1])
                t_nr_found = True
        elif args[i] == '-w':
            w = True
        elif args[i] == '-v':
            v = False
        i += 1

    if not link_found:
        print("\nProvide a valid url")
        print("example: https://en.wikipedia.org/wiki/Static_web_page")
        print("")
        correct = False

    if t_flag_found and not t_nr_found:
        print("\nProvide a number for the -t flag")
        print("example: -t 30")
        print("")
        correct = False

    if correct:
        web_diff(link, r, o, t, w, v)

def get_website_data(link, ver):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return (requests.get(str(link), headers = headers, verify = ver)).content

def web_diff(link, r, o, t, w, v):

    no_diff = True
    
    if w:
        warnings.filterwarnings("ignore")
    
    initial_res = get_website_data(link, v)
    print("\nsaved initial site info for: " + str(link))
    print("-----")

    while no_diff:
        print("\nchecking again in " + str(t) + " secs")
        print("-----")
        time.sleep(t)
        updated_res = get_website_data(link, v)
        print("\nsaved updated(?) site info for: " + link)
        print("diff checking @ " + str(time.ctime()))
        print("-----")
        no_diff = not is_diff(initial_res, updated_res)
        if not no_diff:
            print("\ndiff found!")
            print("-----")
            if o:
                open_link_in_broswer(link)
                print("\nopening browser to: " + link)
                print("-----")
            if r:
                web_diff(link, r, o, t, w, v)
            else:
                no_diff = False
                break
        else:
            print("\nno diff found")
            print("-----")

def main():
    if len(sys.argv) == 1:
        print("")
        print("usage: python " + str(sys.argv[0]) + " -flags <website_url>")
        print("IMPORTANT! THIS IS ONLY USEFUL FOR MOSTLY STATIC WEBPAGES!")
        print("THIS IS VERY SENSITIVE TO EVEN BITS OF INFORMATION BEING CHANGED!")
        print("DOES NOT SHOW ACTUAL CHANGES, JUST CHECKS FOR THEM!")
        print("")
        print("<website_url>: the website to check for differences")
        print("")
        print("Available flags:")
        print("-r     -> check again even if differences are found")
        print("          default: false")
        print("")
        print("-o     -> open web browser when differences are found")
        print("          default: false")
        print("")
        print("-t int -> how often in seconds to check for differences")
        print("          default: 60")
        print("")
        print("-w     -> suppress warnings")
        print("          default: false")
        print("          WARNING!")
        print("          FLAG SHOULDN'T BE USED IF DEBUGGING")
        print("")
        print("-v     -> ignore verifying the SSL certificate")
        print("          default: false")
        print("          WARNING!")
        print("          TRY USING HTTP INSTEAD OF HTTPS")
        print("          USE THIS WITH -w")
        print("          USE THIS IF ALL ELSE FAILS")
        print("")
        print("example: python " + str(sys.argv[0]) + " -o -t 30 https://en.wikipedia.org/wiki/Static_web_page")
        print("(example will check for differences every 30 seconds and will open the browser upon finding one)")
        print("")
    else:
        parse_args(sys.argv)
            
if __name__ == '__main__':
    main()
