# RL-13 mapping: the three contracts as interchange formats, and the convention mapping (2026-11-05)

Every convention field name below is from the lab's knowledge, not fetched, version unverified. The contract itself
pins `open-telemetry/semantic-conventions-genai` at commit 4e8a2812 (stability development, schema gen-ai-dev/1.42.0-dev,
seven files by digest); the lab cannot fetch it and did not.

## 1. Interchange surfaces (what an external emitter must produce)

| contract | schema id | required top-level keys | id and digest forms |
|---|---|---|---|
| verdict ledger | planeon.internal.verdict-ledger/v1 | schemaVersion, ledgerId, subject.scopeDigest, rollouts, contexts, claims, checks, evidence, claimVerdicts, verdict, supersedes | ids `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`; digests `sha256:<64 hex>`; roles, check kinds, evidence kinds and outcomes are closed enums (check-kinds.json) |
| run manifest | planeon.internal.run-manifest/v1 | schemaVersion, runId, scopeDigest, suiteDigest, configuration{model{id,configurationDigest}, harness{commit,dirty}, budget{tokensPerTask,costMicrosPerTask,wallClockSecondsPerTask}, agentCount}, locks{specsDigest, promptDigests[], toolSchemaDigests[], imageDigests[], dependencyLockDigests[], fixtureDigest, datasetDigest, environmentDigest, evaluator{id,version,digest}}, seed{mode,value}, execution{cacheKeyDigest,parallelism}, split{declarationDigest,partition}, repetition, writtenAt, startedAt, ledgerDigest | digests `sha256:`; commit 40 hex; three lock arrays need at least one digest; seed is an object (mode FIXED + value), not a bare integer |
| run-event log | planeon.internal.run-event-log/v1 | schemaVersion, rootRunId, traceId (32 hex, non-zero), sources{loopTraceDigest,runManifestDigest,verdictLedgerDigest}, events[] | each event: sequence, logicalTime, timeMs, runId, agentId, spanId (16 hex, non-zero), parentSpanId, operation (11-value enum), phase (START/END/POINT), name, outcome, payloadRef, inputHash, outputHash, attributes; 16 operation-phase branches fix outcome and the attribute set (RUN START: depth, parentRunId; RUN END: tokens, iterations, costMicros) |

The lab's emitter instances (`data/emitter_*.json`) were written from the schemas' required sets and types alone;
two repairs were needed for the manifest (object-valued model and harness, the budget's three keys, non-empty lock
arrays, the environment digest, the seed object) and two for the event log (non-zero ids, the branch attribute sets).
What the schema text does not say and an emitter must learn elsewhere: nothing found for these three; the branch
attribute sets are in the schema's oneOf.

## 2. The run-event operations and the GenAI conventions

| operation | mapping (from the contract's vectors) | names used | class |
|---|---|---|---|
| RUN | span `gen_ai.invoke_agent.internal`, INTERNAL, operation invoke_agent | gen_ai.agent.name, gen_ai.conversation.id | known names; the span-type id unconfirmable by the lab |
| AGENT_INVOKE | plain span `delegate` | planeon.childRunId | local extension |
| MODEL_CALL | span `gen_ai.client.inference`, CLIENT, operation chat | gen_ai.conversation.id, gen_ai.request.model, gen_ai.provider.name | known names; span-type id unconfirmable |
| TOOL_CALL | span `gen_ai.execute_tool.internal`, INTERNAL, operation execute_tool | gen_ai.tool.name, gen_ai.tool.call.id | known names; span-type id unconfirmable |
| VERIFICATION | plain span `verify {gateId}` + evaluation event | planeon.gateId; gen_ai.evaluation.name, gen_ai.evaluation.result, gen_ai.evaluation.score.label | known names + local extension |
| HOOK, HANDOFF, MESSAGE, ENVIRONMENT, CLAIM, MERGE | span events `planeon.<operation>` with `planeon.*` attributes | planeon.* | local extensions |

Name classes over the 18 dotted names in the mapping: 9 gen_ai.* known to the lab, 3 span-type ids the lab cannot
confirm (they look like the new repository's span-type identifiers), 6 planeon.* local extensions, 0 unknown
gen_ai.* names, 0 overlap with the README's never-emitted list (16 names). Tokens stay local (planeon.tokens) because
the registry has input and output token attributes but no total; providers are absent from derived logs.
