from threading import Semaphore
from collections import defaultdict

class lww_element_set():
    def __init__(self):
        self.add_set = defaultdict(float)
        self.remove_set = defaultdict(float)
        self.add_sem = Semaphore()
        self.remove_sem = Semaphore()

    def add(self, element, timestamp):
        timestamp = float(timestamp)
        self.add_sem.acquire()
        self.check_and_insert(self.add_set, element, timestamp)
        self.add_sem.release()

    def remove(self, element, timestamp):
        timestamp = float(timestamp)
        self.remove_sem.acquire()
        self.check_and_insert(self.remove_set, element, timestamp)
        self.remove_sem.release()

    def check_and_insert(self, target_set, element, timestamp):
        if element in target_set:
            curr_timestamp = target_set[element]
            if curr_timestamp < timestamp:
                target_set[element] = timestamp
        else:
            target_set[element] = timestamp

    def exist(self, element):
        if element not in self.add_set:
            return False
        elif element not in self.remove_set:
            return True
        elif self.add_set[element] >= self.remove_set[element]:
            return True
        else:
            return False

    def get(self):
        result = []
        for element in self.add_set:
            if self.exist(element):
                result.append(element)
        return result
