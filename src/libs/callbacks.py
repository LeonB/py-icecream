#!/usr/bin/python2.5

# Copyright 2008 DeWitt Clinton. All Rights Reserved.

"""A library for creating and running callbacks and closures in Python.

Features include:

  Scopes: Callbacks can be registered in instance, class, module or
  global scope.

  Priority levels: Callbacks can be given a priority, where higher
  priority callbacks will be run before lower priority callbacks.

  Automatic requeuing: Callbacks can be marked as 'permanent' to be
  requeued automatically after being executed.

  Callback chaining: Callbacks can be chained such that the result of
  the previous callback is used as the input for the next callback.

  Genericity: Any callable object (a Callback instance, a function, a
  anonymous lambda function, or a class-based closure) can be used as
  a callback.

  Iterators: Callbacks can be invoked automatically via
  RunAllCallbacks and RunCallbackChain, or iterated over manually with
  CallbackIterator and CopyFirstCallbackIterator.

Overview:

  A callback is callable code that can be registered and executed at
  some point in the future in a different context.  The callback
  pattern allows a library to handle arbitrary clients without knowing
  in advance what they will be.

  The callback registration mechanism that allows client code to tell
  a class or module about a method that should be executed at a point
  in time in the future.

  The library is used by two distinct groups: classes or modules that
  wish to register and execute callbacks, and clients that wish to
  register their code to be called back.

  Classes or modules that register and run callbacks should first
  write a wrapper function around the RegisterCallback method.  This
  method will be invoked by other classes and code that want to be
  called back at some point in the future.  E.g.:

>>> from callbacks import RegisterCallback, RunAllCallbacks
>>>
>>> class CallbackHost(object):
...   def RegisterSomeCallback(self, callback):
...     '''Registers the callback to be invoked by RunAllCallbacks.'''
...     RegisterCallback(self, 'some callback', callback)
...
...   def RunTheCallbacks(self):
...     '''Returns the results (in a list) of  each registed callback.'''
...     return RunAllCallbacks(self, 'some callback')


  To use the registration methods, clients will provide a callback
  method in the form of a function, an anonymous lambda function, a
  class-based callable closure, or a Callback, PermanentCallback, or
  TemporaryCallback (or subclass) instance.

  After the callbacks have been registered, the class can run all of the
  registed callbacks automatically by executing the RunAllCallbacks
  method.  E.g.:

>>> from callbacks import PermanentCallback, Callback

>>> def MyCallback():
...   return 'MyCallback'

>>> host = CallbackHost()
>>> callback = PermanentCallback(MyCallback)
>>> host.RegisterSomeCallback(callback)
>>> host.RunTheCallbacks()
['MyCallback']

  Class-based closures can also be registered:

>>> class MyClosure(object):
...   def __init__(self, string):
...      self.string = string
...   def __call__(self):
...      return self.string

>>> callback = PermanentCallback(MyClosure('MyClosure'))
>>> host.RegisterSomeCallback(callback)
>>> host.RunTheCallbacks()
['MyCallback', 'MyClosure']

  As can higher-priority callbacks:

>>> callback = PermanentCallback(MyClosure('High priority'), priority=10)
>>> host.RegisterSomeCallback(callback)
>>> host.RunTheCallbacks()
['High priority', 'MyCallback', 'MyClosure']

  By default, callbacks expire after being run once:

>>> callback = Callback(MyClosure('Run once'))
>>> host.RegisterSomeCallback(callback)
>>> host.RunTheCallbacks()
['High priority', 'MyCallback', 'MyClosure', 'Run once']
>>> host.RunTheCallbacks()
['High priority', 'MyCallback', 'MyClosure']


Another Example:

  Imagine a TextProcessor class that is used to modify text.  The
  TextProcessor wants to allow callers to provide their own text
  processing routines, and does so via a RegisterProcessor method.
  When the Process method is invoked, so are the registered text
  processors.

>>> import callbacks

>>> class TextProcessor(object):
...   '''A class that modifies text according to registered callbacks.'''
...
...   def RegisterProcessor(self, callback):
...     '''Registers a callback to be invoked when the text.'''
...     callbacks.RegisterCallback(self, 'process', callback)
...
...   def Process(self, text):
...     '''Runs all of the registered callbacks to process the text.'''
...     return callbacks.RunCallbackChain(self, 'process', text)


  In the client:

>>> import re

>>> def Capitalize(text):
...   '''Returns the text with the first character capitalized.'''
...   return text.capitalize()

>>> def CompactWhitespace(text):
...   '''Returns the text with successive whitespace characters collapsed.'''
...   return re.sub('\\s+', ' ', text)

>>> processor = TextProcessor()
>>> processor.RegisterProcessor(Capitalize)
>>> processor.RegisterProcessor(CompactWhitespace)
>>> processor.Process('four  score and  seven  years    ago...')
'Four score and seven years ago...'


Limitations and TODOs:

  Function signatures are not validated.  Helper code could be written
  to match callback signatures against a function specification or
  against a reference function.

  Exceptions raised by callbacks are not handled automatically yet.

  Automatic registration and execution wrappers could be created to
  simplify the one-line boilerplate functions.

"""

