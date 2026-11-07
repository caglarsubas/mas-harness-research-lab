"""RL-13 (PREREG v1): interchange instances validated against the published schemas; convention-mapping coherence.
usage: python3 -I -B rl13_interchange.py EXPORT_ARCH OUT_DIR   (stdlib; writes emitter_*.json and interchange_results.json)"""
import json
import re
import sys
from pathlib import Path

KNOWN_GENAI = {  # from the lab's knowledge of the OpenTelemetry GenAI semantic conventions; NOT fetched; version unverified
    "gen_ai.operation.name", "gen_ai.provider.name", "gen_ai.system", "gen_ai.request.model", "gen_ai.response.model", "gen_ai.agent.name", "gen_ai.agent.id",
    "gen_ai.agent.description", "gen_ai.conversation.id", "gen_ai.tool.name", "gen_ai.tool.call.id", "gen_ai.tool.description", "gen_ai.tool.type",
    "gen_ai.evaluation.name", "gen_ai.evaluation.score.value", "gen_ai.evaluation.score.label", "gen_ai.evaluation.explanation", "gen_ai.evaluation.result",
    "gen_ai.usage.input_tokens", "gen_ai.usage.output_tokens", "gen_ai.input.messages", "gen_ai.output.messages", "gen_ai.system_instructions",
    "gen_ai.tool.definitions", "gen_ai.tool.call.arguments", "gen_ai.tool.call.result", "gen_ai.request.temperature", "gen_ai.request.max_tokens",
    "gen_ai.response.id", "gen_ai.response.finish_reasons", "gen_ai.output.type", "gen_ai.data_source.id", "gen_ai.retrieval.documents",
    "gen_ai.retrieval.query.text", "gen_ai.memory.records", "gen_ai.memory.query.text", "gen_ai.prompt.variable", "gen_ai.main_agent.description",
    "gen_ai.skill.description", "gen_ai.client.inference", "gen_ai.invoke_agent.internal", "gen_ai.execute_tool.internal", "gen_ai.embeddings", "gen_ai.create_agent",
}
NOT_KNOWN_BUT_PLAUSIBLE_SPAN_IDS = {"gen_ai.client.inference", "gen_ai.invoke_agent.internal", "gen_ai.execute_tool.internal"}  # span-type ids the lab cannot confirm


class Validator:
    def __init__(self, schema):
        self.root = schema; self.problems = []

    def ref(self, r):
        node = self.root
        for part in r.lstrip("#/").split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
        return node

    def check(self, schema, doc, path):
        if schema is True or schema == {}:
            return
        if schema is False:
            self.problems.append((path, "false schema")); return
        if "$ref" in schema:
            return self.check(self.ref(schema["$ref"]), doc, path)
        if "const" in schema and doc != schema["const"]: self.problems.append((path, "const"))
        if "enum" in schema and doc not in schema["enum"]: self.problems.append((path, "enum"))
        for key in ("oneOf", "anyOf"):
            if key in schema:
                oks = [not self.probe(s, doc) for s in schema[key]]
                if (key == "oneOf" and sum(oks) != 1) or (key == "anyOf" and not any(oks)): self.problems.append((path, key))
        if "allOf" in schema:
            for s in schema["allOf"]: self.check(s, doc, path)
        t = schema.get("type")
        types = t if isinstance(t, list) else ([t] if t else [])
        if types:
            ok = any((tt == "object" and isinstance(doc, dict)) or (tt == "array" and isinstance(doc, list)) or (tt == "string" and isinstance(doc, str)) or (tt == "integer" and isinstance(doc, int) and not isinstance(doc, bool))
                     or (tt == "number" and isinstance(doc, (int, float)) and not isinstance(doc, bool)) or (tt == "boolean" and isinstance(doc, bool)) or (tt == "null" and doc is None) for tt in types)
            if not ok: self.problems.append((path, "type " + "/".join(types))); return
        if isinstance(doc, dict):
            for k in schema.get("required", []):
                if k not in doc: self.problems.append((path + "/" + k, "missing"))
            props = schema.get("properties", {})
            for k, v in doc.items():
                if k in props: self.check(props[k], v, path + "/" + k)
                elif any(re.search(p, k) for p in schema.get("patternProperties", {})):
                    for p, s in schema["patternProperties"].items():
                        if re.search(p, k): self.check(s, v, path + "/" + k)
                elif schema.get("additionalProperties") is False: self.problems.append((path + "/" + k, "additional"))
                elif isinstance(schema.get("additionalProperties"), dict): self.check(schema["additionalProperties"], v, path + "/" + k)
            if "minProperties" in schema and len(doc) < schema["minProperties"]: self.problems.append((path, "minProperties"))
            if "maxProperties" in schema and len(doc) > schema["maxProperties"]: self.problems.append((path, "maxProperties"))
            if "propertyNames" in schema:
                for k in doc: self.check(schema["propertyNames"], k, path + "/<name>")
        if isinstance(doc, list):
            if "minItems" in schema and len(doc) < schema["minItems"]: self.problems.append((path, "minItems"))
            if "maxItems" in schema and len(doc) > schema["maxItems"]: self.problems.append((path, "maxItems"))
            if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in doc}) != len(doc): self.problems.append((path, "uniqueItems"))
            items = schema.get("items")
            if isinstance(items, dict):
                for i, x in enumerate(doc): self.check(items, x, "%s[%d]" % (path, i))
        if isinstance(doc, str):
            if "pattern" in schema and not re.search(schema["pattern"].replace("(?![\\s\\S])", "$"), doc): self.problems.append((path, "pattern"))
            if "minLength" in schema and len(doc) < schema["minLength"]: self.problems.append((path, "minLength"))
            if "maxLength" in schema and len(doc) > schema["maxLength"]: self.problems.append((path, "maxLength"))
        if isinstance(doc, (int, float)) and not isinstance(doc, bool):
            if "minimum" in schema and doc < schema["minimum"]: self.problems.append((path, "minimum"))
            if "maximum" in schema and doc > schema["maximum"]: self.problems.append((path, "maximum"))

    def probe(self, schema, doc):
        before = len(self.problems); self.check(schema, doc, "?"); bad = self.problems[before:]; del self.problems[before:]; return bad

    def validate(self, doc):
        self.problems = []; self.check(self.root, doc, ""); return list(self.problems)


