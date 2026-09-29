import re
import hashlib
from typing import List, Dict, Any, Tuple
from layalog.models import LogEntry

# Regex patterns for Monolog/Laravel logs
MONOLOG_RE = re.compile(
    r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s+(?:(?P<env>\w+)\.)?(?P<level>[A-Z]+):\s+(?P<message>.*)$"
)

# Generic log pattern (e.g. 2026-09-25 12:00:00 [ERROR] ...)
GENERIC_LOG_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?)\s+(?:\[(?P<level>[A-Z]+)\]|(?P<level2>[A-Z]+)[:\s])\s*(?P<message>.*)$"
)

# Stacktrace indicator patterns
STACKTRACE_START_RE = re.compile(r"^(\[stacktrace\]|Traceback \(most recent call last\):|\s*at\s+[\w\.\\/]+)")

class ParsedBlock:
    def __init__(self, line_number: int, timestamp: str, level: str, message: str, raw_lines: List[str]):
        self.line_number = line_number
        self.timestamp = timestamp
        self.level = level.upper()
        self.message = message
        self.raw_lines = raw_lines
        self.stacktrace_lines: List[str] = []

    def get_full_raw(self) -> str:
        return "\n".join(self.raw_lines)

    def get_stacktrace_str(self) -> str:
        return "\n".join(self.stacktrace_lines) if self.stacktrace_lines else ""

def clean_sample_message(msg: str) -> str:
    """
    Strips trailing context JSON and dynamic IDs to provide a clean title/message for UI and LLM.
    """
    # Remove Monolog trailing context JSON like {"userId": ...} or {"trace": ...}
    json_split = re.split(r'\s+\{\s*"', msg, maxsplit=1)
    base = json_split[0].strip() if json_split else msg.strip()

    # Strip dynamic prefixes like [dspace_6ab3ceb04d1c8] or [envio_email_6ab41b97230fc]
    base = re.sub(r'\[[a-zA-Z0-9_\-]+_[0-9a-fA-F]{6,}\]\s*', '', base)

    # Clean whitespace
    return " ".join(base.split())

