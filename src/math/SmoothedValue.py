import App
import Event
from Vector import *

class Scalar:
   def __init__(self, value, onChangeHandler):
      self.value = value
      self.target = value
      self.onChange = Event.Event(self)
      self.onChange += onChangeHandler

      App.world.onUpdate += self.handleTick

   def set(self, value):
      self.target = value

   def handleTick(self, world):
      if self.value != self.target:
         if abs(self.value - self.target) < 0.1:
            self.value = self.target
         else:
            self.value = (0.5 * self.value) + (0.5 * self.target)

         self.onChange(self.value)

   def __call__(self):
      return self.value

class Vector:
   def __init__(self, value, onChangeHandler):
      self.value = value
      self.target = value
      self.onChange = Event.Event(self)
      self.onChange += onChangeHandler

      App.world.onUpdate += self.handleTick

   def set(self, value):
      self.target = value

   def handleTick(self, world):
      if self.value != self.target:
         if vectorDistance(self.value, self.target) < 0.1:
            self.value = self.target
         else:
            self.value = vectorAdd(vectorScale(self.value, 0.5), vectorScale(self.target, 0.5))

         self.onChange(self.value)

   def __call__(self):
      return self.value
