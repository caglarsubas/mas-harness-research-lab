# Fetch record, 2026-11-05: the owner-approved lines of FETCH-ASK-2026-11-05 (b824fb24)

Owner, through the monitor, verbatim: "The 5 identified lines (Recommended)"; second tier "Not now (Recommended)".
Approved: one read-only GET per exact identifier, six GETs in all (F4 has two). Not approved: anything without an
exact identifier (MemBench, the NeurIPS oversight paper, the rank-reversal study, F1, F3) and the second tier.
Client: a generic command-line client with the user-agent string `generic-fetch/1.0`, no cookies, no personal data.
Each response is stored by sha256 in the lab scratch (an isolated folder per line, never in the bridge), nothing is
executed from it, and the PDFs are read as data only. Redirects: arXiv none; doi.org followed to the publisher, hosts
listed. One request per line; no retry on a paywall or a challenge page.

| line | request URL | HTTP | final URL (host chain) | type | bytes | sha256 | what it is |
|---|---|---|---|---|---|---|---|
| F2 | arxiv.org/pdf/2603.20356 | 200 | same (arxiv.org) | application/pdf | 700,203 | 9dff38ef1396804f3c4f4d6ed471403f89b04e75336e72fe57a0be80152a23d7 | "Agentproof: Static Verification of Agent Workflow Graphs", arXiv 2603.20356v1, 20 Mar 2026, 12 pages; title confirmed on page 1 |
| F4a | arxiv.org/pdf/2605.27922 | 200 | same (arxiv.org) | application/pdf | 7,218,628 | b2ec0c042c4738cd99ace87150af6ed175c098b39fd24f36b1b6ce141e2b5d34 | "Harness-Bench: Evaluating Agent Harnesses across Models and Realistic Workflows", arXiv 2605.27922v2, 15 Oct 2026; title confirmed (RS-2 cites it with a slightly different subtitle) |
| F4b | arxiv.org/pdf/2606.00920 | 200 | same (arxiv.org) | application/pdf | 629,978 | 8488e9440ac33fca66aece3a956fef9ff728daa9ecf1492b02f39ce3b5fafd9b | "How Much Can Repeated Running Buy? A Measured Variance Ceiling for LLM Code Evaluation", arXiv 2606.00920v2, 10 Oct 2026; title confirmed |
| F5 | doi.org/10.1038/s42256-026-01268-y | 200 | www.nature.com/articles/s42256-026-01268-y (chain: doi.org, www.nature.com, idp.nature.com twice, www.nature.com; the publisher's own identity host answered two of the four redirects, then returned to the article with a "cookies not supported" query flag) | text/html | 475,030 | b3a379894adc96b9afb9d2aedddfde85b0b53787f013111911d540aae06741e9 | "Capable language models can outgrow the benefits of collaboration", Nature Machine Intelligence; the page marks itself Open Access and carries Methods, Data availability and Code availability sections (about 195,000 characters of text), so the article body is present; the Zenodo code archive was not requested |
| F6 | arxiv.org/pdf/2606.04329 | 200 | same (arxiv.org) | application/pdf | 4,981,471 | 36999ed0cb2d15b93897fa1f8be9ff2291516b633889e16e377f19db4288f482 | "From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents", arXiv 2606.04329v2, 18 Jun 2026, 14 pages; title confirmed |
| F7 | doi.org/10.1080/10447318.2026.2618568 | 403 | www.tandfonline.com/doi/full/10.1080/10447318.2026.2618568 (chain: doi.org, www.tandfonline.com) | text/html | 5,555 | 44f4cea479da85fde9136115582bd2faee08363f655d36ea05dbbfab02c1ad98 | a bot-challenge page titled "Just a moment..." (5,555 bytes, no article text); kept as received; no second request. The article is NOT held |

Monitor ruling (2026-11-05, on RL-M25a): F5 counts as held (idp.nature.com is the publisher's own host, reached
only through the resolver's chain, no cookies sent); F7 is not held and is never retried or worked around; if the
oversight study is needed later it is an owner question.

Held and readable: F2, F4a, F4b, F5, F6 (five of six). Not held: F7. Every figure quoted from these sources in a
lab record is "as reported" until the lab reproduces it. Next use: F2 for H-25's violation classes and witness
traces; F4a and F4b for H-12 / H-31's reporting unit and clustered intervals; F5 for H-13 / H-14's selection rule;
F6 for H-28's poisoning case class. They enter the crosswalk at a later lock as OWNER_SUPPLIED secondary papers
(the visionary records them by the digests above).