D = "sha256:" + "0" * 64
LEDGER = {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "ext-emitter-ledger-1", "subject": {"scopeDigest": D}, "rollouts": ["r1"],
          "contexts": [{"contextId": "ctx", "role": "VERIFIER", "inheritsFrom": []}],
          "claims": [{"claimId": "c1", "requirement": "the function returns 2 for input 1", "delivered": "returns 2", "rolloutValues": [{"rollout": "r1", "value": "2"}]}],
          "checks": [{"checkId": "k1", "claimId": "c1", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "DELIVERED", "contextId": "ctx", "outcome": "PASS", "evidence": ["e1"], "establishedValue": "2"}],
          "evidence": [{"evidenceId": "e1", "kind": "TEST_RESULT", "contentDigest": D, "producedBy": "external-test-runner"}],
          "claimVerdicts": [{"claimId": "c1", "verdict": "SUPPORTED", "checks": ["k1"], "value": "2"}],
          "verdict": {"status": "PASS", "producedBy": "ctx", "evidenceRefs": [D], "policyViolations": [], "unresolvedChecks": [], "scores": {}}, "supersedes": None}
MANIFEST = {"schemaVersion": "planeon.internal.run-manifest/v1", "runId": "ext-run-1", "scopeDigest": D, "suiteDigest": D,
            "configuration": {"model": {"id": "ext-model-1", "configurationDigest": D}, "harness": {"commit": "0" * 40, "dirty": False}, "budget": {"tokensPerTask": 1000, "costMicrosPerTask": 0, "wallClockSecondsPerTask": 60}, "agentCount": 1},
            "locks": {"specsDigest": D, "promptDigests": ["sha256:0000000000000000000000000000000000000000000000000000000000000000"], "toolSchemaDigests": ["sha256:0000000000000000000000000000000000000000000000000000000000000000"], "imageDigests": ["sha256:0000000000000000000000000000000000000000000000000000000000000000"], "dependencyLockDigests": ["sha256:0000000000000000000000000000000000000000000000000000000000000000"], "fixtureDigest": D, "datasetDigest": D, "environmentDigest": D, "evaluator": {"id": "ext-eval-1", "version": "1", "digest": D}},
            "seed": {"mode": "FIXED", "value": 1}, "execution": {"cacheKeyDigest": D, "parallelism": 1}, "split": {"declarationDigest": D, "partition": "HELD_OUT"}, "repetition": 1,
            "writtenAt": "2026-11-05T00:00:00Z", "startedAt": "2026-11-05T00:00:00Z", "ledgerDigest": D}
EVENTLOG = {"schemaVersion": "planeon.internal.run-event-log/v1", "rootRunId": "ext-run-1", "traceId": "a" * 32, "sources": {"loopTraceDigest": D, "runManifestDigest": D, "verdictLedgerDigest": D},
            "events": [{"sequence": 1, "logicalTime": 1, "timeMs": 0, "runId": "ext-run-1", "agentId": "ext-agent-1", "spanId": "a" * 16, "parentSpanId": None, "operation": "RUN", "phase": "START", "name": "run", "outcome": None, "payloadRef": None, "inputHash": None, "outputHash": None, "attributes": {"depth": 0, "parentRunId": None}},
                       {"sequence": 2, "logicalTime": 2, "timeMs": 1, "runId": "ext-run-1", "agentId": "ext-agent-1", "spanId": "a" * 16, "parentSpanId": None, "operation": "RUN", "phase": "END", "name": "run", "outcome": "COMPLETED", "payloadRef": None, "inputHash": None, "outputHash": None, "attributes": {"tokens": 10, "iterations": 1, "costMicros": None}}]}


