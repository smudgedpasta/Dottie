import contextlib, concurrent.futures


# Assigning the prefix to a variable
PREFIX = "d."


# Assigning a list of bot owners to is_owner check
OWNERS = [530781444742578188, 201548633244565504]

def is_owner(ctx):
  return ctx.message.author.id in OWNERS


# Assigning a list of channels to act as a python terminal within Discord
# TERMINALS = [757848291181461574]


# Assigning a list of channels to act as a python terminal within Discord
with open("terminals", "r") as f:
  s = f.read()
TERMINALS = {int(i) for i in s.splitlines() if i}


# A context manager that enables concurrent imports.
class MultiThreadedImporter(contextlib.AbstractContextManager, contextlib.ContextDecorator):

    def __init__(self, glob=None):
        self.glob = glob
        self.exc = concurrent.futures.ThreadPoolExecutor(max_workers=12)
        self.out = {}

    def __enter__(self):
        return self

    def __import__(self, *modules):
        for module in modules:
            self.out[module] = self.exc.submit(__import__, module)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        if exc_type and exc_value:
            raise exc_value

    def close(self):
        for k in tuple(self.out):
            self.out[k] = self.out[k].result()
        glob = self.glob if self.glob is not None else globals()
        glob.update(self.out)
        self.exc.shutdown(True)


with MultiThreadedImporter() as importer:
    importer.__import__(
        "inspect",
        "time",
        "datetime",
        "random",
        "requests",
        "asyncio",
        "os",
        "psutil",
        "traceback",
        "math",
        "youtube_dl",
        "discord",
        "discord.ext",
        "json",
        "threading",
    )

# The special imports still need to be added, though they're sped up by the files already having been imported
from math import *
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure


# eloop is just the asyncio event loop, what that means is just a queue of actions to be done, all coroutines (stuff with await) are put in this queue, and more than one can be awaited at a time
eloop = asyncio.get_event_loop()
def __setloop__(): return asyncio.set_event_loop(eloop)


# this is a thread pool, which manages the almost fully concurrent operations, which has its own queue similar to the asyncio event loop, but you can put functions on it that aren't async
athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=16,
    initializer=__setloop__,)
__setloop__()


# uh, don't know why this is here, maybe it was for the other threads trying to get the `eloop` variable?
def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return eloop

# similar to the asyncio.wrap_future function except doesn't check that it's actually a future, which allows you to add some other classes with a `result()` method
def wrap_future(fut, loop=None):
    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = eloop
    new_fut = loop.create_future()

    def on_done(*void):
        try:
            result = fut.result()
        except Exception as ex:
            loop.call_soon_threadsafe(new_fut.set_exception, ex)
        else:
            loop.call_soon_threadsafe(new_fut.set_result, result)

    fut.add_done_callback(on_done)
    return new_fut


# checks if you can `await` the targeted object
def awaitable(obj): return hasattr(obj, "__await__") or issubclass(type(obj), asyncio.Future) or issubclass(type(obj), asyncio.Task) or inspect.isawaitable(obj)


# submits a function to the thread pool queue, returning the associated concurrent.futures Future object
def create_future_ex(func, *args, timeout=None, **kwargs):
    fut = athreads.submit(func, *args, **kwargs)
    if timeout is not None:
        fut = athreads.submit(fut.result, timeout=timeout)
    return fut


# submits function to the thread pool queue, but waits asynchronously for the output, then makes sure the result is no longer an awaitable by repeatedly awaiting it
async def _create_future(obj, *args, loop, timeout, **kwargs):
    if asyncio.iscoroutinefunction(obj):
        obj = obj(*args, **kwargs)
    elif callable(obj):
        if asyncio.iscoroutinefunction(obj.__call__) or not is_main_thread():
            obj = obj.__call__(*args, **kwargs)
        else:
            obj = await wrap_future(create_future_ex(obj, *args, timeout=timeout, **kwargs), loop=loop)
    while awaitable(obj):
        if timeout is not None:
            obj = await asyncio.wait_for(obj, timeout=timeout)
        else:
            obj = await obj
    return obj


# just a helper function for _create_future which is able to identify the event loop
def create_future(obj, *args, loop=None, timeout=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    fut = _create_future(obj, *args, loop=loop, timeout=timeout, **kwargs)
    return create_task(fut, loop=loop)


# works like asyncio.create_task but falls back to using `eloop` if the asyncio loop isn't found for whatever reason
def create_task(fut, *args, loop=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    return asyncio.ensure_future(fut, *args, loop=loop, **kwargs)

# checks if the function is being called by the main thread
is_main_thread = lambda: threading.current_thread() is threading.main_thread()
