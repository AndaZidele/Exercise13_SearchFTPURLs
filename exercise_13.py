from ftplib import FTP
from googlesearch import search
import threading
import queue
import random
import urllib.parse

# Example Python Code to Search for FTP URLs Using Google Custom Search API

# Lai palaistu šo failu ir jāaktivizē virtuālā vide
# Un terminālī jāieraksta "sudo python3.12 exercise_13.py"

# 5 - WorkerThread
class WorkerThread(threading.Thread):
    def __init__(self, ftpQueue, num_files):
        super().__init__()
        self.ftpQueue = ftpQueue
        self.num_files = num_files
    
    def run(self):
        while not ftpQueue.empty():
            ftpUrl = ftpQueue.get(timeout=20)

            try:
                print("Thread {} connecting to: {}".format(threading.current_thread().name, ftpUrl))

                # login to ftp site:
                #print("\n", ftpUrl)
               
                parsed_url = urllib.parse.urlparse(ftpUrl) 
                hostnameForUrl = parsed_url.hostname  
                #print(hostnameForUrl)


                ftp = FTP(hostnameForUrl, timeout=20)
                ftp.login()
            
                print("Thread {} Files in root directory of: {}".format(threading.current_thread().name, ftpUrl))

                # list the root directory content:
                # ftp = FTP('ftp.us.debian.org')

                ftp.retrlines("LIST")

                print("Worker {} - Retrieving first {} files from {}:".format(threading.current_thread().name, num_files, ftpUrl))
                files = ftp.nlst()  # List the directory contents

                # # Retrieve and print only the first 2 files
                for i, file in enumerate(files[:num_files]):
                    print("{}. {}".format(i+1, file))


                ftp.quit()

            except Exception as e:
                print("Thread {} failed to connect to {}: {}".format(threading.current_thread().name, ftpUrl, e))

            finally:
                print("")


# 4 - funkcija
def getResults(randomThreadsCount, ftpQueue, num_files):
    ftpThreads = []
    while randomThreadsCount > 0:
        ftpThread = WorkerThread(ftpQueue, num_files)
        ftpThread.start()
        ftpThreads.append(ftpThread)
        randomThreadsCount -= 1
    #ftpThreads.join()
    for thread in ftpThreads:
        thread.join()




if __name__ == "__main__":
    # 1 - create a list of 20 FTP sites
    # kodu parveidot nedaudz jo ir no interneta
    que = "public data" #site:gnu.org" #"public ftp"
    query = "inurl:ftp:// site:gnu.org" #"inurl:ftp://" #"inurl:ftp:// {}".format(que) #"#inurl:ftp:// public ftp" #data" #"site:"
    num_results = 20
    num_files = 2
    port = 20

    ftpUrls = [url for url in search(query, num_results=num_results)]
# print(ftpUrls)


    # 2 - use multiple threads (random from 3-5)
    randomThreadsCount = random.randint(3, 5)

    # 3 - list to queue
    ftpQueue = queue.Queue()
    for ftpUrl in ftpUrls:
        ftpQueue.put(ftpUrl)
    #print(ftpUrls)

    getResults(randomThreadsCount, ftpQueue, num_files)
    print("Work with threads are finished!")    
