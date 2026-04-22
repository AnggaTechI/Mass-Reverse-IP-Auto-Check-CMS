# Mass Reverse IP Auto Check CMS
# Follow for update :
# https://github.com/AnggaTechI

import sys
import re
import time
import os
import shutil
import asyncio
import warnings
warnings.filterwarnings("ignore")

IS_WINDOWS = sys.platform == "win32"

try:
    import aiohttp
except ImportError:
    os.system("pip install aiohttp -q")
    import aiohttp

aiodns = None
if not IS_WINDOWS:
    try:
        import aiodns
    except ImportError:
        os.system("pip install aiodns -q")
        try:
            import aiodns
        except ImportError:
            aiodns = None

from urllib.parse import urlparse

API_URL        = "http://api.webscan.cc/?action=query&ip={ip}"
OUTPUT_ALL     = "results.txt"
TIMEOUT        = 8
DNS_TIMEOUT    = 4
FP_TIMEOUT     = 6
FP_RATIO       = 2
FP_READ_BYTES  = 24000
PROGRESS_EVERY = 0.1

DEFAULT_CONC = 150 if IS_WINDOWS else 200
MAX_CONC     = 1000 if IS_WINDOWS else 2000

CMS_FILES = {
    "wordpress":   "wordpress.txt",
    "laravel":     "laravel.txt",
    "joomla":      "joomla.txt",
    "drupal":      "drupal.txt",
    "magento":     "magento.txt",
    "shopify":     "shopify.txt",
    "codeigniter": "codeigniter.txt",
    "prestashop":  "prestashop.txt",
    "opencart":    "opencart.txt",
    "vbulletin":   "vbulletin.txt",
    "phpbb":       "phpbb.txt",
}

R="\033[91m";G="\033[92m";Y="\033[93m";B="\033[94m";M="\033[95m";C="\033[96m";W="\033[97m"
DIM="\033[2m";BLD="\033[1m";RST="\033[0m";CL="\033[2K\r"

if IS_WINDOWS:
    os.system("")

def bold(t): return f"{BLD}{t}{RST}"

def banner():
    os.system("cls" if os.name == "nt" else "clear")

    logo = [
        f"{R}           ⛧        ⛧        ⛧{RST}",
        f"{R}      ╔══════════════════════════════╗{RST}",
        f"{R}      ║{RST}   {W}{BLD}MASS REVERSE IP{RST}   {R}║{RST}",
        f"{R}      ║{RST}   {W}{BLD}AUTO CHECK CMS{RST}   {R}║{RST}",
        f"{R}      ╚══════════════════════════════╝{RST}",
        f"{M}           ☠  AnggaTechI  ☠{RST}",
        "",
        f"{C}  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RST}",
        f"{C}  ┃{RST} {Y}Fast Async Lookup{RST} {DIM}•{RST} {G}Auto Check CMS{RST} {DIM}•{RST} {M}AnggaTechI{RST}"
        f"{' ' * 17}{C}┃{RST}",
        f"{C}  ┃{RST} {B}GitHub:{RST} {W}github.com/AnggaTechI{RST}"
        f"{' ' * 37}{C}┃{RST}",
        f"{C}  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RST}",
        ""
    ]

    for line in logo:
        print(line)

def extract_host(raw):
    raw = raw.strip()
    if raw.startswith(("http://", "https://")):
        try:
            return urlparse(raw).hostname or ""
        except Exception:
            return ""
    return raw.split("/")[0]

_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
def is_ip(value): return bool(_IP_RE.match(value))

def ask_yes_no(prompt, default_yes=True):
    hint = f"{DIM}(Y/n){RST}" if default_yes else f"{DIM}(y/N){RST}"
    raw = input(f"  {C}›{RST} {prompt} {hint} : ").strip().lower()
    if not raw:
        return default_yes
    return raw[0] in ("y", "t", "1") 

async def resolve_aiodns(resolver, host):
    try:
        result = await asyncio.wait_for(resolver.query(host, "A"), timeout=DNS_TIMEOUT)
        return result[0].host if result else None
    except Exception:
        return None

