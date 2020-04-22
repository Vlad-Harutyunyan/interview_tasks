import threading as t
import time
import random 
from queue import Queue

#init max queue size and buffer size for threads
MAX_QSIZE = 100
BUFF_SIZE = 20

#Producer class
class ProducerThread:


    def __init__(self, queue, sm ): #init queue 
        self.queue = queue #init queue 
        self.s = sm # init semaphore


    def run(self): #mehtod for Producer class starting
        try: #try to catch keyboard interrupt error , still doesnt work
            #if  queue doesnt full ,we also can use queue class full method with  not
            while self.queue.qsize() < 100 :

                self.s.release() #Acquire a semaphore.
                item = random.randint(1,101) #random number in 1-100 range 
                self.queue.put(item) # insert random number to queue
                print('Putting:  {} elements in queue'.format(self.queue.qsize()) ) 
                time.sleep(random.random()) # sleep random miliseconds in range 0.1 - 0.99 ~ 10 - 99.99 milliseconds
               
                if self.queue.qsize() == 100: #if queue size is full stop threads and alert in console 
                    print('Queue is full,producer waiting...')
                    self.s.acquire() # Thread sleep 
                    
            if self.queue.qsize() == 80 :
                self.s.release()#Thread wake up

        except KeyboardInterrupt: # still doesnt work , print('ok') hust for testing
            print('ok')
        
#Consumer Class
class ConsumerThread:


    def __init__(self, queue ,sm):#iniit queue
        self.queue = queue # init qeuee
        self.s = sm #init semaphore


    def run(self):
        try: #try to catch keyboard interrupt error , still doesnt work

            while not self.queue.empty(): # if queue is not empty 

                item = self.queue.get() # getting first item from queue (FIFO-first in first out)
                f = open('data.txt' , 'a+')#open data.txt file a+ (we can open and add new text without deleting old text in this file)
                f.write(str(item))
                f.close() # close file , if we doesnt close file , loop doesnt work 
                self.s.release()
                self.queue.task_done() # Used by queue consumer threads. For each get() used to fetch a task, a subsequent call to task_done() tells the queue that the processing on the task is complete.
                print ('Getting: {} elements in queue'.format(self.queue.qsize()) )
                time.sleep(random.random()) # sleep random miliseconds in range 0.1 - 0.99 ~ 10 - 99.99 milliseconds

            self.s.acquire()
            print ("consumer:Waiting...") 

        except KeyboardInterrupt:

            print('ok')

def main(prod_count,cons_conut):
    q = Queue(maxsize=MAX_QSIZE) #init queue
    
    Producer_Thread_List = [] # list for all producer threds
    for i in range(prod_count):# appending N conut threads to list
        # creating semaphore for multiprocessroing
        s = t.Semaphore(prod_count)
        producer = ProducerThread(q,s)
        producer_thread = t.Thread(target=producer.run , name = f'poducer_{i}')
        Producer_Thread_List.append(producer_thread)


    Consumer_Thread_List = [] # list for all consumer threds
    for i in range(cons_conut): # appending N conut threads to list
        # creating semaphore for multiprocessroing
        s = t.Semaphore(cons_conut)
        consumer = ConsumerThread(q,s)
        consumer_thread = t.Thread(target=consumer.run , name = f'consumer_{i}')
        Consumer_Thread_List.append(consumer_thread)

    for elem in Producer_Thread_List:#start all producer threads
        elem.start()
    for elem in Consumer_Thread_List:#start all consumer threads
        elem.start()

    q.join() # Blocks until all items in the queue have been gotten and processed.

if __name__ == '__main__':
    prod_count = int(input('Please enter number of producers : ')) #getting count of producers thread
    cons_count = int(input('Please enter number of consumers : ')) #getting count of consumers thread
    try:#try catch error here still doesnt work
        main(prod_count,cons_count)
    except KeyboardInterrupt:
        print('Please wait')
        
    
    