__author__ = 'dewitt@unto.net'
__version__ = '0.1'


from collections import defaultdict
import heapq
import inspect
import Queue

class Callback(object):
  """A class wrapper around functions to be executed in the future."""

  def __init__(self, callback, permanent=False, priority=0):
    """Creates a new callback instance.

    Args:
      callback: The function, labmda, or callable closure to be executed.
      permanent: This callback should be requeued after being executed.
      priority: This callback will be run before callbacks of lower priority.
    """
    if not callable(callback):
      raise ValueError('The callback must callable, was %s' %
                       type(callback).__name__)

    if priority is None:
      priority = 0

    if permanent is None:
      permanent = False

    self.callback = callback
    self.permanent = permanent
    self.priority = priority

  def __call__(self, *args, **kwargs):
    """Runs the callback function, lambda, or callable closure."""
    return self.callback(*args, **kwargs)



class PermanentCallback(Callback):
  """A Callback that will be requeued after execution."""

  def __init__(self, callback, priority=0):
    """Creates a new permaent callback instance.

    Args:
      callback: The function, labmda, or callable closure to be executed.
      priority: This callback will be run before callbacks of lower priority.
    """
    super(PermanentCallback, self).__init__(
      callback, permanent=True, priority=priority)


class TemporaryCallback(Callback):
  """A Callback that will not be requeued after execution."""

  def __init__(self, callback, priority=0):
    """Creates a new temporary callback instance.

    Args:
      callback: The function, labmda, or callable closure to be executed.
      priority: This callback will be run before callbacks of lower priority.
    """
    super(TemporaryCallback, self).__init__(
      callback, permanent=False, priority=priority)


def RegisterCallback(scope, name, callback, permanent=False, priority=0):
  """Registers a new callback to be executed in the future.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
    name: The name associated with this callback
    callback: A Callback instance, a function, or other callable object
    permanent: This callback should be requeued after being executed.
    priority: Set or override the priority with the specified value
  """
  if not callable(callback):
    raise ValueError('The callback must callable, was %s' % type(callback))

  if not isinstance(callback, Callback):
    callback = Callback(callback, permanent=permanent, priority=priority)

  _GetCallbackMap(scope)[name].put(callback, priority=callback.priority)


def RunAllCallbacks(scope, name, *args, **kwargs):
  """Executes all of the callbacks within a given scope in priority order.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
    name: The name associated with the callbacks to be executed
    args:  Additional positional arguments for the callback
    kwargs:  Additional keyword arguments for the callback
  Returns:
    A list of the results from each executed callback
  """
  results = list()
  for callback in CallbackIterator(scope, name):
    results.append(callback(*args, **kwargs))
  return results


def RunCallbackChain(scope, name, param, *args, **kwargs):
  """Executes all of the callbacks with the previous callback as a parameter.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
    name: The name associated with the callbacks to be executed
    param: The in_args to the first callback in the chain.
    args:  Additional positional arguments for the callback
    kwargs:  Additional keyword arguments for the callback
  Returns:
    The final callback's result.
  """
  result = None

  for callback in CallbackIterator(scope, name):
    result = callback(param, *args, **kwargs)
    param = result
  return result