async def resolve_asyncio(loop, host):
    try:
        infos = await asyncio.wait_for(
            loop.getaddrinfo(host, None, type=1),
            timeout=DNS_TIMEOUT
        )
        for info in infos:
            ip = info[4][0]
            if is_ip(ip):
                return ip
        return None
    except Exception:
        return None

async def lookup(session, ip):
    try:
        async with session.get(API_URL.format(ip=ip), timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
            data = await resp.json(content_type=None)
            if isinstance(data, list):
                return [i["domain"] for i in data if isinstance(i, dict) and "domain" in i]
            if isinstance(data, dict) and "data" in data:
                return [i["domain"] for i in data["data"] if isinstance(i, dict) and "domain" in i]
            return []
    except Exception:
        return []

_SIG_WP      = re.compile(rb"wp-content|wp-includes|wp-json", re.I)
_SIG_JOOMLA  = re.compile(rb"content=['\"]Joomla!|/media/jui/|/components/com_", re.I)
_SIG_DRUPAL  = re.compile(rb"Drupal\.settings|/sites/default/files/|/sites/all/", re.I)
_SIG_MAGENTO = re.compile(rb"Mage\.Cookies|/skin/frontend/|var BLANK_URL|Magento_", re.I)
_SIG_PRESTA  = re.compile(rb"content=['\"]PrestaShop|var prestashop", re.I)
_SIG_OPENCART= re.compile(rb"catalog/view/theme|route=product/", re.I)
_SIG_VBUL    = re.compile(rb"vBulletin|vbulletin_global\.js", re.I)
_SIG_PHPBB   = re.compile(rb"phpBB|phpbb/styles/", re.I)
_SIG_GEN_LRV = re.compile(rb"<meta name=[\"']csrf-token[\"']", re.I)

def fingerprint(headers, cookies, body):
    found = set()
    server      = headers.get("Server", "").lower()
    generator   = headers.get("X-Generator", "").lower()
    drupal_hdr  = headers.get("X-Drupal-Cache", "") or headers.get("X-Drupal-Dynamic-Cache", "")
    shopify_hdr = headers.get("X-Shopify-Stage", "") or headers.get("X-Shopid", "") or headers.get("X-ShardId", "")
    magento_hdr = headers.get("X-Magento-Cache-Debug", "") or headers.get("X-Magento-Tags", "")

    if "drupal" in generator or drupal_hdr:
        found.add("drupal")
    if shopify_hdr or "shopify" in server:
        found.add("shopify")
    if magento_hdr:
        found.add("magento")

    cookie_names = {ck.key.lower() for ck in cookies.values()} if cookies else set()
    set_cookie_raw = ""
    for h, v in headers.items():
        if h.lower() == "set-cookie":
            set_cookie_raw += v.lower() + ";"
    cookie_blob = set_cookie_raw + " " + " ".join(cookie_names)

    if "laravel_session" in cookie_blob or "xsrf-token" in cookie_blob:
        found.add("laravel")
    if "ci_session" in cookie_blob:
        found.add("codeigniter")
    if "prestashop-" in cookie_blob or "presta-" in cookie_blob:
        found.add("prestashop")
    if "ocsessid" in cookie_blob:
        found.add("opencart")
    if "bbsessionhash" in cookie_blob:
        found.add("vbulletin")
    if "phpbb3_" in cookie_blob or "phpbb_" in cookie_blob:
        found.add("phpbb")

    if body:
        if _SIG_WP.search(body):      found.add("wordpress")
        if _SIG_JOOMLA.search(body):  found.add("joomla")
        if _SIG_DRUPAL.search(body):  found.add("drupal")
        if _SIG_MAGENTO.search(body): found.add("magento")
        if _SIG_PRESTA.search(body):  found.add("prestashop")
        if _SIG_OPENCART.search(body):found.add("opencart")
        if _SIG_VBUL.search(body):    found.add("vbulletin")
        if _SIG_PHPBB.search(body):   found.add("phpbb")
        if "laravel" not in found and _SIG_GEN_LRV.search(body) and b"laravel" in body.lower():
            found.add("laravel")

    return found

async def detect_cms(session, domain):
    for scheme in ("http://", "https://"):
        url = f"{scheme}{domain}/"
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=FP_TIMEOUT),
                allow_redirects=True,
                ssl=False,
                max_redirects=3,
            ) as resp:
                body = await resp.content.read(FP_READ_BYTES)
                return fingerprint(resp.headers, resp.cookies, body or b"")
        except Exception:
            continue
    return set()

