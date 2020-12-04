import contextlib, concurrent.futures


PREFIX = "d."


OWNERS = [530781444742578188, 201548633244565504]

def is_owner(ctx):
  return ctx.message.author.id in OWNERS


try:
    with open("terminals", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
TERMINALS = {int(i) for i in s.splitlines() if i}


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
        "discord",
        "discord.ext",
        "json",
        "threading",
    )

from math import *
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure


eloop = asyncio.get_event_loop()
def __setloop__(): return asyncio.set_event_loop(eloop)


athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=16,
    initializer=__setloop__,)
__setloop__()


def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return eloop

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


def awaitable(obj): return hasattr(obj, "__await__") or issubclass(type(obj), asyncio.Future) or issubclass(type(obj), asyncio.Task) or inspect.isawaitable(obj)


def create_future_ex(func, *args, timeout=None, **kwargs):
    fut = athreads.submit(func, *args, **kwargs)
    if timeout is not None:
        fut = athreads.submit(fut.result, timeout=timeout)
    return fut


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


def create_future(obj, *args, loop=None, timeout=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    fut = _create_future(obj, *args, loop=loop, timeout=timeout, **kwargs)
    return create_task(fut, loop=loop)


def create_task(fut, *args, loop=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    return asyncio.ensure_future(fut, *args, loop=loop, **kwargs)

is_main_thread = lambda: threading.current_thread() is threading.main_thread()