def CallbackIterator(scope, name):
  """Returns an iterator over each named callback in priority order.

  This iterator keeps a copy of all permanent callbacks, and after the
  last callback has been executed, resets the callback queue with the
  saved permanent callbacks.

  Care must be taken to ensure that the iterator is run through to the
  end, as the permament callbacks are only reset after the final
  callback has been run.

  See also CopyFirstCallbackIterator for an iterator that resets
  permanent callbacks immediately, at the expense of making a copy
  of the list beforehand.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
    name: The name associated with this callback
  Returns:
    An iterator over a copy of the named callbacks.
  """
  callback_map = _GetCallbackMap(scope)
  callback_queue = callback_map[name]
  saved_callbacks = PriorityQueue()
  for callback in callback_queue:
    if callback.permanent:
      saved_callbacks.put(callback, priority=callback.priority)
    yield callback
  callback_map[name] = saved_callbacks


def CopyFirstCallbackIterator(scope, name):
  """Returns an iterator over each named callback in priority order.

  This iterator makes a copy of the list of callbacks prior to
  beginning the iteration so that permanent callbacks can be requeued
  immediately.

  See also CallbackIterator for an iterator that avoids the overhead
  of making a copy up front, but needs to be run to completion to
  requeue the permanent callbacks.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
    name: The name associated with this callback
  Returns:
    An iterator over a copy of the named callbacks.
  """
  callback_map = _GetCallbackMap(scope)
  callback_queue = callback_map[name]
  saved_callbacks = list(callback_queue)
  for callback in saved_callbacks:
    if callback.permanent:
      callback_queue.put(callback, priority=callback.priority)
    yield callback


def ClearCallbacks(scope, name):
  try:
    del _GetCallbackMap(scope)[name]
  except KeyError:
    pass  # there were no registered callbacks under this name


def ClearAllCallbacks(scope):
  """Clears all callbacks within a given scope.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
  """
  _GetCallbackMap(scope).clear()


def _GetCallbackMap(scope):
  """Returns the dict containing all callbacks in the specified scope.

  Args:
    scope: A module, a class, an instance, or None (for the global scope)
  Returns:
    a dict of (name, priority queue of callbacks)
  """
  if scope is None:  # global scope, special case
    global __global_callbacks
    return __global_callbacks
  elif inspect.ismodule(scope):  # module scope
    attribute_name = '__module_callbacks'
  elif inspect.isclass(scope):  # class scope
    attribute_name = '__class_callbacks'
  else:  # instance scope
    attribute_name = '__instance_callbacks'
  try:
    return getattr(scope, attribute_name)
  except AttributeError:
    setattr(scope, attribute_name, defaultdict(PriorityQueue))
  return getattr(scope, attribute_name)


class PriorityQueue(Queue.Queue):
  """Implements a stable, heap-based, synchronized priority queue."""

  def _init(self, maxsize):
    self.maxsize = maxsize
    self.queue = []
    self.ordinal = 0

  def put(self, item, priority=0, *args, **kwargs):
    """Puts the item into the queue.

    Items are enqueued to be retrieved in FIFO order based on their
    priority group.

    Args:
      item: The data to be enqueued.
      priority:
        Higher priority items are retrieved before lower priority
        items.  Optional, default 0.
      block:
        If optional args block is true and timeout is None (the default),
        block if necessary until a free slot is available.
      timeout:
        If timeout is a positive number, it blocks at most timeout
        seconds and raises the Full exception if no free slot was
        available within that time. Otherwise (block is false), put an
        item on the queue if a free slot is immediately available,
        else raise the Full exception (timeout is ignored in that
        case).
    """
    self.ordinal += 1
    Queue.Queue.put(self, (-priority, self.ordinal, item), *args, **kwargs)


  def _put(self, item):
    heapq.heappush(self.queue, item)

  def _get(self):
    return heapq.heappop(self.queue)[2]

  def __iter__(self):
    while not self.empty():
      yield self.get()


__global_callbacks = defaultdict(PriorityQueue)


def _Test():
  import doctest
  doctest.testmod()

if __name__ == "__main__":
  _Test()