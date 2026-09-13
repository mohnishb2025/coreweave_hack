"""Generate the compact, deterministic Repair Loop benchmark corpus."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).parent / "cases"


CASES = [
    {
        "id": "01_clamp_boundary",
        "difficulty": "easy",
        "tags": ["boundary", "math"],
        "files": {
            "clamp.py": """def clamp(value, low, high):
    if value >= high:
        return high - 1
    return max(low, value)
""",
            "tests/test_clamp.py": """from clamp import clamp

def test_upper_boundary_is_inclusive():
    assert clamp(10, 0, 10) == 10
""",
            "../hidden_tests/test_regression.py": """from clamp import clamp

def test_values_above_upper_boundary():
    assert clamp(99, 0, 10) == 10
""",
        },
        "expected": "tests/test_clamp.py::test_upper_boundary_is_inclusive",
        "reason": "The inclusive upper bound is reduced by one.",
    },
    {
        "id": "02_mutable_default",
        "difficulty": "easy",
        "tags": ["mutable-state", "state-leak"],
        "files": {
            "collector.py": """def collect(item, items=[]):
    items.append(item)
    return list(items)
""",
            "tests/test_collector.py": """from collector import collect

def test_calls_are_independent():
    assert collect("a") == ["a"]
    assert collect("b") == ["b"]
""",
            "../hidden_tests/test_regression.py": """from collector import collect

def test_three_fresh_calls():
    assert [collect(i) for i in range(3)] == [[0], [1], [2]]
""",
        },
        "expected": "tests/test_collector.py::test_calls_are_independent",
        "reason": "A mutable default leaks values between calls.",
    },
    {
        "id": "03_csv_parsing",
        "difficulty": "medium",
        "tags": ["parsing", "csv"],
        "files": {
            "records.py": """def parse_row(line):
    name, city = line.strip().split(",")
    return {"name": name.strip('"'), "city": city.strip('"')}
""",
            "tests/test_records.py": """from records import parse_row

def test_quoted_comma():
    assert parse_row('"Doe, Jane","Austin"') == {"name": "Doe, Jane", "city": "Austin"}
""",
            "../hidden_tests/test_regression.py": """from records import parse_row

def test_escaped_quote():
    assert parse_row('"A ""quoted"" name","Rome"')["name"] == 'A "quoted" name'
""",
        },
        "expected": "tests/test_records.py::test_quoted_comma",
        "reason": "Naive comma splitting does not implement CSV quoting.",
    },
    {
        "id": "04_async_lookup",
        "difficulty": "easy",
        "tags": ["async", "await"],
        "files": {
            "lookup.py": """async def fetch_name(client, user_id):
    response = client.get(user_id)
    return response["name"]
""",
            "tests/test_lookup.py": """import asyncio
from lookup import fetch_name

class Client:
    async def get(self, user_id):
        return {"name": f"user-{user_id}"}

def test_fetch_name_awaits_client():
    assert asyncio.run(fetch_name(Client(), 7)) == "user-7"
""",
            "../hidden_tests/test_regression.py": """import asyncio
from lookup import fetch_name

class Client:
    async def get(self, user_id):
        return {"name": f"user-{user_id}"}

def test_second_identifier():
    assert asyncio.run(fetch_name(Client(), 9)) == "user-9"
""",
        },
        "expected": "tests/test_lookup.py::test_fetch_name_awaits_client",
        "reason": "The asynchronous client call is not awaited.",
    },
    {
        "id": "05_wrong_exception",
        "difficulty": "easy",
        "tags": ["exceptions", "validation"],
        "files": {
            "users.py": """def require_email(record):
    if "email" not in record:
        raise KeyError("email is required")
    return record["email"]
""",
            "tests/test_users.py": """import pytest
from users import require_email

def test_missing_email_is_validation_error():
    with pytest.raises(ValueError, match="email is required"):
        require_email({})
""",
            "../hidden_tests/test_regression.py": """import pytest
from users import require_email

