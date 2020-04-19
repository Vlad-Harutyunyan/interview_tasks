import threading 
from threading import Semaphore
import time
import random 

lock = threading.Lock

qu = []
MAX_BUFF = 100
s = Semaphore()

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name
        global queue
        

    def run(self):
        while True:
            if len(qu) <= 100:
                item = random.randint(1,100)
                qu.append(item)
                print('Putting  {} elements in queue'.format(len(qu)) )
                s.release()
                time.sleep(random.random())
            else:
                print('list is full,producer waiting')
                s.release()
                print ("Space in queue, Consumer notified the producer")

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        
        while True:
            s.acquire()
            if qu:
                f = open('data.txt' , 'a+')
                # item = q.dequeue()
                # q.dequeue()
                item = qu[0]
                qu.pop(0)
                f.write(str(item)+",")
                f.close()
                print('Getting {} elements in queue'.format(len(qu)) )
                s.release()
                time.sleep(random.random())
            else :
                print ("Producer added something to queue and notified the consumer")
                s.release()
        return

def runCons():
    c = ConsumerThread(name = 'Consumer')
    c.start()
def runProd():
    p = ProducerThread(name = 'Producer')
    p.start()
if __name__ == '__main__':
    cons_number = int(input('please, enter consumers number : '))
    prod_number = int(input('please, enter producers number : '))
    for x in range(cons_number) :
        runCons()
    for x in range(prod_number) :
        runProd()

    #semaphor - es anum minjev sax chanen lock , nuyn indexov datain chen karanq dimenq , petqa sinxronizaciya 

    #deadlock kardal .   

    
    
