'''
* Fork a thread
* run in background on iPad
* rewrite with gui

in the child thread:
	set timer
	when timer expires, creat alert
	option to set next timer or exit
	
in parent thread:
	wait for child to finish
	
end program

'''


#!/usr/bin/python

import threading
import time
import menu

exitFlag = 0
threadLock = threading.Lock()
threads = []

class myThread (threading.Thread):
   def __init__(self, threadID, name, iterations, delay, label):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.iterations = iterations
      self.delay = delay
      self.label = label
   def run(self):
      print ("\nStarting " + self.name)
      
      # Get lock to synchronize threads
      #threadLock.acquire()
      #print_time(self.name, self.counter, 1)
      menu.testCorrectScore([ self.iterations, self.delay, self.label ])
      # Free lock to release next thread
      #threadLock.release()
      
      print ("\nExiting " + self.name)

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print (threadName + " *** " + str( time.ctime(time.time())) )
      counter -= 1


def start(iterations, delay, label) :
	

	print("starting ")
	

	
	
	# Create new threads
	thread1 = myThread(1, "Thread-1 ", iterations, delay, label)
	#thread2 = myThread(2, "Thread-2 ", 3)
	
	# Start new Threads
	thread1.start()
	#thread2.start()
	
	#Add threads to thread list
	#threads.append(thread1)
	#threads.append(thread2)
	
	# Wait for all threads to complete
	#for t in threads:
	#    t.join()
	
	
	print ("Exiting Start")



'''
import _thread


#!/usr/bin/python

import _thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
    #  print "%s: %s" % ( threadName, time.ctime(time.time()) )
      print(threadName + str(time.ctime(time.time()) ))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass
   
   
'''
'''
# coding: utf-8
import ui, time
v=ui.View()
b1=ui.Button(title='backgrounded',frame=(10,50,100,50))
b2=ui.Button(title='not backgrounded',frame=(10,150,100,50))

@ui.in_background
def b1action(sender):
   for i in range(6):
      sender.title=str(i)
      time.sleep(0.5)

def b2action(sender):
   # the ui does not update until this method exits!
   for i in range(6):
      sender.title=str(i)
      time.sleep(0.5)
      
b1.action=b1action    
b2.action=b2action
v.add_subview(b1)
v.add_subview(b2)
v.present()
'''

