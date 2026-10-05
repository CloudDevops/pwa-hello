#!/usr/bin/env python3
"""Pull STOCK Act periodic transaction reports (PTRs) from the official sources into JSON.

Sources
  House   https://disclosures-clerk.house.gov  yearly ZIP index + one PDF per filing (text via `pdftotext`)
  Senate  https://efdsearch.senate.gov          search endpoint (JSON) + one HTML table per filing
  President / senior staff  https://www.whitehouse.gov/disclosures/  (OGE Form 278-T PDFs are image scans,
                                                                       so only filing metadata is collected)
  Party / state lookup  https://unitedstates.github.io/congress-legislators/legislators-current.json

Output (all under --out, default ./data)
  house-<year>.json, senate-<year>.json   one record per filing, each with its parsed trades
  president.json                          list of PTR filings published by the White House
  index.json                              what files exist, counts, generation time, source status

Runs are incremental: filings already present in the output files are not fetched again unless the
parser version changed. Only the standard library is used; `pdftotext` (poppler-utils) must be installed.

Usage
  python3 scripts/fetch_trades.py                 # current year + previous year
  python3 scripts/fetch_trades.py --years 2026    # one year only
  python3 scripts/fetch_trades.py --limit 20      # quick smoke test (first 20 new filings per source)
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import http.cookiejar
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile

PARSER_VERSION = 2
UA = "pwa-hello-congress-trades/1.0 (+https://github.com/CloudDevops/pwa-hello)"

HOUSE_ZIP = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
HOUSE_PDF = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf"
SENATE = "https://efdsearch.senate.gov"
WH_DISCLOSURES = "https://www.whitehouse.gov/disclosures/"
LEGISLATORS = "https://unitedstates.github.io/congress-legislators/legislators-current.json"

PARTY = {"Democrat": "D", "Republican": "R", "Independent": "I"}

# House asset-type codes (https://fd.house.gov/reference/asset-type-codes.aspx) -> coarse class
HOUSE_CLASS = {
    "ST": "stock", "OP": "option", "EF": "fund", "MF": "fund", "ET": "fund", "RE": "fund", "RF": "fund",
    "GS": "treasury", "CS": "corp_bond", "AB": "corp_bond", "CT": "crypto",
    "PS": "private", "OI": "private", "OL": "private", "HN": "private", "HE": "private",
}
SENATE_CLASS = {
    "stock": "stock", "stock option": "option", "municipal security": "muni", "corporate bond": "corp_bond",
    "non-public stock": "private", "etf": "fund", "mutual fund": "fund", "cryptocurrency": "crypto",
}
ACTION = {
    "P": "buy", "P (partial)": "buy", "S": "sell", "S (partial)": "sell_partial", "E": "exchange", "E (partial)": "exchange",
    "Purchase": "buy", "Sale (Full)": "sell", "Sale (Partial)": "sell_partial", "Exchange": "exchange",
}
OWNER = {"": "self", "SP": "spouse", "DC": "child", "JT": "joint", "Self": "self", "Spouse": "spouse", "Child": "child", "Joint": "joint"}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------------------- HTTP

def fetch(url: str, *, data=None, headers=None, opener=None, retries: int = 3, timeout: int = 90, pause: float = 0.2) -> bytes:
    hdrs = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        hdrs.update(headers)
    body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=hdrs)
            op = opener or urllib.request.build_opener()
            with op.open(req, timeout=timeout) as resp:
                out = resp.read()
            time.sleep(pause)
            return out
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:  # noqa: PERF203
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"fetch failed for {url}: {last}")


class Cache:
    """Tiny file cache so re-runs during development do not hammer the sources."""

    def __init__(self, root: str):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def get(self, key: str, producer, max_age: float | None = None) -> bytes:
        path = os.path.join(self.root, key)
        if os.path.exists(path):
            age = time.time() - os.path.getmtime(path)
            if max_age is None or age < max_age:
                with open(path, "rb") as fh:
                    return fh.read()
        data = producer()
        with open(path, "wb") as fh:
            fh.write(data)
        return data


# ------------------------------------------------------------------------------------ helpers

def iso_date(us: str | None) -> str | None:
    """'8/21/2026' -> '2026-08-21'. Two-digit years are assumed to be 20xx."""
    if not us:
        return None
    m = re.match(r"\s*(\d{1,2})/(\d{1,2})/(\d{2,4})", us)
    if not m:
        return None
    mo, d, y = (int(x) for x in m.groups())
    if y < 100:
        y += 2000
    try:
        return dt.date(y, mo, d).isoformat()
    except ValueError:
        return None


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", " ", s, flags=re.I)
    return re.sub(r"[^a-z]", "", s.lower())


def parse_amount(raw: str):
    """Return (min, max, cleaned_label). max is None for open-ended brackets."""
    s = re.sub(r"\s+", " ", raw or "").strip()
    nums = [float(n.replace(",", "")) for n in re.findall(r"\$([\d,]+(?:\.\d{1,2})?)", s)]
    if s.startswith("Spouse/DC Over"):
        lo = nums[0] if nums else 1_000_000
        return int(lo), None, f"Spouse/DC Over ${int(lo):,}"
    if s.startswith("Over"):
        lo = nums[0] if nums else None
        return (int(lo) if lo is not None else None), None, s
    if len(nums) >= 2:
        lo, hi = nums[0], nums[1]
        return int(lo), int(hi), f"${int(lo):,} - ${int(hi):,}"
    if len(nums) == 1:
        v = nums[0]
        v = int(v) if v == int(v) else v
        return v, v, f"${v:,}"
    return None, None, s


def parse_options(text: str):
    """Extract call/put, strike and expiry from a description such as
    'Purchased 200 call options with a strike price of $50 and an expiration date of 3/19/27.'
    or the Senate form 'Option Type: Put Strike price: $155.00 Expires: 12/20/2024'."""
    if not text:
        return None
    kind = re.search(r"\b(call|put)\b", text, re.I)
    strike = re.search(r"strike price[:\s]*(?:of\s*)?\$?\s*([\d,]+(?:\.\d+)?)", text, re.I)
    exp = re.search(r"(?:expiration date(?: of)?|expires?|exp\.?)[:\s]*(\d{1,2}/\d{1,2}/\d{2,4})", text, re.I)
    if not kind or not (strike or exp):
        return None
    qty = re.search(r"(\d[\d,]*)\s+(?:call|put)", text, re.I)
    out = {"kind": kind.group(1).lower()}
    if strike:
        out["strike"] = float(strike.group(1).replace(",", ""))
    if exp:
        out["expiry"] = iso_date(exp.group(1))
    if qty:
        out["contracts"] = int(qty.group(1).replace(",", ""))
    return out


def parse_shares(text: str):
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s+shares", text or "", re.I)
    return float(m.group(1).replace(",", "")) if m else None


# --------------------------------------------------------------------------- legislators

def load_legislators(cache: Cache):
    try:
        raw = cache.get("legislators-current.json", lambda: fetch(LEGISLATORS), max_age=6 * 3600)
        people = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        log(f"WARN legislators lookup unavailable: {exc}")
        return {}, {}
    house, senate = {}, {}
    for p in people:
        term = p["terms"][-1]
        name = p["name"].get("official_full") or f"{p['name']['first']} {p['name']['last']}"
        rec = {"name": name, "party": PARTY.get(term.get("party"), term.get("party")), "state": term.get("state"), "bioguide": p.get("id", {}).get("bioguide")}
        if term["type"] == "rep":
            house[(term["state"], int(term.get("district") or 0))] = rec
        else:
            senate.setdefault(norm_name(p["name"]["last"]), []).append((p["name"]["first"], rec))
    return house, senate


def match_senator(senate_lookup, last: str, first: str):
    cands = senate_lookup.get(norm_name(last), [])
    if len(cands) == 1:
        return cands[0][1]
    f = norm_name(first)
    for cfirst, rec in cands:
        if f and (norm_name(cfirst).startswith(f[:3]) or f.startswith(norm_name(cfirst)[:3])):
            return rec
    return None


# ---------------------------------------------------------------------------------- House

HOUSE_FIELDS = ["prefix", "last", "first", "suffix", "filing_type", "state_dst", "year", "filing_date", "doc_id"]


def house_index(year: int, cache: Cache) -> list[dict]:
    raw = cache.get(f"house-{year}FD.zip", lambda: fetch(HOUSE_ZIP.format(year=year)), max_age=1800)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".txt"))
        text = z.read(name).decode("utf-8-sig", errors="replace")
    rows = []
    for line in text.splitlines()[1:]:
        parts = [p.strip() for p in line.rstrip("\r").split("\t")]
        if len(parts) >= 9 and parts[8]:
            rows.append(dict(zip(HOUSE_FIELDS, parts[:9])))
    return rows


def pdf_text(pdf: bytes) -> str:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext not found: install poppler-utils")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
        fh.write(pdf)
        path = fh.name
    try:
        proc = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, timeout=180, check=False)
        return proc.stdout.decode("utf-8", errors="replace")
    finally:
        os.unlink(path)


TYPE_TOKENS = r"P \(partial\)|S \(partial\)|E \(partial\)|P|S|E"
DATE_RE = r"\d{1,2}/\d{1,2}/\d{4}"
AMOUNT_RE = r"\$[\d,]+(?:\.\d{1,2})?(?:\s*-\s*\$?[\d,]*)?|Spouse/DC Over(?:\s*\$[\d,]+)?|Over\s*\$[\d,]+"
TX_RE = re.compile(
    rf"^\s*(?:(?P<owner>SP|DC|JT)\s{{2,}})?(?P<asset>\S.*?)\s+(?P<type>{TYPE_TOKENS})\s+(?P<date>{DATE_RE})\s+(?P<notified>{DATE_RE})\s+(?P<amount>{AMOUNT_RE})(?P<tail>.*)$"
)
LABEL_RE = re.compile(r"^\s+(?P<label>F\s+S|S\s+O|D|L|C)\s*:\s?(?P<value>.*)$")
SKIP_RE = re.compile(r"^\s*(ID\s+Owner\s+Asset|Type\s+Date|\$200\?|\*\s*For the complete list|Filing ID #|Clerk of the House)")
LABELS = {"FS": "status", "SO": "account", "D": "note", "L": "location", "C": "comment"}


def split_asset(asset: str):
    """'Bloom Energy Corporation Class A Common Stock (BE) [ST]' -> (name, 'BE', 'ST')"""
    asset = re.sub(r"\s+", " ", asset).strip()
    code = None
    m = re.search(r"\[([A-Z0-9]{2})\]\s*$", asset)
    if m:
        code = m.group(1)
        asset = asset[: m.start()].strip()
    ticker = None
    m = re.search(r"\(([^()]+)\)\s*$", asset)
    if m:
        cand = re.sub(r"^(?:Ticker:\s*|CRYPTO:\s*)", "", m.group(1).strip(), flags=re.I)
        if re.fullmatch(r"[A-Z][A-Z0-9.\-$]{0,9}", cand):
            ticker = cand
            asset = asset[: m.start()].strip(" -")
    return asset, ticker, code


def parse_house_text(text: str) -> list[dict]:
    """Parse the `pdftotext -layout` output of an e-filed House PTR into trade dicts."""
    trades: list[dict] = []
    cur: dict | None = None
    mode = None  # 'asset' (asset/amount continuation) or 'label'
    last_label = None
    type_col = amount_col = 0

    def finish():
        nonlocal cur
        if not cur:
            return
        name, ticker, code = split_asset(cur.pop("_asset"))
        lo, hi, label = parse_amount(cur.pop("_amount"))
        note = re.sub(r"\s+", " ", cur.get("note", "")).strip()
        rec = {
            "owner": OWNER.get(cur.pop("_owner") or "", "self"),
            "asset": name,
            "ticker": ticker,
            "asset_code": code,
            "asset_class": HOUSE_CLASS.get(code or "", "other"),
            "action": ACTION.get(cur.pop("_type"), "other"),
            "date": iso_date(cur.pop("_date")),
            "notified": iso_date(cur.pop("_notified")),
            "amount": label,
            "min": lo,
            "max": hi,
            "note": note or None,
            "status": cur.get("status") if cur.get("status") not in (None, "", "New") else None,
            "account": re.sub(r"\s+", " ", cur["account"]).strip() if cur.get("account") else None,
            "comment": re.sub(r"\s+", " ", cur["comment"]).strip() if cur.get("comment") else None,
            "options": parse_options(note + " " + name),
            "shares": parse_shares(note),
        }
        trades.append(compact(rec))
        cur = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if mode == "label":
                mode = None
            continue
        if SKIP_RE.match(line):
            continue
        m = TX_RE.match(line)
        if m:
            finish()
            type_col, amount_col = m.start("type"), m.start("amount")
            cur = {
                "_owner": m.group("owner"),
                "_asset": m.group("asset"),
                "_type": m.group("type"),
                "_date": m.group("date"),
                "_notified": m.group("notified"),
                "_amount": m.group("amount"),
            }
            mode = "asset"
            continue
        if cur is None:
            continue
        lm = LABEL_RE.match(line)
        if lm:
            key = LABELS[re.sub(r"\s+", "", lm.group("label"))]
            cur[key] = lm.group("value").strip()
            last_label = key
            mode = "label"
            continue
        if mode == "asset":
            # Wrapped rows: the asset name continues in its column and a wrapped amount bracket
            # (e.g. "$50,000" after "$15,001 -") sits in the amount column at the far right. The asset
            # column can be wider than the type column in some layouts, so cut near the amount column.
            cut = max(amount_col - 4, type_col + 1)
            right = line[cut:].strip()
            if right and (right.startswith("$") or re.fullmatch(r"[\d,]+(?:\.\d{1,2})?", right)):
                cur["_amount"] += " " + right
                left = line[:cut].strip()
            else:
                left = line.strip()
            if left:
                cur["_asset"] += " " + left
            continue
        if mode == "label" and last_label:
            cur[last_label] = (cur.get(last_label, "") + " " + line.strip()).strip()
    finish()
    return trades


def update_house(year: int, out_dir: str, cache: Cache, house_lookup, limit: int | None) -> dict:
    path = os.path.join(out_dir, f"house-{year}.json")
    existing = load_json(path) or {}
    filings = {f["id"]: f for f in existing.get("filings", [])}
    index = [r for r in house_index(year, cache) if r["filing_type"] == "P"]
    todo = [r for r in index if r["doc_id"] not in filings or filings[r["doc_id"]].get("parser", 0) < PARSER_VERSION]
    if limit:
        todo = todo[:limit]
    log(f"House {year}: {len(index)} PTR filings in index, {len(todo)} to fetch")
    for i, row in enumerate(todo, 1):
        doc_id = row["doc_id"]
        url = HOUSE_PDF.format(year=year, doc_id=doc_id)
        try:
            pdf = cache.get(f"house-{year}-{doc_id}.pdf", lambda: fetch(url))
            text = pdf_text(pdf)
        except Exception as exc:  # noqa: BLE001
            log(f"  WARN {doc_id}: {exc}")
            continue
        scanned = len(text.strip()) < 200 or "Filing ID" not in text
        trades = [] if scanned else parse_house_text(text)
        state = row["state_dst"][:2]
        district = int(row["state_dst"][2:]) if row["state_dst"][2:].isdigit() else None
        who = house_lookup.get((state, district)) if district is not None else None
        status = re.search(r"^Status:\s*(.+)$", text, re.M)
        filing = {
            "id": doc_id,
            "chamber": "house",
            "url": url,
            "filed": iso_date(row["filing_date"]),
            "name": who["name"] if who else " ".join(x for x in (row["first"], row["last"], row["suffix"]) if x),
            "last": row["last"],
            "first": row["first"],
            "state": state,
            "district": district,
            "party": who["party"] if who else None,
            "bioguide": who["bioguide"] if who else None,
            "status": status.group(1).strip() if status else None,
            "amendment": any(t.get("status") == "Amended" for t in trades),
            "scanned": scanned,
            "parser": PARSER_VERSION,
            "trades": trades,
        }
        filings[doc_id] = compact(filing) | {"trades": trades}
        if i % 25 == 0:
            log(f"  {i}/{len(todo)} filings fetched")
    data = {
        "chamber": "house",
        "year": year,
        "generated": now_iso(),
        "source": HOUSE_ZIP.format(year=year),
        "filings": sorted(filings.values(), key=lambda f: (f["filed"] or "", f["id"]), reverse=True),
    }
    return summarize(save_if_changed(path, data, existing))


# --------------------------------------------------------------------------------- Senate

class SenateClient:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.csrf = None

    def handshake(self) -> None:
        home = fetch(f"{SENATE}/search/home/", opener=self.opener).decode("utf-8", "replace")
        m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', home)
        if not m:
            raise RuntimeError("Senate eFD: csrf token not found on home page")
        fetch(
            f"{SENATE}/search/home/",
            opener=self.opener,
            data={"csrfmiddlewaretoken": m.group(1), "prohibition_agreement": "1"},
            headers={"Referer": f"{SENATE}/search/home/"},
        )
        self.csrf = next((c.value for c in self.jar if c.name == "csrftoken"), m.group(1))

    def search_ptrs(self, start: str, end: str) -> list[list[str]]:
        rows: list[list[str]] = []
        offset = 0
        while True:
            form = {
                "start": offset, "length": 100, "report_types": "[11]", "filer_types": "[1]",
                "submitted_start_date": f"{start} 00:00:00", "submitted_end_date": f"{end} 23:59:59" if end else "",
                "candidate_state": "", "senator_state": "", "office_id": "", "first_name": "", "last_name": "",
                "draw": 1, "order[0][column]": 4, "order[0][dir]": "desc",
            }
            raw = fetch(
                f"{SENATE}/search/report/data/",
                opener=self.opener,
                data=form,
                headers={"Referer": f"{SENATE}/search/", "X-CSRFToken": self.csrf or "", "X-Requested-With": "XMLHttpRequest"},
            )
            page = json.loads(raw)
            rows.extend(page.get("data", []))
            offset += 100
            if not page.get("data") or offset >= int(page.get("recordsTotal", 0)):
                return rows

    def page(self, path: str) -> str:
        return fetch(f"{SENATE}{path}", opener=self.opener, headers={"Referer": f"{SENATE}/search/"}).decode("utf-8", "replace")


def strip_tags(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def parse_senate_html(page: str) -> list[dict]:
    tables = re.findall(r"<table.*?</table>", page, flags=re.S)
    if not tables:
        return []
    trades = []
    for row in re.findall(r"<tr.*?</tr>", tables[0], flags=re.S)[1:]:
        cells = [strip_tags(c) for c in re.findall(r"<t[hd].*?</t[hd]>", row, flags=re.S)]
        if len(cells) < 8:
            continue
        _, date, owner, ticker, asset, asset_type, ttype, amount = cells[:8]
        comment = cells[8] if len(cells) > 8 else ""
        lo, hi, label = parse_amount(amount)
        rec = {
            "owner": OWNER.get(owner, owner.lower() or "self"),
            "asset": asset,
            "ticker": None if ticker in ("--", "") else ticker,
            "asset_code": asset_type,
            "asset_class": SENATE_CLASS.get(asset_type.lower(), "other"),
            "action": ACTION.get(ttype, "other"),
            "date": iso_date(date),
            "amount": label,
            "min": lo,
            "max": hi,
            "note": comment if comment and comment != "--" else None,
            "options": parse_options(asset + " " + comment),
        }
        trades.append(compact(rec))
    return trades


def update_senate(year: int, out_dir: str, cache: Cache, senate_lookup, client: SenateClient, limit: int | None) -> dict:
    path = os.path.join(out_dir, f"senate-{year}.json")
    existing = load_json(path) or {}
    filings = {f["id"]: f for f in existing.get("filings", [])}
    rows = client.search_ptrs(f"01/01/{year}", f"12/31/{year}")
    todo = []
    for first, last, display, link, filed in rows:
        m = re.search(r'href="([^"]+)"', link)
        if not m:
            continue
        href = m.group(1)
        fid = href.rstrip("/").rsplit("/", 1)[-1]
        if fid in filings and filings[fid].get("parser", 0) >= PARSER_VERSION:
            continue
        todo.append((fid, href, first, last, display, strip_tags(link), filed))
    if limit:
        todo = todo[:limit]
    log(f"Senate {year}: {len(rows)} PTR filings listed, {len(todo)} to fetch")
    for i, (fid, href, first, last, display, title, filed) in enumerate(todo, 1):
        paper = "/paper/" in href
        trades: list[dict] = []
        if not paper:
            try:
                page = cache.get(f"senate-{fid}.html", lambda: client.page(href).encode()).decode("utf-8", "replace")
                trades = parse_senate_html(page)
            except Exception as exc:  # noqa: BLE001
                log(f"  WARN {fid}: {exc}")
                continue
        who = match_senator(senate_lookup, last, first)
        filings[fid] = compact({
            "id": fid,
            "chamber": "senate",
            "url": f"{SENATE}{href}",
            "filed": iso_date(filed),
            "name": who["name"] if who else f"{first} {last}".strip(),
            "last": last,
            "first": first,
            "state": who["state"] if who else None,
            "party": who["party"] if who else None,
            "bioguide": who["bioguide"] if who else None,
            "status": "Senator",
            "title": title,
            "amendment": "Amendment" in title,
            "scanned": paper,
            "parser": PARSER_VERSION,
        }) | {"trades": trades}
        if i % 25 == 0:
            log(f"  {i}/{len(todo)} filings fetched")
    data = {
        "chamber": "senate",
        "year": year,
        "generated": now_iso(),
        "source": f"{SENATE}/search/",
        "filings": sorted(filings.values(), key=lambda f: (f["filed"] or "", f["id"]), reverse=True),
    }
    return summarize(save_if_changed(path, data, existing))


# ------------------------------------------------------------------------------ President

def update_president(out_dir: str) -> dict:
    path = os.path.join(out_dir, "president.json")
    page = fetch(WH_DISCLOSURES).decode("utf-8", "replace")
    links = sorted(set(re.findall(r'href="(https://www\.whitehouse\.gov/wp-content/uploads/[^"]*Periodic-Transaction-Report[^"]*\.pdf)"', page)))
    filings = []
    for url in links:
        fn = url.rsplit("/", 1)[-1]
        filer = fn.split("-Periodic-Transaction-Report")[0].replace("-", " ").replace(".", ". ")
        filer = re.sub(r"\s+", " ", filer).strip()
        tail = fn.split("Periodic-Transaction-Report", 1)[-1]
        nums = [int(x) for x in re.findall(r"\d+", tail)]
        if nums and nums[0] == 0:
            nums = nums[1:]
        date = None
        if len(nums) >= 3:
            mo, d, y = nums[0], nums[1], nums[2]
            y = y + 2000 if y < 100 else y
            try:
                date = dt.date(y, mo, d).isoformat()
            except ValueError:
                date = None
        if not date:
            m = re.search(r"/uploads/(\d{4})/(\d{2})/", url)
            date = f"{m.group(1)}-{m.group(2)}-01" if m else None
        filings.append({
            "filer": filer,
            "president": fn.startswith("President-"),
            "date": date,
            "part": nums[3] if len(nums) > 3 else None,
            "amendment": "Amendment" in tail,
            "url": url,
            "file": fn,
        })
    filings.sort(key=lambda f: (f["date"] or "", f["part"] or 0), reverse=True)
    data = {
        "generated": now_iso(),
        "source": WH_DISCLOSURES,
        "note": "OGE Form 278-T PTRs published by the White House are image scans; transactions are not machine-parsed here.",
        "filings": filings,
    }
    filings = save_if_changed(path, data, load_json(path))["filings"]
    return {"filings": len(filings), "president_filings": sum(1 for f in filings if f["president"]), "ok": True}


# ----------------------------------------------------------------------------------- misc

def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def compact(d: dict) -> dict:
    """Drop None/False/empty values so the JSON stays small."""
    return {k: v for k, v in d.items() if v not in (None, False, "", [], {})}


def save_if_changed(path: str, data: dict, existing: dict | None) -> dict:
    """Write the file only when its filings differ from what is already on disk.

    The per-file `generated` stamp would otherwise change on every run and make the daily
    workflow commit multi-megabyte files that carry no new information. index.json still
    records when the sources were last checked."""
    if existing and existing.get("filings") == data.get("filings"):
        return existing
    save_json(path, data)
    return data


def load_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


def summarize(data: dict) -> dict:
    filings = data["filings"]
    return {
        "ok": True,
        "filings": len(filings),
        "trades": sum(len(f["trades"]) for f in filings),
        "scanned": sum(1 for f in filings if f.get("scanned")),
        "latest_filed": max((f["filed"] or "" for f in filings), default=None),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    today = dt.date.today()
    ap.add_argument("--years", nargs="*", type=int, default=[today.year, today.year - 1])
    ap.add_argument("--out", default="data")
    ap.add_argument("--cache", default=".cache/trades")
    ap.add_argument("--limit", type=int, default=None, help="max new filings per source (smoke tests)")
    ap.add_argument("--skip-house", action="store_true")
    ap.add_argument("--skip-senate", action="store_true")
    ap.add_argument("--skip-president", action="store_true")
    args = ap.parse_args(argv)

    cache = Cache(args.cache)
    os.makedirs(args.out, exist_ok=True)
    house_lookup, senate_lookup = load_legislators(cache)
    index = load_json(os.path.join(args.out, "index.json")) or {}
    status = index.get("sources", {})
    years = sorted(set(args.years), reverse=True)
    failures = 0

    for year in years:
        if not args.skip_house:
            try:
                status[f"house-{year}"] = update_house(year, args.out, cache, house_lookup, args.limit)
            except Exception as exc:  # noqa: BLE001
                failures += 1
                log(f"ERROR house {year}: {exc}")
                status[f"house-{year}"] = {"ok": False, "error": str(exc), "at": now_iso()}
    if not args.skip_senate:
        client = SenateClient()
        try:
            client.handshake()
            for year in years:
                try:
                    status[f"senate-{year}"] = update_senate(year, args.out, cache, senate_lookup, client, args.limit)
                except Exception as exc:  # noqa: BLE001
                    failures += 1
                    log(f"ERROR senate {year}: {exc}")
                    status[f"senate-{year}"] = {"ok": False, "error": str(exc), "at": now_iso()}
        except Exception as exc:  # noqa: BLE001
            failures += 1
            log(f"ERROR senate handshake: {exc}")
            status["senate"] = {"ok": False, "error": str(exc), "at": now_iso()}
    if not args.skip_president:
        try:
            status["president"] = update_president(args.out)
        except Exception as exc:  # noqa: BLE001
            log(f"ERROR president: {exc}")
            status["president"] = {"ok": False, "error": str(exc), "at": now_iso()}

    files = {}
    for name in sorted(os.listdir(args.out)):
        m = re.match(r"(house|senate)-(\d{4})\.json$", name)
        if m:
            files.setdefault(m.group(2), {})[m.group(1)] = name
    index = {
        "generated": now_iso(),
        "parser": PARSER_VERSION,
        "years": sorted(files, reverse=True),
        "files": files,
        "president": "president.json" if os.path.exists(os.path.join(args.out, "president.json")) else None,
        "sources": status,
    }
    save_json(os.path.join(args.out, "index.json"), index)
    log("index: " + json.dumps({k: v for k, v in index.items() if k != "sources"}))
    for k, v in status.items():
        log(f"  {k}: {v}")
    return 1 if failures and failures >= len(years) * 2 else 0


if __name__ == "__main__":
    sys.exit(main())
