import contextlib, concurrent.futures

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

from math import *
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