def test_error_is_not_mapping_leak():
    with pytest.raises(ValueError):
        require_email({"name": "Ada"})
""",
        },
        "expected": "tests/test_users.py::test_missing_email_is_validation_error",
        "reason": "Validation raises KeyError instead of ValueError.",
    },
    {
        "id": "06_snake_case",
        "difficulty": "medium",
        "tags": ["transformation", "strings"],
        "files": {
            "naming.py": """import re

def snake_case(value):
    return re.sub(r"([A-Z])", r"_\\1", value).strip("_").lower()
""",
            "tests/test_naming.py": """from naming import snake_case

def test_acronym_is_one_word():
    assert snake_case("HTTPServer") == "http_server"
""",
            "../hidden_tests/test_regression.py": """from naming import snake_case

def test_identifier_with_acronym():
    assert snake_case("parseJSONValue") == "parse_json_value"
""",
        },
        "expected": "tests/test_naming.py::test_acronym_is_one_word",
        "reason": "Every acronym letter receives its own separator.",
    },
    {
        "id": "07_pagination_multifile",
        "difficulty": "medium",
        "tags": ["boundary", "multi-file", "pagination"],
        "files": {
            "pager/__init__.py": """from .service import page_count
""",
            "pager/math.py": """def divide_round_up(total, size):
    return total // size
""",
            "pager/service.py": """from .math import divide_round_up

def page_count(items, page_size):
    return divide_round_up(len(items), page_size)
""",
            "tests/test_pager.py": """from pager import page_count

def test_partial_page_counts():
    assert page_count(list(range(11)), 10) == 2
""",
            "../hidden_tests/test_regression.py": """from pager import page_count

def test_single_partial_page():
    assert page_count([1], 10) == 1
""",
        },
        "expected": "tests/test_pager.py::test_partial_page_counts",
        "reason": "Shared division helper truncates partial pages.",
    },
    {
        "id": "08_cache_multifile",
        "difficulty": "hard",
        "tags": ["mutable-state", "multi-file", "cache"],
        "files": {
            "store/__init__.py": """from .service import cached_profile
""",
            "store/cache.py": """CACHE = {}

def put(key, value):
    CACHE[key] = value
    return value
""",
            "store/service.py": """from .cache import CACHE, put

def cached_profile(user_id, loader):
    profile = CACHE.get(user_id)
    if not profile:
        profile = put(user_id, loader(user_id))
    return profile
""",
            "tests/test_cache.py": """from store import cached_profile

def test_falsey_profile_is_cached():
    calls = []
    loader = lambda key: calls.append(key) or {}
    cached_profile("u", loader)
    cached_profile("u", loader)
    assert calls == ["u"]
""",
            "../hidden_tests/test_regression.py": """from store import cached_profile

def test_none_value_is_cached():
    calls = []
    loader = lambda key: calls.append(key)
    cached_profile("none", loader)
    cached_profile("none", loader)
    assert calls == ["none"]
""",
        },
        "expected": "tests/test_cache.py::test_falsey_profile_is_cached",
        "reason": "Truthiness is mistaken for cache membership.",
    },
    {
        "id": "09_config_multifile",
        "difficulty": "medium",
        "tags": ["parsing", "multi-file", "configuration"],
        "files": {
            "config/__init__.py": """from .loader import load_flag
""",
            "config/parser.py": """def parse_bool(raw):
    return bool(raw)
""",
            "config/loader.py": """from .parser import parse_bool

def load_flag(env, name, default=False):
    return parse_bool(env[name]) if name in env else default
""",
            "tests/test_config.py": """from config import load_flag

def test_false_string():
    assert load_flag({"FEATURE": "false"}, "FEATURE") is False
""",
            "../hidden_tests/test_regression.py": """from config import load_flag

def test_zero_string():
    assert load_flag({"FEATURE": "0"}, "FEATURE") is False