class Stats:
    __slots__ = ("lookup_done","fp_done","domain_total","ip_unique","start","last_render","cms_count","cms_enabled")
    def __init__(self, cms_enabled):
        self.lookup_done  = 0
        self.fp_done      = 0
        self.domain_total = 0
        self.ip_unique    = 0
        self.start        = time.time()
        self.last_render  = 0.0
        self.cms_count    = {name: 0 for name in CMS_FILES}
        self.cms_enabled  = cms_enabled

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def _visible_len(s):
    return len(_ANSI_RE.sub('', s))

def render(stats, lookup_total, force=False):
    now = time.time()
    if not force and (now - stats.last_render) < PROGRESS_EVERY:
        return
    stats.last_render = now

    ld, lt = stats.lookup_done, lookup_total
    pct = (ld / lt) * 100 if lt else 0
    bar_len = 20
    filled = int(bar_len * ld / lt) if lt else 0
    bar = f"{G}{'█' * filled}{DIM}{'░' * (bar_len - filled)}{RST}"
    elapsed = now - stats.start
    rps = ld / elapsed if elapsed > 0 else 0

    if stats.cms_enabled:
        top = sorted(stats.cms_count.items(), key=lambda x: -x[1])[:3]
        cms_parts = [f"{DIM}{k[:4]}{RST}{M}{v}{RST}" for k, v in top if v > 0]
        cms_str = " ".join(cms_parts) if cms_parts else f"{DIM}--{RST}"
        tail = f"{DIM}fp{RST}{W}{stats.fp_done}{RST} {cms_str} "
    else:
        tail = ""

    body = (
        f"[{bar}] {Y}{pct:5.1f}%{RST} "
        f"{DIM}lk{RST}{W}{ld}{RST}{DIM}/{lt}{RST} "
        f"{DIM}ip{RST}{C}{stats.ip_unique}{RST} "
        f"{DIM}dom{RST}{W}{stats.domain_total}{RST} "
        f"{tail}"
        f"{DIM}{rps:.0f}r/s{RST}"
    )

    try:
        term_w = shutil.get_terminal_size((120, 20)).columns
    except Exception:
        term_w = 120
    max_w = max(40, term_w - 2)  

    if _visible_len(body) > max_w:
        body = (
            f"[{bar}] {Y}{pct:5.1f}%{RST} "
            f"{DIM}lk{RST}{W}{ld}{RST}{DIM}/{lt}{RST} "
            f"{DIM}ip{RST}{C}{stats.ip_unique}{RST} "
            f"{DIM}dom{RST}{W}{stats.domain_total}{RST} "
            f"{DIM}{rps:.0f}r/s{RST}"
        )

    pad_count = max(0, max_w - _visible_len(body))
    line = "\r " + body + (" " * pad_count)

    sys.stdout.write(line)
    sys.stdout.flush()

class CMSWriter:
    __slots__ = ("files","written")
    def __init__(self):
        self.files   = {}
        self.written = {name: set() for name in CMS_FILES}

    def write(self, cms, domain):
        if domain in self.written[cms]:
            return False
        self.written[cms].add(domain)
        fp = self.files.get(cms)
        if fp is None:
            fp = open(CMS_FILES[cms], "w", encoding="utf-8", buffering=1)
            self.files[cms] = fp
        fp.write(domain + "\n")
        return True

    def close_all(self):
        for fp in self.files.values():
            try: fp.close()
            except Exception: pass

