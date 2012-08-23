import App
import Event
from Vector import *

class Scalar:
   def __init__(self, value):
      self.value = value
      self.target = value
      self.onChange = Event.Event(self)

      App.world.onUpdate += self.handleTick

   def set(self, value):
      self.target = value

   def handleTick(self, world):
      if self.value != self.target:
         self.value = (0.5 * self.value) + (0.5 * self.target)
         self.onChange(self.value)

   def __call__(self):
      return self.value

class Vector:
   def __init__(self, value):
      self.value = value
      self.target = value
      self.onChange = Event.Event(self)

      App.world.onUpdate += self.handleTick

   def set(self, value):
      self.target = value

   def handleTick(self, world):
      if self.value != self.target:
         self.value = vectorAdd(vectorScale(self.value, 0.5), vectorScale(self.target, 0.5))
         self.onChange(self.value)

   def __call__(self):
      return self.value
