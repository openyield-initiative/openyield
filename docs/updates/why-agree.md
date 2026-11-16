# Why Can't Autonomous Cars Just Agree on Who Gives Way?

**DRAFT — not published. OpenYield is at the simulation-foundation stage.**

On a narrow Melbourne residential street, parked cars leave room for one vehicle
at a time. Two drivers approach from opposite ends. One slows near a gap, the
other moves through, and both continue. Sometimes someone has to reverse.

It is tempting to imagine autonomous cars exchanging a quick message: “You go
first.” But agreeing on an order leaves several questions unanswered. Is the gap
large enough? Can either vehicle actually reach it? Is there enough clearance
throughout the movement? What happens if one vehicle cannot follow the agreement?

These are the questions motivating OpenYield. A message can express an intention,
but it cannot make an impossible movement possible. Any future agreement must
remain subject to each vehicle's own local constraints. A vehicle must be able
to decline or stop when those constraints cannot be satisfied.

## What we want to investigate

Our immediate research question is whether decentralized, geometry-aware
negotiation improves efficiency and reliability compared with independent
decision-making and fixed-priority strategies in narrow-road encounters.

The wording matters. Communication may help, but we have not demonstrated that it
does in this setting. Fixed priority may be adequate in some encounters. Extra
negotiation may add delay or introduce failure modes. We need common scenarios,
clearly defined policies and measured outcomes before drawing a conclusion.

## What the first demonstration does

The v0.1 demonstration is deliberately scripted. One rectangular vehicle begins
inside a passing space and waits. The other travels past it. The waiting vehicle
then translates sideways and continues. There is no negotiation between them.
It is not an independent-driving baseline or a proposed solution.

The simulation checks the movement between frames for contact, clearance and road
boundary violations. It stops before accepting a step that fails those checks.
A trace and offline replay make the sequence inspectable and repeatable.

That is a useful foundation, with substantial limits. Real vehicles cannot slide
sideways, and rectangles do not establish steering feasibility. Our current
monitor sees the full simulated world; it does not prove independent safety
enforcement on real vehicles. There are no sensors, uncertain observations,
messages or communication failures in v0.1.

## What remains unknown

We still need to define fair comparisons, useful metrics and how to recognize
deadlock or repeated yielding. Later work may explore how negotiation changes
those outcomes, and when it fails to help. A stronger motion model will require
separate work before any physically realistic claim is justified.

The first milestone makes a small encounter reproducible. The research begins
with finding out what that foundation can support, and what evidence is still
missing.
