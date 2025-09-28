class Agent:
    def __init__(self):
        self.x = None
        self.y = None
        
    def position_setter(self,x,y):
        self.x = x
        self.y = y
    def position_getter(self):
        return (self.x,self.y)
