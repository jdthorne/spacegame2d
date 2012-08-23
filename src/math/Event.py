
class Event:
   def __init__(self, sender):
      self.sender = sender
      self.callbacks = []

   def __add__(self, callback):
      self.callbacks.append(callback)
      
      return self

   def __sub__(self, callback):
      self.callbacks.remove(callback)
      
      return self

   def __call__(self, *args):
      for c in self.callbacks:
         c(self.sender, *args)