async def lookup_worker(target_q, domain_q, session, resolve_fn, seen_ips, seen_lock,
                        stats, lookup_total, out_fp, written_domains, cms_enabled):
    while True:
        raw = await target_q.get()
        if raw is None:
            target_q.task_done()
            break
        try:
            host = extract_host(raw)
            if not host:
                continue
            ip = host if is_ip(host) else await resolve_fn(host)
            if not ip:
                continue

            async with seen_lock:
                if ip in seen_ips:
                    need_fetch = False
                else:
                    seen_ips[ip] = []
                    need_fetch = True

            if need_fetch:
                domains = await lookup(session, ip)
                async with seen_lock:
                    seen_ips[ip] = domains
                    stats.ip_unique = len(seen_ips)
                for d in domains:
                    if d not in written_domains:
                        written_domains.add(d)
                        out_fp.write(d + "\n")
                        stats.domain_total += 1
                        if cms_enabled:
                            await domain_q.put(d)
        except Exception:
            pass
        finally:
            stats.lookup_done += 1
            render(stats, lookup_total)
            target_q.task_done()

async def fp_worker(domain_q, fp_session, stats, writer, lookup_total):
    while True:
        domain = await domain_q.get()
        if domain is None:
            domain_q.task_done()
            break
        try:
            cms_set = await detect_cms(fp_session, domain)
            for cms in cms_set:
                if writer.write(cms, domain):
                    stats.cms_count[cms] += 1
        except Exception:
            pass
        finally:
            stats.fp_done += 1
            render(stats, lookup_total)
            domain_q.task_done()

async def run(targets, concurrency, cms_enabled):
    lookup_total = len(targets)
    stats        = Stats(cms_enabled)
    seen_ips     = {}
    seen_lock    = asyncio.Lock()
    written_domains = set()
    writer       = CMSWriter() if cms_enabled else None

    target_q = asyncio.Queue(maxsize=concurrency * 4)
    domain_q = asyncio.Queue(maxsize=concurrency * 8) if cms_enabled else None

    loop = asyncio.get_running_loop()
    if aiodns is not None and not IS_WINDOWS:
        resolver = aiodns.DNSResolver(timeout=DNS_TIMEOUT, tries=2)
        async def resolve_fn(host):
            return await resolve_aiodns(resolver, host)
    else:
        async def resolve_fn(host):
            return await resolve_asyncio(loop, host)

    lookup_conn = aiohttp.TCPConnector(
        limit=concurrency, limit_per_host=concurrency,
        ttl_dns_cache=300, use_dns_cache=True,
        enable_cleanup_closed=True,
    )
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RecScan/1.0)"}
    session = aiohttp.ClientSession(connector=lookup_conn, headers=headers)

    fp_session = None
    fp_conn = None
    if cms_enabled:
        fp_conn = aiohttp.TCPConnector(
            limit=concurrency * FP_RATIO, limit_per_host=0,
            ttl_dns_cache=300, use_dns_cache=True,
            enable_cleanup_closed=True, ssl=False,
        )
        fp_session = aiohttp.ClientSession(connector=fp_conn, headers=headers)

    out_fp = open(OUTPUT_ALL, "w", encoding="utf-8", buffering=1)

    try:
        lookup_workers = [
            asyncio.create_task(lookup_worker(
                target_q, domain_q, session, resolve_fn,
                seen_ips, seen_lock, stats, lookup_total, out_fp, written_domains, cms_enabled))
            for _ in range(concurrency)
        ]

        fp_workers = []
        if cms_enabled:
            fp_n = concurrency * FP_RATIO
            fp_workers = [
                asyncio.create_task(fp_worker(
                    domain_q, fp_session, stats, writer, lookup_total))
                for _ in range(fp_n)
            ]

        async def feeder():
            for t in targets:
                await target_q.put(t)
            for _ in range(concurrency):
                await target_q.put(None)
        feeder_task = asyncio.create_task(feeder())

        await feeder_task
        await asyncio.gather(*lookup_workers, return_exceptions=True)

        if cms_enabled:
            for _ in range(len(fp_workers)):
                await domain_q.put(None)
            await asyncio.gather(*fp_workers, return_exceptions=True)
    finally:
        out_fp.close()
        if writer:
            writer.close_all()
        try: await session.close()
        except Exception: pass
        if fp_session:
            try: await fp_session.close()
            except Exception: pass
        await asyncio.sleep(0.25)

    render(stats, lookup_total, force=True)
    elapsed = time.time() - stats.start
    rps = lookup_total / elapsed if elapsed else 0

    print(f"\n\n  {DIM}{'─'*60}{RST}")
    print(f"  {G}[✓] Selesai!{RST}")
    print(f"  {G}▸{RST} Waktu total   : {bold(f'{elapsed:.2f}s')}  {DIM}({rps:.1f} target/s){RST}")
    print(f"  {G}▸{RST} IP unik       : {bold(f'{stats.ip_unique:,}')}")
    print(f"  {G}▸{RST} Domain unik   : {bold(f'{stats.domain_total:,}')}  {DIM}→ {OUTPUT_ALL}{RST}")

    if cms_enabled:
        print(f"  {DIM}{'─'*60}{RST}")
        print(f"  {BLD}{W}[CMS BREAKDOWN]{RST}")
        any_hit = False
        for name in CMS_FILES:
            n = stats.cms_count[name]
            if n > 0:
                any_hit = True
                pct = (n * 100 / stats.domain_total) if stats.domain_total else 0
                print(f"  {M}▸{RST} {name:<12} : {bold(f'{n:,}')} {DIM}({pct:.1f}%) → {CMS_FILES[name]}{RST}")
        if not any_hit:
            print(f"  {DIM}  (tidak ada CMS terdeteksi){RST}")
    print(f"  {DIM}{'─'*60}{RST}\n")

