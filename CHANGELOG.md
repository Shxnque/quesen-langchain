# Changelog

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
