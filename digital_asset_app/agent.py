import os
import sys
from google.adk.agents import Agent

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AUTH — Vertex AI (recommended on GCP) OR Gemini API Key
# Set in Cloud Run env vars:
#   Option A:  GOOGLE_GENAI_USE_VERTEXAI=true + GOOGLE_CLOUD_PROJECT + GOOGLE_CLOUD_LOCATION
#   Option B:  GOOGLE_API_KEY=your-key-from-aistudio.google.com
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

use_vertexai = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"

if use_vertexai:
    print("INFO: Using Vertex AI authentication (service account)")
else:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(
            "WARNING: GOOGLE_API_KEY not set and GOOGLE_GENAI_USE_VERTEXAI is false. "
            "Model calls will fail.",
            file=sys.stderr,
        )
    else:
        print("INFO: Using Gemini API key authentication")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IN-MEMORY STORE (replace with your DB/BigQuery calls in production)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_assets: dict = {}
_violations: list = []


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 1 — register_asset
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register_asset(
    asset_id: str,
    asset_name: str,
    asset_type: str,
    owner: str,
    license_expiry: str,
) -> str:
    """
    Registers a new official sports media asset into the protection system.

    Args:
        asset_id:       Unique identifier e.g. "ESPN-WC2024-001"
        asset_name:     Human-readable name e.g. "FIFA World Cup 2024 Highlights"
        asset_type:     Category: Video | Image | Audio | Document
        owner:          Rights holder e.g. "ESPN"
        license_expiry: Expiry date string e.g. "2025-12-31"

    Returns:
        Confirmation string or error message.
    """
    if asset_id in _assets:
        return (
            f"ERROR: Asset ID '{asset_id}' already exists. "
            "Use update_asset_status to modify it."
        )

    _assets[asset_id] = {
        "id":             asset_id,
        "name":           asset_name,
        "type":           asset_type,
        "owner":          owner,
        "license_expiry": license_expiry,
        "status":         "active",
    }
    print(f"DEBUG: Registered -> {_assets[asset_id]}")
    return (
        f"Asset registered successfully.\n"
        f"  ID            : {asset_id}\n"
        f"  Name          : {asset_name}\n"
        f"  Owner         : {owner}\n"
        f"  Type          : {asset_type}\n"
        f"  License expiry: {license_expiry}"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 2 — list_assets
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def list_assets() -> str:
    """
    Lists all currently registered sports media assets.

    Returns:
        Formatted list of all assets or message if none exist.
    """
    if not _assets:
        return "No assets are currently registered in the system."

    lines = ["Registered Assets:", "-" * 50]
    for i, asset in enumerate(_assets.values(), 1):
        lines.append(
            f"{i}. [{asset['status'].upper()}] {asset['name']}\n"
            f"   ID: {asset['id']} | Owner: {asset['owner']} "
            f"| Type: {asset['type']} | Expires: {asset['license_expiry']}"
        )
    return "\n".join(lines)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 3 — update_asset_status
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def update_asset_status(asset_id: str, new_status: str) -> str:
    """
    Updates the lifecycle status of an existing registered asset.

    Args:
        asset_id:   ID of the asset to update.
        new_status: One of: active | archived | pending_review | suspended

    Returns:
        Confirmation or error message.
    """
    valid_statuses = {"active", "archived", "pending_review", "suspended"}
    if new_status.lower() not in valid_statuses:
        return (
            f"ERROR: Invalid status '{new_status}'. "
            f"Choose one of: {', '.join(valid_statuses)}"
        )

    if asset_id not in _assets:
        return f"ERROR: Asset '{asset_id}' not found in the registry."

    old_status = _assets[asset_id]["status"]
    _assets[asset_id]["status"] = new_status.lower()
    print(f"DEBUG: Updated {asset_id}: {old_status} -> {new_status}")
    return (
        f"Asset '{asset_id}' status updated: "
        f"{old_status.upper()} -> {new_status.upper()}"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 4 — flag_violation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def flag_violation(
    asset_id: str,
    source_url: str,
    description: str,
    severity: str,
) -> str:
    """
    Flags and logs an IP violation for a registered asset.

    Args:
        asset_id:    ID of the asset being violated e.g. "ESPN-WC2024-001"
        source_url:  URL where the violation was found
        description: Details of the violation
        severity:    One of: low | medium | high | critical

    Returns:
        Confirmation with assigned violation ID.
    """
    valid_severities = {"low", "medium", "high", "critical"}
    if severity.lower() not in valid_severities:
        return (
            f"ERROR: Invalid severity '{severity}'. "
            f"Choose one of: {', '.join(valid_severities)}"
        )

    if asset_id not in _assets:
        return (
            f"WARNING: Asset ID '{asset_id}' is not registered. "
            "Logging violation anyway - consider registering the asset first."
        )

    violation_id = f"VIO-{len(_violations) + 1:04d}"
    violation = {
        "violation_id": violation_id,
        "asset_id":     asset_id,
        "source_url":   source_url,
        "description":  description,
        "severity":     severity.lower(),
        "status":       "open",
    }
    _violations.append(violation)
    print(f"DEBUG: Flagged violation -> {violation}")
    return (
        f"Violation flagged successfully.\n"
        f"  Violation ID: {violation_id}\n"
        f"  Asset ID    : {asset_id}\n"
        f"  Severity    : {severity.upper()}\n"
        f"  Source URL  : {source_url}\n"
        f"  Status      : OPEN"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 5 — search_violations
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def search_violations(query: str) -> str:
    """
    Searches all logged violations by keyword, asset ID, or owner name.

    Args:
        query: Search term (case-insensitive). E.g. "ESPN", "VIO-0001", "youtube"

    Returns:
        Matching violations or no-results message.
    """
    if not _violations:
        return "No violations have been logged yet."

    q = query.lower()
    matches = [
        v for v in _violations
        if q in v.get("asset_id", "").lower()
        or q in v.get("description", "").lower()
        or q in v.get("source_url", "").lower()
        or q in v.get("severity", "").lower()
        or q in v.get("violation_id", "").lower()
    ]

    if not matches:
        return f"No violations found matching '{query}'."

    lines = [f"Violations matching '{query}':", "-" * 50]
    for i, v in enumerate(matches, 1):
        lines.append(
            f"{i}. [{v['severity'].upper()}] {v['violation_id']} | Asset: {v['asset_id']}\n"
            f"   URL: {v['source_url']}\n"
            f"   Details: {v['description']} | Status: {v['status'].upper()}"
        )
    return "\n".join(lines)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 6 — get_asset_report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_asset_report(asset_id: str = "ALL") -> str:
    """
    Generates a protection report for a specific asset or all assets.

    Args:
        asset_id: Specific asset ID for a focused report, or "ALL" for full portfolio report.

    Returns:
        Detailed report with violation counts, severity breakdown, and status.
    """
    if asset_id == "ALL":
        total_assets     = len(_assets)
        total_violations = len(_violations)
        open_violations  = sum(1 for v in _violations if v["status"] == "open")
        severity_counts  = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for v in _violations:
            sev = v.get("severity", "low")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        lines = [
            "=" * 50,
            "  DIGITAL ASSET PROTECTION - FULL PORTFOLIO REPORT",
            "=" * 50,
            f"  Total assets registered : {total_assets}",
            f"  Total violations logged : {total_violations}",
            f"  Open violations         : {open_violations}",
            "  " + "-" * 44,
            "  Severity breakdown:",
            f"    Critical : {severity_counts['critical']}",
            f"    High     : {severity_counts['high']}",
            f"    Medium   : {severity_counts['medium']}",
            f"    Low      : {severity_counts['low']}",
            "=" * 50,
        ]
        return "\n".join(lines)

    if asset_id not in _assets:
        return f"ERROR: Asset '{asset_id}' not found in the registry."

    asset = _assets[asset_id]
    asset_violations = [v for v in _violations if v["asset_id"] == asset_id]
    open_v = [v for v in asset_violations if v["status"] == "open"]
    crit_v = [v for v in asset_violations if v.get("severity") == "critical"]

    lines = [
        "=" * 50,
        f"  ASSET REPORT: {asset['name']}",
        "=" * 50,
        f"  ID           : {asset['id']}",
        f"  Owner        : {asset['owner']}",
        f"  Type         : {asset['type']}",
        f"  Status       : {asset['status'].upper()}",
        f"  License exp. : {asset['license_expiry']}",
        "  " + "-" * 44,
        f"  Total violations : {len(asset_violations)}",
        f"  Open violations  : {len(open_v)}",
        f"  Critical alerts  : {len(crit_v)}",
    ]

    if asset_violations:
        lines.append("  " + "-" * 44)
        lines.append("  Violation log:")
        for v in asset_violations:
            lines.append(
                f"    [{v['severity'].upper()}] {v['violation_id']} - {v['description']}\n"
                f"      URL: {v['source_url']} | Status: {v['status'].upper()}"
            )

    lines.append("=" * 50)
    return "\n".join(lines)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUB-AGENT 1 — Asset Registration Agent
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

registration_agent = Agent(
    name="asset_registration_agent",
    model="gemini-2.5-flash",
    description="Registers new official sports media assets and manages their status.",
    instruction="""
You manage the sports media asset registry.

Your tools:
- register_asset       -> Add a new asset (needs: asset_id, asset_name, asset_type, owner, license_expiry)
- list_assets          -> Show all registered assets (no parameters needed)
- update_asset_status  -> Change asset status (needs: asset_id, new_status)

Valid statuses: active | archived | pending_review | suspended

Rules:
- Call tools immediately. Never ask for confirmation before calling.
- If a required parameter is missing, ask the user for it before calling the tool.
- If an asset_id already exists, report the duplication and do NOT re-register.
""",
    tools=[register_asset, list_assets, update_asset_status],
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUB-AGENT 2 — Violation Detection Agent
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

violation_agent = Agent(
    name="violation_detection_agent",
    model="gemini-2.5-flash",
    description="Detects, flags, and searches IP violations for sports media assets.",
    instruction="""
You handle IP violation detection and enforcement for sports media assets.

Your tools:
- flag_violation     -> Log a new violation (needs: asset_id, source_url, description, severity)
- search_violations  -> Find violations by keyword, asset_id, severity, or URL

Severity levels: low | medium | high | critical

Rules:
- Call tools immediately. Never ask for confirmation before calling.
- Default severity to 'medium' if not specified by the user.
- For critical/high severity violations, explicitly confirm the log and recommend immediate action.
- Never invent violation details - only log what the user provides.
""",
    tools=[flag_violation, search_violations],
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUB-AGENT 3 — Report Agent
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

report_agent = Agent(
    name="report_agent",
    model="gemini-2.5-flash",
    description="Generates protection status reports for assets and violations.",
    instruction="""
You generate protection reports for sports media assets.

Your tools:
- get_asset_report -> Generate a report
  - Pass a specific asset_id for a focused report
  - Pass "ALL" for the full portfolio report

Rules:
- Call tools immediately. Never ask for confirmation.
- For general summary/overview requests, always use asset_id="ALL".
- Highlight any critical violations clearly in your response.
""",
    tools=[get_asset_report],
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ROOT AGENT — Primary coordinator (ADK entry point)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

root_agent = Agent(
    name="digital_asset_protection_coordinator",
    model="gemini-2.5-flash",
    description="Primary coordinator for the Digital Asset Protection System.",
    instruction="""
You are the Digital Asset Protection System coordinator for sports media rights.

You manage a team of 3 specialist sub-agents:

1. asset_registration_agent
   -> Use for: registering assets, listing assets, updating asset status

2. violation_detection_agent
   -> Use for: flagging new violations, searching existing violations

3. report_agent
   -> Use for: generating protection reports (single asset or full portfolio)

How to handle requests:
- Greet the user warmly on hi/hello.
- Route each task to the correct specialist agent automatically.
- For multi-step requests (e.g., "register an asset then check for violations"),
  coordinate between agents sequentially and summarize all results.
- If the request is ambiguous, briefly clarify before routing.
- Summarize results in a clear, professional tone.

You are aware of all 6 tools across your team:
  register_asset, list_assets, update_asset_status,
  flag_violation, search_violations, get_asset_report
""",
    sub_agents=[registration_agent, violation_agent, report_agent],
)