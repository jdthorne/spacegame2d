import weakref

class Event:
   def __init__(self, sender):
      self.sender = sender
      self.callbacks = []

   def __add__(self, callback):
      owner = weakref.ref(callback.im_self)
      function = callback.im_func

      self.callbacks.append( (owner, function) )
      
      return self

   def __sub__(self, callback):
      for ownerRef, function in self.callbacks:
         owner = ownerRef()
         if (owner is callback.im_self) and (function is callback.im_func):
            self.callbacks.remove( (ownerRef, function) )
            return self
      
      return self

   def __call__(self, *args):
      for ownerRef, function in self.callbacks:
         owner = ownerRef()

         function(owner, self.sender, *args)
