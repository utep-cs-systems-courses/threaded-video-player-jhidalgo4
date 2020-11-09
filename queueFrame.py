#!/usr/bin/env python3

import threading
from threading import Lock
from threading import Semaphore


class Queue:
    #capacity set to 10
    def __init__(self, capacity):
        self.queue = []
        self.capacity = capacity
        self.semaphore1 = threading.Semaphore(capacity)
        self.semaphore2 = threading.Semaphore(0)

        
    def post(self, frame):
        self.semaphore1.acquire()
        self.queue.append(frame)
        self.semaphore2.release()

        
    def get(self):
        self.semaphore2.acquire()
        frame = self.queue.pop(0)
        self.semaphore1.release()
        return frame

