import contextlib, concurrent.futures

GLOBALS = globals()


PREFIX = ["d.", "D."]


OWNERS = [530781444742578188, 201548633244565504]

def is_owner(ctx):
  return ctx.message.author.id in OWNERS


try:
    with open("database/terminal_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
TERMINALS = {int(i) for i in s.splitlines() if i}


try:
    with open("database/DM_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
DM_CHANNEL = {int(i) for i in s.splitlines() if i}


try:
    with open("database/log_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
LOG_CHANNELS = {int(i) for i in s.splitlines() if i}


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
        "subprocess",
        "inspect",
        "time",
        "datetime",
        "random",
        "copy",
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
        "sys",
        "inspirobot",
        "re",
        "io",
        "PIL",
    )

from PIL import Image, ImageDraw, ImageChops
from math import *
from requests.exceptions import ConnectionError
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
    try:
        kwargs["timeout"] = kwargs.pop("_timeout_")
    except KeyError:
        pass
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
    if not isinstance(fut, asyncio.Task):
        fut = create_task(fut, loop=loop)
    return fut


def create_task(fut, *args, loop=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    return asyncio.ensure_future(fut, *args, loop=loop, **kwargs)

is_main_thread = lambda: threading.current_thread() is threading.main_thread()


pink_embed = 15277667

rainbow_embeds = [
    16711680,
    16738304,
    16773888,
    2948864,
    61951,
    6655,
    8323327,
    16711861
]


def create_progress_bar(length, ratio):
	start_bar = [
		"<:_:777028747383013376>",
		"<a:_:777028749970636833>",
		"<a:_:777028752660103179>",
		"<a:_:777028754983485462>",
		"<a:_:777028758895853589>",
	]
	mid_bar = [
		"<:_:777028760477892668>",
		"<a:_:777028763149271061>",
		"<a:_:777028767125995520>",
		"<a:_:777028769839054878>",
		"<a:_:777028773320589375>",
	]
	end_bar = [
		"<:_:777028775451820032>",
		"<a:_:777028777909551144>",
		"<a:_:777028780640305202>",
		"<a:_:777028782766555137>",
		"<a:_:777028787971424288>",
	]
	high = length * 4
	position = min(high, round(ratio * high))
	items = []
	new = min(4, position)
	items.append(start_bar[new])
	position -= new
	for i in range(length - 1):
		new = min(4, position)
		if i >= length - 2:
			bar = end_bar
		else:
			bar = mid_bar
		items.append(bar[new])
		position -= new
	return "".join(items)


def get_random_emoji():
    random_emoji = chr(128512 + random.randint(0, 49))
    return random_emoji


if not os.path.exists("../database"):
    try:
        print("Checking for database files, folder will be created if missing...")
        database_folder = os.path.join("../Dottie", "database")
        os.mkdir(database_folder)
    except Exception as e:
        print()

if not os.path.exists("config.json") or not os.path.getsize("config.json"):
    print("No token found, generating config.json file... Please include Discord token when complete.\n\n")
    with open("config.json", "w") as f:
        template = {
            "token": ""
        }
        json.dump(template, f, indent=4)
        raise SystemExit


def start_miza():
    if "MIZA" in GLOBALS:
        stop_miza()
    GLOBALS["MIZA"] = psutil.Popen(["python", "bot.py"], cwd=os.getcwd() + "/../../Miza-VOICE", stdout=subprocess.DEVNULL)

def stop_miza():
    try:
        p = GLOBALS["MIZA"]
        for c in p.children(recursive=True):
            c.kill()
        p.kill()
    except psutil.NoSuchProcess:
        pass
