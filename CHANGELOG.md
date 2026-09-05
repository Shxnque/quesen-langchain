# Changelog

## [0.5.0] — 2026-09-05 · SDK 0.6.0 parity · offline verdict replay

### Added
- **`verify_recompute=True`** on `QuesenFirewallTool` — REPLAY the verdict offline
  (via `quesen-sdk` `replay`/`verify_receipt(recompute_request=...)`) against the exact
  context and merge `receipt_recomputed` + `receipt_verification` into the tool output.
  The direct answer to "locally replay the verdict" (BEA criticism-ledger C-003 / C-004).

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.6.0`.

## [0.4.0] — 2026-09-05 · SDK 0.5.0 parity · enforcement + verifiable receipts

### Added
- **`quesen_guard(...)`** — fail-closed enforcement decorator. Wraps
  `quesen_sdk.QuesenFirewall.guard` so any Python callable (a tool's function, a
  LangGraph node) executes ONLY on a PASS verdict; otherwise `TscBlocked` is
  raised and the body never runs. Verdict is attached as `.last_decision`.
- **Independent receipt verification** on `QuesenFirewallTool`: set
  `verify_receipts=True` (and optionally `engine_public_key_hex=...`) to merge a
  client-side `receipt_verified` + `receipt_verification` into the returned
  envelope (structural, plus optional Ed25519 via `quesen-sdk[verify]`).

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.5.0`.

## [0.3.0] — 2026-08-27 · Agent Firewall tool (TSC v2)

### Added
- **`QuesenFirewallTool`** — LangChain `BaseTool` wrapping the Quesen Agent
  Firewall (`POST /tsc/validate`). Deterministic PASS/REVIEW/BLOCK/SKIP + audit
  receipt before a high-risk action (data egress / tool call / payment).
- `sandbox=True` mints a free sandbox key on first use (no signup) so the tool
  works out of the box against the hosted engine.

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.4.1` (firewall + onboarding).

## [0.2.0] — 2026-07-31 · Tracks engine v1.10.0 receipt provenance

### Changed
- Bumped `__version__` `0.1.0` → `0.2.0`.
- Bumped `quesen-sdk` dependency floor to `>=0.2.0`.
- README documents that the raw response dict returned by `QuesenValidateTool`
  now carries `input_snapshot_hash` and `commit_sha` fields when the engine is
  v1.10.0+ (both flow through unchanged from `quesen-sdk` 0.2.0).

### Notes
- No code change to the tool wrappers themselves. `._run(...)` still returns
  `r.raw`; the added fields flow through automatically once the underlying SDK
  exposes them.

## [0.1.0] — 2026-07-16 · Initial release
- Three LangChain `BaseTool` subclasses: `QuesenValidateTool`,
  `QuesenSimulateTool`, `QuesenReportTool`.

[0.2.0]: https://github.com/Shxnque/quesen-langchain/releases/tag/v0.2.0
[0.1.0]: https://github.com/Shxnque/quesen-langchain/releases/tag/v0.1.0