""",
        },
        "expected": "tests/test_config.py::test_false_string",
        "reason": "Non-empty false-like strings are treated as true.",
    },
    {
        "id": "10_chunk_boundary",
        "difficulty": "easy",
        "tags": ["boundary", "collections"],
        "files": {
            "chunks.py": """def chunks(values, size):
    return [values[i:i + size] for i in range(0, len(values) - size, size)]
""",
            "tests/test_chunks.py": """from chunks import chunks

def test_exact_chunk_is_retained():
    assert chunks([1, 2], 2) == [[1, 2]]
""",
            "../hidden_tests/test_regression.py": """from chunks import chunks

def test_final_partial_chunk():
    assert chunks([1, 2, 3], 2) == [[1, 2], [3]]
""",
        },
        "expected": "tests/test_chunks.py::test_exact_chunk_is_retained",
        "reason": "The range stop drops exact and trailing chunks.",
    },
    {
        "id": "11_stable_dedupe",
        "difficulty": "easy",
        "tags": ["transformation", "ordering"],
        "files": {
            "dedupe.py": """def unique(values):
    return list(set(values))
""",
            "tests/test_dedupe.py": """from dedupe import unique

def test_first_seen_order_is_preserved():
    assert unique([3, 1, 3, 2]) == [3, 1, 2]
""",
            "../hidden_tests/test_regression.py": """from dedupe import unique

def test_string_order():
    assert unique(["z", "a", "z", "m"]) == ["z", "a", "m"]
""",
        },
        "expected": "tests/test_dedupe.py::test_first_seen_order_is_preserved",
        "reason": "Set conversion destroys first-seen ordering.",
    },
    {
        "id": "12_iso_timestamp",
        "difficulty": "medium",
        "tags": ["parsing", "datetime"],
        "files": {
            "timestamps.py": """from datetime import datetime