def main():
    banner()
    print(f"  {BLD}{W}[INPUT]{RST}")
    input_file  = input(f"  {C}›{RST} File input  : ").strip()
    cms_enabled = ask_yes_no("Active CMS detection?", default_yes=True)
    conc_inp    = input(f"  {C}›{RST} Concurrency {DIM}(default={DEFAULT_CONC}, max={MAX_CONC}){RST} : ").strip()
    concurrency = int(conc_inp) if conc_inp.isdigit() and int(conc_inp) > 0 else DEFAULT_CONC
    if concurrency > MAX_CONC:
        concurrency = MAX_CONC
    print()

    if not os.path.isfile(input_file):
        print(f"  {R}[✗] File tidak ditemukan:{RST} {input_file}")
        sys.exit(1)

    seen = set()
    targets = []
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line not in seen:
                seen.add(line)
                targets.append(line)

    if not targets:
        print(f"  {R}[✗] GOBLOK.{RST}")
        sys.exit(1)
    print(f"  {DIM}{'─'*60}{RST}")
    print(f"  {G}▸{RST} Total target  : {bold(f'{len(targets):,}')}")
    if cms_enabled:
        print(f"  {G}▸{RST} Mode          : {bold('Reverse IP + CMS Detection')}")
        print(f"  {G}▸{RST} Concurrency   : {bold(str(concurrency))} {DIM}(lookup){RST} + {bold(str(concurrency*FP_RATIO))} {DIM}(fingerprint){RST}")
        print(f"  {M}▸{RST} CMS detected  : {DIM}{', '.join(CMS_FILES.keys())}{RST}")
    else:
        print(f"  {G}▸{RST} Mode          : {bold('Reverse IP only')}")
        print(f"  {G}▸{RST} Concurrency   : {bold(str(concurrency))} {DIM}(lookup){RST}")
    print(f"  {G}▸{RST} Output all    : {bold(OUTPUT_ALL)}")
    print(f"  {DIM}{'─'*60}{RST}\n")
    mode_str = "reverse-ip → Check CMS " if cms_enabled else "reverse-ip only"
    print(f"  {BLD}[PIPELINE]{RST}  {DIM}{mode_str}{RST}\n")

    if IS_WINDOWS:
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        except AttributeError:
            pass

    try:
        asyncio.run(run(targets, concurrency, cms_enabled))
    except KeyboardInterrupt:
        print(f"\n\n  {Y}[!] Dihentikan oleh user.{RST}")
    except Exception as e:
        print(f"\n\n  {R}[✗] Error:{RST} {e}")

if __name__ == "__main__":
    main()
