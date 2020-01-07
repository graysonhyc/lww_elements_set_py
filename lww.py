from threading import Semaphore
from collections import defaultdict

class LWW_ElementSet():
    """A Python implementation of Last-Writer-Win (LWW) element set.

    The LWW element set stores a single instance of each element, coupled with 
    the timestamp of insertion, i.e., {lww element: timestamp}. 
    """

    def __init__(self):
        """LWW element set constructor

        Points to note:
        -Python dictionaries are used as the main data structure.
        -Insertion, Update and Searching can be done in O(1) time.
        -The data type of timestamp is a floating point number.
        -Semaphores are added to ensure thread-safe operations
        """
        self.add_set = defaultdict(float)
        self.remove_set = defaultdict(float)

        # Just for demo: Python built-in dictionaries are inherently thread-safe
        # https://stackoverflow.com/questions/6953351/thread-safety-in-pythons-dictionary
        self.add_sem = Semaphore()
        self.remove_sem = Semaphore()

    def add(self, element, timestamp):
        """Add an element to the LWW element set, or update its timestamp if it already exists.
        
        Elements are added to an LWW-Element-Set by inserting the element 
        into the add set, with a timestamp.

        The timestamp input arguemnt is first converted to float. Then, this method
        tries to add the element with timestamp into the add_set. 

        Returns True if insertion is successful, or False if any exception occur.
        """
        timestamp = float(timestamp)
        success = True
        self.add_sem.acquire()
        try: 
            self.check_and_insert(self.add_set, element, timestamp)
        except:
            success = False 
        finally:
            self.add_sem.release() #unlock no matter what
        return success

    def remove(self, element, timestamp):
        """Remove an element from the LWW element set.
        
        Elements are removed from the LWW-Element-Set by being added 
        to the remove set, again with a timestamp.

        Note that there is a conceptual difference between LWW set removal and ordinary 
        set removal. In LWW set operation, a removal does not actually remove an element 
        from the set, but to add a "removal record" in the remove set.

        The timestamp input arguemnt is first converted to float. Then, this method
        tries to add the element with timestamp into the remove_set. 

        Returns True if insertion is successful, or False if any exception occur.
        """
        timestamp = float(timestamp)
        success = True
        self.remove_sem.acquire()
        try:
            self.check_and_insert(self.remove_set, element, timestamp)
        except:
            success = False
        finally:
            self.remove_sem.release() #unlock no matter what
        return success

    def check_and_insert(self, target_set, element, timestamp):
        """A helper function to add element/update timestamp in the target set.

        This helper function adds an element in the target set if an element 
        does not exist, or update the original timestamp if the input timestamp 
        is newer.

        The use of defaultdict automatically assigns the return value to 0.0
        if element key does not exist. Since timestamp is >= 0, we can use the following
        one-liner.

        Input arguments:
        - target_set: add_set/remove_set 
        - element: the element to be added
        - timestamp: the time of insertion (float, non-negative)
        """
        target_set[element] = max(target_set[element], timestamp)

    def contains(self, element):
        """Determine if an element exists in the LWW element set.

        An element is a member of the LWW-Element-Set if it is in the add set, 
        and either not in the remove set, or in the remove set but with an earlier 
        timestamp than the latest timestamp in the add set. We bias "add" if the "add" and
        "remove" of the same element has the same timestamp to prevent data loss.

        Returns True if element exists, or False if element doesn't exist.
        """

        # The element was never added
        if element not in self.add_set:
            return False
        # The element was added before and was never removed
        elif element not in self.remove_set:
            return True
        # The element was added and removed before, but the timestamp of "add" is 
        # larger than that of "remove"
        elif self.add_set[element] >= self.remove_set[element]:
            return True
        # The element was added and removed before, but the timstamp of "remove" is 
        # larger than that of "add"
        else:
            return False

    def get_all(self):
        """Return a list of all existing elements in the LWW element set

        This method makes use of contains() and checks all elements in the add_set.
        Elements will be copied to the result list if they are not removed eventually.
        """
        result = [x for x in self.add_set if self.contains(x)]
        return result