def parse_timestamp(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
""",
            "tests/test_timestamps.py": """from datetime import timezone
from timestamps import parse_timestamp

def test_utc_z_suffix():
    assert parse_timestamp("2025-01-02T03:04:05Z").tzinfo == timezone.utc
""",
            "../hidden_tests/test_regression.py": """from timestamps import parse_timestamp

def test_offset_suffix():
    assert parse_timestamp("2025-01-02T03:04:05+02:00").utcoffset().total_seconds() == 7200
""",
        },
        "expected": "tests/test_timestamps.py::test_utc_z_suffix",
        "reason": "The parser rejects ISO-8601 timezone suffixes.",
    },
    {
        "id": "13_async_retry",
        "difficulty": "medium",
        "tags": ["async", "boundary", "retry"],
        "files": {
            "retry.py": """async def retry(operation, retries):
    for _ in range(retries):
        try:
            return await operation()
        except RuntimeError:
            pass
    raise RuntimeError("exhausted")
""",
            "tests/test_retry.py": """import asyncio
from retry import retry

def test_retries_means_extra_attempts():
    attempts = 0
    async def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("temporary")
        return "ok"
    assert asyncio.run(retry(operation, retries=1)) == "ok"
""",
            "../hidden_tests/test_regression.py": """import asyncio
from retry import retry

def test_zero_retries_still_attempts_once():
    async def operation():
        return 42
    assert asyncio.run(retry(operation, retries=0)) == 42
""",
        },
        "expected": "tests/test_retry.py::test_retries_means_extra_attempts",
        "reason": "Retries are counted as total attempts instead of extra attempts.",
    },
    {
        "id": "14_extension_transform",
        "difficulty": "easy",
        "tags": ["transformation", "paths"],
        "files": {
            "paths.py": """def replace_extension(path, extension):
    stem = path.split(".")[0]
    return f"{stem}.{extension.lstrip('.')}"
""",
            "tests/test_paths.py": """from paths import replace_extension

def test_dotted_directory_and_filename():
    assert replace_extension("archive.v1/report.final.txt", "json") == "archive.v1/report.final.json"
""",
            "../hidden_tests/test_regression.py": """from paths import replace_extension

def test_hidden_file():
    assert replace_extension(".env", "example") == ".env.example"
""",
        },
        "expected": "tests/test_paths.py::test_dotted_directory_and_filename",
        "reason": "Splitting on the first dot corrupts dotted paths.",
    },
    {
        "id": "15_inventory_multifile",
        "difficulty": "hard",
        "tags": ["mutable-state", "multi-file", "domain"],
        "files": {
            "inventory/__init__.py": """from .service import reserve
""",
            "inventory/model.py": """def snapshot(stock):
    return stock
""",
            "inventory/service.py": """from .model import snapshot

def reserve(stock, sku, amount):
    before = snapshot(stock)
    stock[sku] -= amount
    return before, stock
""",
            "tests/test_inventory.py": """from inventory import reserve

def test_before_snapshot_is_unchanged():
    before, after = reserve({"widget": 5}, "widget", 2)
    assert before == {"widget": 5}
    assert after == {"widget": 3}
""",
            "../hidden_tests/test_regression.py": """from inventory import reserve

def test_snapshots_are_distinct_objects():
    before, after = reserve({"x": 2}, "x", 1)
    assert before is not after
""",
        },
        "expected": "tests/test_inventory.py::test_before_snapshot_is_unchanged",
        "reason": "The snapshot aliases the live mutable stock mapping.",
    },
    {
        "id": "16_interval_merge_unsorted",
        "difficulty": "hard",
        "tags": ["boundary", "collections", "ordering"],
        "files": {
            "intervals.py": """def merge(ranges):
    ranges = [list(item) for item in ranges]
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
""",
            "tests/test_intervals.py": """from intervals import merge

def test_overlapping_out_of_order_ranges_collapse():
    assert merge([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]
""",
            "../hidden_tests/test_regression.py": """from intervals import merge

def test_touching_and_contained_ranges():
    assert merge([[5, 5], [1, 4], [4, 7], [15, 18]]) == [[1, 7], [15, 18]]
""",
        },
        "expected": "tests/test_intervals.py::test_overlapping_out_of_order_ranges_collapse",
        "reason": "Intervals are merged in list order instead of after sorting by start.",
    },
    {
        "id": "17_rate_limit_window",
        "difficulty": "hard",
        "tags": ["boundary", "time", "multi-file"],
        "files": {
            "limiter/__init__.py": """from .policy import accept
""",
            "limiter/window.py": """def recent(history, now, window):
    return [stamp for stamp in history if now - stamp < window]
""",
            "limiter/policy.py": """from .window import recent

def accept(history, now, limit, window):
    history.append(now)
    return len(recent(history, now, window)) <= limit
""",
            "tests/test_limiter.py": """from limiter import accept

def test_event_on_window_boundary_still_counts():
    history = [0, 4]
    assert accept(history, 10, limit=3, window=10) is True
    assert accept([0, 4, 10], 10, limit=3, window=10) is False
""",
            "../hidden_tests/test_regression.py": """from limiter import accept

def test_zero_window_is_exact_timestamp_only():
    assert accept([], 5, limit=1, window=0) is True
    assert accept([5], 5, limit=1, window=0) is False
    assert accept([4], 5, limit=1, window=0) is True
""",
        },
        "expected": "tests/test_limiter.py::test_event_on_window_boundary_still_counts",
        "reason": "The sliding window uses a strict inequality, so boundary events are ignored.",
    },
    {
        "id": "18_atomic_transfer",
        "difficulty": "hard",
        "tags": ["mutable-state", "multi-file", "transactions"],
        "files": {
            "bank/__init__.py": """from .ledger import transfer
""",
            "bank/accounts.py": """def copy_accounts(accounts):
    return accounts
""",
            "bank/ledger.py": """from .accounts import copy_accounts

def transfer(accounts, source, dest, amount):
    working = copy_accounts(accounts)
    working[source] -= amount
    if working[source] < 0:
        raise ValueError("insufficient funds")
    working[dest] += amount
    return working
""",
            "tests/test_bank.py": """import pytest
from bank import transfer

def test_failed_transfer_does_not_debit_source():
    start = {"a": 10, "b": 1}
    with pytest.raises(ValueError, match="insufficient"):
        transfer(start, "a", "b", 15)
    assert start == {"a": 10, "b": 1}
""",
            "../hidden_tests/test_regression.py": """from bank import transfer

def test_successful_transfer_does_not_alias_input():
    start = {"a": 10, "b": 1}
    result = transfer(start, "a", "b", 4)
    assert result == {"a": 6, "b": 5}
    assert start == {"a": 10, "b": 1}
    assert result is not start
""",
        },
        "expected": "tests/test_bank.py::test_failed_transfer_does_not_debit_source",
        "reason": "The ledger mutates the caller's mapping before the insufficient-funds check.",
    },
    {
        "id": "19_topo_cycle",
        "difficulty": "hard",
        "tags": ["graph", "ordering", "exceptions"],
        "files": {
            "schedule.py": """def order(graph):
    remaining = {node: set(deps) for node, deps in graph.items()}
    done = []
    while remaining:
        ready = [node for node, deps in remaining.items() if not deps]
        if not ready:
            break
        node = sorted(ready)[0]
        done.append(node)
        del remaining[node]
        for deps in remaining.values():
            deps.discard(node)
    return done
""",
            "tests/test_schedule.py": """import pytest
from schedule import order

def test_cycle_is_an_error():
    with pytest.raises(ValueError, match="cycle"):
        order({"build": ["test"], "test": ["build"]})
""",
            "../hidden_tests/test_regression.py": """from schedule import order

def test_diamond_dependencies_keep_prereqs_first():
    result = order({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []})
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")
""",
        },
        "expected": "tests/test_schedule.py::test_cycle_is_an_error",
        "reason": "A cyclic dependency returns a partial order instead of raising.",
    },
    {
        "id": "20_json_pointer",
        "difficulty": "hard",
        "tags": ["parsing", "transformation", "encoding"],
        "files": {
            "pointer.py": """def resolve(document, pointer):
    current = document
    for part in pointer.lstrip("/").split("/"):
        current = current[part]
    return current
""",
            "tests/test_pointer.py": """from pointer import resolve

def test_escaped_slash_is_one_key():
    document = {"a/b": 3, "a": {"b": 9}}
    assert resolve(document, "/a~1b") == 3
""",
            "../hidden_tests/test_regression.py": """from pointer import resolve

def test_tilde_and_nested_escape():
    document = {"~": {"x": 1}, "m~n": 4}
    assert resolve(document, "/~0/x") == 1
    assert resolve(document, "/m~0n") == 4
""",
        },
        "expected": "tests/test_pointer.py::test_escaped_slash_is_one_key",
        "reason": "JSON Pointer segments are not unescaped, so ~1 is not treated as a slash.",
    },
]

_extra = runpy.run_path(str(Path(__file__).with_name("extra_cases.py")))
CASES.extend(_extra["EXTRA_CASES"])
for _case in CASES:
    if "fixed" not in _case and _case["id"] in _extra["FIXED_BY_ID"]:
        _case["fixed"] = _extra["FIXED_BY_ID"][_case["id"]]


def build() -> None:
    for case in CASES:
        case_root = ROOT / case["id"]
        repo = case_root / "repo"
        hidden = case_root / "hidden_tests"
        for relative, content in case["files"].items():
            target = repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        allowed = sorted(
            path
            for path in case["files"]
            if not path.startswith("../") and not path.startswith("tests/")
        )
        manifest = {
            "schema_version": 1,
            "id": case["id"],
            "language": "python",
            "difficulty": case["difficulty"],
            "tags": case["tags"],
            "repository": "repo",
            "hidden_tests": "hidden_tests",
            "allowed_source_paths": allowed,
            "test_commands": {
                "public": "python -m pytest -q tests",
                "hidden": "python -m pytest -q ../hidden_tests",
            },
            "expected_failure": {
                "nodeid": case["expected"],
                "reason": case["reason"],
            },
        }
        case_root.mkdir(parents=True, exist_ok=True)
        (case_root / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        hidden.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    build()
