import threading as t
import time
import random 
from queue import Queue


MAX_QSIZE = 100
BUFF_SIZE = 20
# creating semaphore for multiprocessroing
s = t.Semaphore(BUFF_SIZE)
fill_count = t.Semaphore(0)
empty_count = t.Semaphore(1000)

class ProducerThread:
    def __init__(self, queue, buff_size=BUFF_SIZE):
        self.queue = queue
        self.buff_size = buff_size
        self.s = s


    def run(self):
        check = True
        try:
            while self.queue.qsize() < 100 and check == True:
                empty_count.acquire()
                item = random.randint(1,100)
                fill_count.release()
                self.queue.put(item)
                print('Putting:  {} elements in queue'.format(self.queue.qsize()) )
                time.sleep(random.random())
                if self.queue.qsize() == 100:
                    print('Queue is full,producer waiting...')
                    empty_count.release()
                    
            if self.queue.qsize() == 80 :
                empty_count.acquire()
                
        except KeyboardInterrupt:
            print('ok')
        

class ConsumerThread:
    def __init__(self, queue):
        self.queue = queue
        self.s = s

    def run(self):
        try:
            while not self.queue.empty():
                item = self.queue.get()
                f = open('data.txt' , 'a+')
                f.write(str(item))
                f.close()
                empty_count.acquire()
                fill_count.release()
                self.queue.task_done()
                print ('Getting: {} elements in queue'.format(self.queue.qsize()) )
                time.sleep(random.random())

            empty_count.release()
            print ("consumer:Waiting...")
        except KeyboardInterrupt:
            print('ok')

def main(prod_count,cons_conut):
    q = Queue(maxsize=MAX_QSIZE)
    
    Producer_Thread_List = []
    for i in range(prod_count):
        producer = ProducerThread(q)
        producer_thread = t.Thread(target=producer.run , name = f'poducer_{i}')
        Producer_Thread_List.append(producer_thread)


    Consumer_Thread_List = []
    for i in range(cons_conut):
        consumer = ConsumerThread(q)
        consumer_thread = t.Thread(target=consumer.run , name = f'consumer_{i}')
        Consumer_Thread_List.append(consumer_thread)

    for elem in Producer_Thread_List:
        elem.start()
    for elem in Consumer_Thread_List:
        elem.start()

    q.join()

if __name__ == '__main__':
    prod_count = int(input('Please enter number of producers : '))
    cons_count = int(input('Please enter number of consumer : '))

    main(prod_count,cons_count)

    
    
