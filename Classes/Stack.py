class Stack:
    # Initializing the stack with an empty list to hold items
    def __init__(self):
        self.items = []

    # Method to push an item onto the stack
    def push(self, item):
        self.items.append(item)

    # Method to pop an item from the stack
    def pop(self):
        return self.items.pop()
    
    # Method to peek at the top item of the stack without removing it
    def peek(self):
        return self.items[-1]
    

if __name__ == '__main__':
    # Creating a new stack instance
    s = Stack()
    # Pushing items onto the stack
    s.push(1)
    s.push(2)
    s.push(3)
    # Popping items from the stack and printing them
    print(s.pop())  
    print(s.pop())  
    print(s.pop())  
