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
        "aiohttp",
        "urllib",
        "collections",
        "contextlib",
        "inspect",
    )

from PIL import Image, ImageDraw, ImageChops
from math import *
from requests.exceptions import ConnectionError
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord import utils
from collections import deque


eloop = asyncio.get_event_loop()
def __setloop__(): return asyncio.set_event_loop(eloop)


athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=64,
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
    try:
        if "MIZA" in GLOBALS:
            stop_miza()
        GLOBALS["MIZA"] = psutil.Popen(["python", "bot.py"], cwd=os.getcwd() + "/../../Miza-VOICE", stdout=subprocess.DEVNULL)
    except:
        print("Directory \"MIZA-VOICE\" not found.\n")

def stop_miza():
    try:
        p = GLOBALS["MIZA"]
        for c in p.children(recursive=True):
            c.kill()
        p.kill()
    except psutil.NoSuchProcess:
        pass


emptyfut = fut_nop = asyncio.Future()
fut_nop.set_result(None)
newfut = concurrent.futures.Future()
newfut.set_result(None)


# Manages concurrency limits, similar to asyncio.Semaphore, but has a secondary threshold for enqueued tasks.
class Semaphore(contextlib.AbstractContextManager, contextlib.AbstractAsyncContextManager, contextlib.ContextDecorator, collections.abc.Callable):

    __slots__ = ("limit", "buffer", "fut", "active", "passive", "rate_limit", "rate_bin", "last", "trace")

    def __init__(self, limit=256, buffer=32, delay=0.05, rate_limit=None, randomize_ratio=2, last=False, trace=False):
        self.limit = limit
        self.buffer = buffer
        self.active = 0
        self.passive = 0
        self.rate_limit = rate_limit
        self.rate_bin = deque()
        self.fut = concurrent.futures.Future()
        self.fut.set_result(None)
        self.last = last
        self.trace = trace and inspect.stack()[1]

    def __str__(self):
        classname = str(self.__class__).replace("'>", "")
        classname = classname[classname.index("'") + 1:]
        return f"<{classname} object at {hex(id(self)).upper().replace('X', 'x')}>: {self.active}/{self.limit}, {self.passive}/{self.buffer}, {len(self.rate_bin)}/{self.rate_limit}"

    def _update_bin_after(self, t):
        time.sleep(t)
        self._update_bin()

    def _update_bin(self):
        if self.rate_limit:
            try:
                if self.last:
                    if self.rate_bin and time.time() - self.rate_bin[-1] >= self.rate_limit:
                        self.rate_bin.clear()
                else:
                    while self.rate_bin and time.time() - self.rate_bin[0] >= self.rate_limit:
                        self.rate_bin.popleft()
            except IndexError:
                pass
            if len(self.rate_bin) < self.limit:
                try:
                    self.fut.set_result(None)
                except concurrent.futures.InvalidStateError:
                    pass
        return self.rate_bin

    def enter(self):
        if self.trace:
            self.trace = inspect.stack()[2]
        self.active += 1
        if self.rate_limit:
            self._update_bin().append(time.time())
        if self.fut.done() and (self.active >= self.limit or self.rate_limit and len(self.rate_bin) >= self.limit):
            self.fut = concurrent.futures.Future()
        return self

    def check_overflow(self):
        if self.passive >= self.buffer:
            raise SemaphoreOverflowError(f"Semaphore object of limit {self.limit} overloaded by {self.passive}")

    def __enter__(self):
        if self.is_busy():
            self.check_overflow()
            self.passive += 1
            while self.is_busy():
                self.fut.result()
            self.passive -= 1
        return self.enter()

    def __exit__(self, *args):
        self.active -= 1
        if self.rate_bin:
            t = self.rate_bin[0 - self.last] + self.rate_limit - time.time()
            if t > 0:
                create_future_ex(self._update_bin_after, t)
            else:
                self._update_bin()
        elif self.active < self.limit:
            try:
                self.fut.set_result(None)
            except concurrent.futures.InvalidStateError:
                pass

    async def __aenter__(self):
        if self.is_busy():
            self.check_overflow()
            self.passive += 1
            while self.is_busy():
                await wrap_future(self.fut)
            self.passive -= 1
        self.enter()
        return self

    def __aexit__(self, *args):
        self.__exit__()
        return emptyfut

    def wait(self):
        while self.is_busy():
            self.fut.result()

    async def __call__(self):
        while self.is_busy():
            await wrap_future(self.fut)
    
    acquire = __call__

    def is_active(self):
        return self.active or self.passive

    def is_busy(self):
        return self.active >= self.limit or self.rate_limit and len(self._update_bin()) >= self.limit

    @property
    def busy(self):
        return self.is_busy()

class SemaphoreOverflowError(RuntimeError):
    __slots__ = ()


