import threading
import time
import random 

lock = threading.Lock

qu = []

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            if q.size() < 100:
                item = random.randint(1,100)
                qu.append(item)
                print('Putting  {} elements in queue'.format(len(qu)) )
                time.sleep(random.random())
            elif 100 < q.size() != 80 :
                lock()
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            if len(qu) > 0:
                f = open('data.txt' , 'a+')
                # item = q.dequeue()
                # q.dequeue()
                item = qu[-1]
                qu.pop()
                f.write(str(item)+",")
                f.close()
                print('Getting {} elements in queue'.format(len(qu)) )
                time.sleep(random.random())
            else :
                lock()
        return

if __name__ == '__main__':
    
    prod_number = 10
    cons_number = 10

    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    
    p.start()
    c.start()