def main(arch, out_dir):
    arch = Path(arch); out_dir = Path(out_dir); out = {"instances": {}, "positives": {}, "mapping": {}}
    schemas = {"ledger": ("verdict-ledger/ledger.schema.json", LEDGER), "manifest": ("run-manifest/run-manifest.schema.json", MANIFEST), "eventlog": ("run-events/run-event-log.schema.json", EVENTLOG)}
    for name, (path, inst) in schemas.items():
        v = Validator(json.loads((arch / path).read_text()))
        problems = v.validate(inst)
        (out_dir / ("emitter_%s.json" % name)).write_text(json.dumps(inst, indent=1, sort_keys=True), encoding="utf-8")
        out["instances"][name] = {"schema": path, "problems": [list(p) for p in problems][:20], "valid": not problems}
    # positives sanity: run-manifest cases with expect None (document) and ledger vectors with expect None
    lv = json.loads((arch / "verdict-ledger/vectors.json").read_text()); mv = json.loads((arch / "run-manifest/vectors.json").read_text())
    vl = Validator(json.loads((arch / "verdict-ledger/ledger.schema.json").read_text()))
    pos = [x for x in lv["ledgers"] if x.get("expect") is None]; bad = [x["id"] for x in pos if vl.validate(x["ledger"])]
    out["positives"]["ledger"] = {"n": len(pos), "failing_in_lab_checker": bad[:10]}
    msch = {k: Validator(json.loads((arch / ("run-manifest/%s.schema.json" % k)).read_text())) for k in ("run-manifest", "evaluation-record", "split-declaration", "selection-record", "distribution-gate")}
    kinds = {}
    for c in mv["cases"]:
        if c.get("expect") is None and isinstance(c.get("document"), dict):
            k = c.get("kind"); kinds.setdefault(k, {"n": 0, "failing": [], "no_schema": 0}); kinds[k]["n"] += 1
            key = {"RUN_MANIFEST": "run-manifest", "EVALUATION_RECORD": "evaluation-record", "SPLIT_DECLARATION": "split-declaration", "SELECTION_RECORD": "selection-record", "DISTRIBUTION_GATE": "distribution-gate"}.get(str(k), None)
            if key is None or key not in msch: kinds[k]["no_schema"] += 1; continue
            if msch[key].validate(c["document"]): kinds[k]["failing"].append(c["id"])
    out["positives"]["manifest_by_kind"] = kinds
    # mapping coherence
    ev = json.loads((arch / "run-events/vectors.json").read_text()); sch = json.loads((arch / "run-events/run-event-log.schema.json").read_text())
    ops = sch["properties"]["events"]["items"]["properties"]["operation"]["enum"]
    spans, points = ev["otelSpans"], ev["otelPointEvents"]
    out["mapping"]["operations"] = {op: ("span" if op in spans else "point" if op in points else "NONE") for op in ops}
    out["mapping"]["coverage_ok"] = all(v != "NONE" for v in out["mapping"]["operations"].values())
    used = sorted(set(re.findall(r'"((?:gen_ai|planeon|error|server|otel)\.[a-z_.]+)"', json.dumps(spans) + json.dumps(points) + json.dumps(ev["otelEvaluationEvent"]))))
    readme = (arch / "run-events/README.md").read_text(encoding="utf-8")
    never = set(re.findall(r"`(gen_ai\.[a-z_.]+)`", readme.split("Never emitted", 1)[1].split("\n\n", 1)[0])) if "Never emitted" in readme else set()
    cls = {}
    for n in used:
        if n.startswith("planeon."): cls[n] = "local extension (planeon.*)"
        elif n.startswith("gen_ai."): cls[n] = ("known to the lab (unverified version)" if n in KNOWN_GENAI and n not in NOT_KNOWN_BUT_PLAUSIBLE_SPAN_IDS else "span-type id the lab cannot confirm" if n in NOT_KNOWN_BUT_PLAUSIBLE_SPAN_IDS else "gen_ai name unknown to the lab")
        else: cls[n] = "core or other registry (error.*, server.*)"
    out["mapping"]["names"] = cls; out["mapping"]["never_emitted"] = sorted(never); out["mapping"]["overlap_with_never_emitted"] = sorted(set(used) & never)
    out["mapping"]["pinned_source"] = {k: ev["otelSource"].get(k) for k in ("repository", "commit", "stability", "schemaUrl")}; out["mapping"]["pinned_files"] = len(ev["otelSource"].get("files", []))
    (out_dir / "interchange_results.json").write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({"instances": {k: (v["valid"], v["problems"][:6]) for k, v in out["instances"].items()}, "positives": out["positives"], "coverage_ok": out["mapping"]["coverage_ok"], "operations": out["mapping"]["operations"], "name_classes": {c: sum(1 for x in cls.values() if x == c) for c in set(cls.values())}, "overlap": out["mapping"]["overlap_with_never_emitted"], "pinned": out["mapping"]["pinned_source"], "pinned_files": out["mapping"]["pinned_files"]}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