async def request(self, route, *, files=None, form=None, **kwargs):
    bucket = route.bucket
    method = route.method
    url = route.url

    rtype = 0
    if "/messages" in url:
        rtype = 1

    lock = self._locks.get(bucket)
    if lock is None:
        if rtype == 1:
            lock = Semaphore(5, 256, rate_limit=5.1)
        else:
            lock = asyncio.Lock()
        if bucket is not None:
            self._locks[bucket] = lock

    # header creation
    headers = {
        'User-Agent': self.user_agent,
    }

    if self.token is not None:
        headers['Authorization'] = 'Bot ' + self.token
    # some checking if it's a JSON request
    if 'json' in kwargs:
        headers['Content-Type'] = 'application/json'
        kwargs['data'] = utils.to_json(kwargs.pop('json'))

    try:
        reason = kwargs.pop('reason')
    except KeyError:
        pass
    else:
        if reason:
            headers['X-Audit-Log-Reason'] = urllib.parse.quote(reason, safe='/ ')

    kwargs['headers'] = headers

    # Proxy support
    if self.proxy is not None:
        kwargs['proxy'] = self.proxy
    if self.proxy_auth is not None:
        kwargs['proxy_auth'] = self.proxy_auth

    if not self._global_over.is_set():
        # wait until the global lock is complete
        await self._global_over.wait()

    if not rtype:
        await lock.acquire()
        with discord.http.MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):
                if files:
                    for f in files:
                        f.reset(seek=tries)

                if form:
                    form_data = aiohttp.FormData()
                    for params in form:
                        form_data.add_field(**params)
                    kwargs['data'] = form_data

                try:
                    async with self.__dict__["_HTTPClient__session"].request(method, url, **kwargs) as r:
                        # log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), r.status)

                        # even errors have text involved in them so this is safe to call
                        data = await discord.http.json_or_text(r)

                        # check if we have rate limit header information
                        remaining = r.headers.get('X-Ratelimit-Remaining')
                        if remaining == '0' and r.status != 429:
                            # we've depleted our current bucket
                            delta = utils._parse_ratelimit_header(r, use_clock=self.use_clock)
                            # log.debug('A rate limit bucket has been exhausted (bucket: %s, retry: %s).', bucket, delta)
                            maybe_lock.defer()
                            self.loop.call_later(delta, lock.release)

                        # the request was successful so just return the text/json
                        if 300 > r.status >= 200:
                            # log.debug('%s %s has received %s', method, url, data)
                            return data

                        # we are being rate limited
                        if r.status == 429:
                            if not r.headers.get('Via'):
                                # Banned by Cloudflare more than likely.
                                raise discord.HTTPException(r, data)

                            # fmt = 'We are being rate limited. Retrying in %.2f seconds. Handled under the bucket "%s"'

                            # sleep a bit
                            retry_after: float = data['retry_after']  # type: ignore
                            # log.warning(fmt, retry_after, bucket)

                            # check if it's a global rate limit
                            is_global = data.get('global', False)
                            if is_global:
                                # log.warning('Global rate limit has been hit. Retrying in %.2f seconds.', retry_after)
                                self._global_over.clear()

                            await asyncio.sleep(retry_after)
                            # log.debug('Done sleeping for the rate limit. Retrying...')

                            # release the global lock now that the
                            # global rate limit has passed
                            if is_global:
                                self._global_over.set()
                                # log.debug('Global rate limit is now over.')

                            continue

                        # we've received a 500 or 502, unconditional retry
                        if r.status >= 500 and tries < 3:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if r.status == 403:
                            raise discord.Forbidden(r, data)
                        elif r.status == 404:
                            raise discord.NotFound(r, data)
                        elif r.status == 503:
                            raise discord.DiscordServerError(r, data)
                        else:
                            raise discord.HTTPException(r, data)

                # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

    else:
        async with lock:
            for tries in range(5):
                if files:
                    for f in files:
                        f.reset(seek=tries)

                if form:
                    form_data = aiohttp.FormData()
                    for params in form:
                        form_data.add_field(**params)
                    kwargs['data'] = form_data

                try:
                    async with self.__dict__["_HTTPClient__session"].request(method, url, **kwargs) as r:
                        # log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), r.status)

                        # even errors have text involved in them so this is safe to call
                        data = await discord.http.json_or_text(r)

                        # the request was successful so just return the text/json
                        if 300 > r.status >= 200:
                            # log.debug('%s %s has received %s', method, url, data)
                            return data

                        # we are being rate limited
                        if r.status == 429:
                            if not r.headers.get('Via'):
                                # Banned by Cloudflare more than likely.
                                raise discord.HTTPException(r, data)

                            # fmt = 'We are being rate limited. Retrying in %.2f seconds. Handled under the bucket "%s"'

                            # sleep a bit
                            retry_after: float = data['retry_after']  # type: ignore
                            # log.warning(fmt, retry_after, bucket)

                            # check if it's a global rate limit
                            is_global = data.get('global', False)
                            if is_global:
                                # log.warning('Global rate limit has been hit. Retrying in %.2f seconds.', retry_after)
                                self._global_over.clear()

                            await asyncio.sleep(retry_after)
                            # log.debug('Done sleeping for the rate limit. Retrying...')

                            # release the global lock now that the
                            # global rate limit has passed
                            if is_global:
                                self._global_over.set()
                                # log.debug('Global rate limit is now over.')

                            continue

                        # we've received a 500 or 502, unconditional retry
                        if r.status >= 500 and tries < 3:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if r.status == 403:
                            raise discord.Forbidden(r, data)
                        elif r.status == 404:
                            raise discord.NotFound(r, data)
                        elif r.status == 503:
                            raise discord.DiscordServerError(r, data)
                        else:
                            raise discord.HTTPException(r, data)

                # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

    # We've run out of retries, raise.
    if r.status >= 500:
        raise discord.DiscordServerError(r, data)

    raise discord.HTTPException(r, data)

discord.http.HTTPClient.request = lambda self, *args, **kwargs: request(self, *args, **kwargs)