GoodNotes Interview - SWE Challenge (By Grayson Ho)
===
This is the deliverable for the first technical challenge for the position of Software Engineer, Machine Learning @ GoodNotes. A Last-Writer-Wins (LWW) Element set data structure, an operation-based Conflict-Free Replicated Data Type (CDRT) was implemented in Python. A test suite was also included to test various CDRT properties, i.e., communtativity,
associativity and idempotence.

### Operations
The conceptual idea is referenced from [this wiki page](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set_(Last-Write-Wins-Element-Set)).

Operations on CRDTs need to adhere to the following rules:

- Associativity (a+(b+c)=(a+b)+c), so that grouping doesn't matter.
- Commutativity (a+b=b+a), so that order of application doesn't matter.
- Idempotence (a+a=a), so that duplication doesn't matter.

To determine if an element exists in the LWW element set, the following rules are applied:

- Exists if the element's most recent operation is an "add"
- Does not exist if the element's most recent operation is a "remove"

This implementation provides the following APIs:

- add(element, timestamp) : Add an element with the timestamp to the add set
- remove(element, timestamp) : Add an element with the timestamp to the remove set
- exist(element) : Check if an element exists in the LWW element set using the rules above
- get() : Return all existing elements in the LWW element set

### Testing

#### Test for Idempotence
It is required that duplication or re-delivery of operations does not affect the final result.
The following tests attempt to repeat the "add" / "remove" operations with different timestamps.

| Original state | Operation   | Resulting state | Final result |
|----------------|-------------|-----------------|--------------|
| A(a,1) R()     | add(a,0)    | A(a,1) R()      | ['a']        |
| A(a,1) R()     | add(a,1)    | A(a,1) R()      | ['a']        |
| A(a,1) R()     | add(a,2)    | A(a,2) R()      | ['a']        |
| A() R(a,1)     | remove(a,0) | A() R(a,1)      | [   ]        |
| A() R(a,1)     | remove(a,1) | A() R(a,1)      | [   ]        |
| A() R(a,1)     | remove(a,2) | A() R(a,2)      | [   ]        |

#### Test for Commutativity
It is required that the order of operations does not affect the final result.
The following tests attempt to reverse the "add" and "remove" operations with different timestamps.

| Original state | Operation   | Resulting state | Final result |
|----------------|-------------|-----------------|--------------|
| A(a,1) R()     | remove(a,1) | A(a,1) R(a,1)   | ['a']        |
| A() R(a,1)     | add(a,1)    | A(a,1) R(a,1)   | ['a']        |
| A(a,1) R()     | remove(a,0) | A(a,1) R(a,0)   | ['a']        |
| A() R(a,0)     | add(a,1)    | A(a,1) R(a,0)   | ['a']        |
| A(a,1) R()     | remove(a,2) | A(a,1) R(a,2)   | [   ]        |
| A() R(a,2)     | add(a,1)    | A(a,1) R(a,2)   | [   ]        |

#### Test for Associativity
It is required that the grouping of operations does not affect the final result.


### References