def normalize_log_message(msg: str) -> str:
    """
    Deep normalization of log error message to extract the root failure pattern,
    ignoring dynamic IDs, timestamps, user info, URLs, query parameters, and line numbers.
    """
    clean_msg = msg.strip()

    # 1. Remove generic exception wrapper prefix if present (e.g. GuzzleHttp\Exception\ServerException: ...)
    clean_msg = re.sub(r'^[a-zA-Z0-9_\\]+(?:Exception|Error):\s*', '', clean_msg)

    # 2. Extract base message before Monolog context JSON
    json_split = re.split(r'\s+\{\s*"', clean_msg, maxsplit=1)
    base_msg = json_split[0].strip() if json_split else clean_msg

    if "Registro de Log" in base_msg and len(json_split) > 1:
        if "GuzzleHttp" in json_split[1] or "DSpace" in base_msg:
            base_msg = "Server error during DSpace / external service call"

    core_msg = base_msg

    # 3. Strip dynamic prefixes like [dspace_6ab3ceb04d1c8] or [envio_email_6ab41b97230fc]
    core_msg = re.sub(r'\[[a-zA-Z0-9_\-]+_[0-9a-fA-F]{6,}\]\s*', '', core_msg)
    core_msg = re.sub(r'ID:\s*\[\d+\]', 'ID: [<ID>]', core_msg)

    # 4. Standardize PHP property access errors
    prop_match = re.search(r"Trying to get property '([^']+)' of non-object", core_msg)
    if prop_match:
        core_msg = f"Trying to get property '{prop_match.group(1)}' of non-object"

    # 5. URLs, Endpoints, Query strings, IPs, Ports
    core_msg = re.sub(r'https?://[^\s/\'"`]+', 'http://<HOST>', core_msg)
    core_msg = re.sub(r'/collections/\d+/', '/collections/<ID>/', core_msg)
    core_msg = re.sub(r'\?[^ \r\n"\'`]+', '?<QUERY>', core_msg)

    # 6. Emails & UUIDs & Hex hashes & Memory addresses
    core_msg = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '<EMAIL>', core_msg)
    core_msg = re.sub(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', '<UUID>', core_msg)
    core_msg = re.sub(r'\b[0-9a-fA-F]{10,}\b', '<HEX_HASH>', core_msg)
    core_msg = re.sub(r'0x[0-9a-fA-F]+', '<ADDR>', core_msg)

    # 7. Memory exhaustion standardization
    core_msg = re.sub(r'Allowed memory size of \d+ bytes exhausted \(tried to allocate \d+ bytes\)', 'Allowed memory size exhausted', core_msg)

    # 8. File paths & line numbers inside message
    core_msg = re.sub(r'\s+in\s+/[^\s]+\.(?:php|py|js|ts|java)(?::\d+)?', '', core_msg)
    core_msg = re.sub(r'(:|\bline\s+)\d+\b', r'\g<1><LINE>', core_msg)
    core_msg = re.sub(r'/[^\s:()]*/([a-zA-Z0-9_\-]+\.(?:php|py|js|ts|java))', r'\1', core_msg)

    # 9. Numbers >= 2 digits
    core_msg = re.sub(r'\b\d{2,}\b', '<NUM>', core_msg)

    # Clean whitespace
    return " ".join(core_msg.split())

def get_representative_stack_frame(stack_lines: List[str]) -> str:
    """
    Extracts and normalizes the first relevant stack trace frame.
    """
    if not stack_lines:
        return ""
    for line in stack_lines:
        s = line.strip()
        if not s or s.startswith('[stacktrace]') or s.lower().startswith('stack trace'):
            continue
        # Strip frame counter (#0, #1...)
        s = re.sub(r'^#\d+\s*', '', s)
        # Normalize line numbers
        s = re.sub(r'\((\d+)\)', '(<LINE>)', s)
        s = re.sub(r':\d+', ':<LINE>', s)
        # Strip full path to basename
        s = re.sub(r'/[^\s:()]*/([a-zA-Z0-9_\-]+\.(?:php|py|js|ts|java))', r'\1', s)
        s = re.sub(r'0x[0-9a-fA-F]+', '<ADDR>', s)
        s = re.sub(r'Object\([^\)]+\)', 'Object()', s)
        return " ".join(s.split())
    return ""

def generate_signature(message: str, stacktrace_first_line: str = "") -> str:
    """
    Generates a consistent 16-char hex signature for an error block by deeply normalizing
    the error message and stacktrace frame.
    """
    n_msg = normalize_log_message(message)
    # If the message is sufficiently descriptive, hash directly on normalized root message.
    # If message is short (like 'Error Code : 904'), append normalized stack trace frame.
    if len(n_msg) < 25 and stacktrace_first_line:
        n_st = get_representative_stack_frame([stacktrace_first_line])
        sig_base = f"{n_msg} || {n_st}"
    else:
        sig_base = n_msg

    return hashlib.sha256(sig_base.encode("utf-8")).hexdigest()[:16]

class LogParser:
    def parse_text(self, text: str) -> Tuple[List[ParsedBlock], int]:
        """
        Parses full log text into blocks of log entries with line tracking.
        Returns (list of error blocks, total line count).
        """
        lines = text.splitlines()
        total_lines = len(lines)
        blocks: List[ParsedBlock] = []
        current_block: ParsedBlock = None
        in_stacktrace = False

        for idx, line in enumerate(lines, start=1):
            monolog_match = MONOLOG_RE.match(line)
            generic_match = GENERIC_LOG_RE.match(line) if not monolog_match else None

            if monolog_match or generic_match:
                # Save previous block if it was an error
                if current_block and self._is_error_level(current_block.level):
                    blocks.append(current_block)

                match = monolog_match or generic_match
                ts = match.group("timestamp") or ""
                level = match.group("level") or match.group("level2") or "INFO"
                msg = match.group("message") or ""

                current_block = ParsedBlock(
                    line_number=idx,
                    timestamp=ts,
                    level=level,
                    message=msg,
                    raw_lines=[line]
                )
                in_stacktrace = False
            else:
                if current_block is not None:
                    current_block.raw_lines.append(line)
                    if STACKTRACE_START_RE.search(line) or line.strip().startswith("#"):
                        in_stacktrace = True
                    if in_stacktrace:
                        current_block.stacktrace_lines.append(line)
                else:
                    # Line before any header (orphan)
                    if self._looks_like_error(line):
                        current_block = ParsedBlock(
                            line_number=idx,
                            timestamp="",
                            level="ERROR",
                            message=line.strip(),
                            raw_lines=[line]
                        )

        if current_block and self._is_error_level(current_block.level):
            blocks.append(current_block)

        return blocks, total_lines

    def _is_error_level(self, level: str) -> bool:
        error_levels = {"ERROR", "CRITICAL", "ALERT", "EMERGENCY", "FATAL", "EXCEPTION", "SEVERE", "WARN", "WARNING"}
        return level.upper() in error_levels

    def _looks_like_error(self, line: str) -> bool:
        lower = line.lower()
        return "error" in lower or "exception" in lower or "fatal" in lower or "traceback" in lower

    def group_incidents(self, blocks: List[ParsedBlock]) -> Dict[str, Dict[str, Any]]:
        """
        Groups parsed error blocks into aggregated incident clusters by signature.
        """
        grouped: Dict[str, Dict[str, Any]] = {}

        for b in blocks:
            top_stack = b.stacktrace_lines[0] if b.stacktrace_lines else ""
            sig = generate_signature(b.message, top_stack)

            if sig not in grouped:
                grouped[sig] = {
                    "signature": sig,
                    "message": clean_sample_message(b.message),
                    "raw_message": b.message,
                    "level": b.level,
                    "first_seen_line": b.line_number,
                    "first_seen_time": b.timestamp,
                    "occurrences": 1,
                    "lines": [b.line_number],
                    "sample_raw": b.get_full_raw(),
                    "sample_stacktrace": b.get_stacktrace_str(),
                }
            else:
                grouped[sig]["occurrences"] += 1
                grouped[sig]["lines"].append(b.line_number)
                # Upgrade sample if another occurrence has full stacktrace
                if not grouped[sig]["sample_stacktrace"] and b.stacktrace_lines:
                    grouped[sig]["sample_stacktrace"] = b.get_stacktrace_str()
                    grouped[sig]["sample_raw"] = b.get_full_raw()

        return grouped
