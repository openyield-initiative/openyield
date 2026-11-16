# OpenYield

Two vehicles meet on a narrow Melbourne residential street. Parked cars prevent
them passing side by side. One driver waits in a gap; the other proceeds. What
would it take for autonomous vehicles to resolve this encounter cooperatively?

**Research question:** Does decentralized, geometry-aware negotiation improve
efficiency and reliability in narrow-road autonomous vehicle encounters compared
with independent decision-making and fixed-priority strategies?

Communication is a hypothesis to test. Each future vehicle must enforce its own
local constraints; an agreement must never override them. The v0.1 shared simulation
monitor is an experimental checking tool, not that future local control system.

The current foundation represents two rectangular vehicles, static obstacles and
one passing space. It exports a deterministic scripted trace and an offline replay.
There is no negotiation, independent-driving baseline or performance comparison.
No novelty or real-world safety claim follows from this demonstration.

Start with [the setup instructions](getting-started.md) and read
[the model assumptions](model.md) before interpreting any output.

This is an early research initiative intended to become open source. Licensing
and ownership remain undecided; no permission grant is implied.
