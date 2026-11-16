# Research context and literature leads

This is an initial source check on 16 November 2026, not a comprehensive review.
The project brief supplied five unverified leads. Below we distinguish identified
sources from unresolved identification. No results are transferred to OpenYield.

1. **Wang, Avedisov, Altintas and Orosz (2024)**, *Negotiation in Cooperative
   Maneuvering using Conflict Analysis: Theory and Experimental Evaluation*,
   IEEE Intelligent Vehicles Symposium, pp. 2297–2302. Verified against the
   [author-hosted original paper](https://websites.umich.edu/~orosz/articles/2024_IVS_Wang_Avedisov_Altintas_Orosz.pdf).
   It provides a lead on maneuver requests, responses and conflict analysis. Its
   illustrated encounter is an intersection, not our narrow-road bay experiment.

2. **Rettenmaier and Bengler (2021), bottleneck communication**: the brief does
   not supply a title. A plausible match is *The Matter of How and When: Comparing
   Explicit and Implicit Communication Strategies of Automated Vehicles in
   Bottleneck Scenarios*, IEEE Open Journal of Intelligent Transportation Systems
   2, 282–293, DOI 10.1109/OJITS.2021.3107678.
   [Original paper in TUM's repository](https://mediatum.ub.tum.de/doc/1738468/document.pdf).
   Bibliographic details verified; identity as the intended lead remains unresolved.
   Human–vehicle communication is related context, not evidence for AV–AV negotiation.

3. **Cao and Zhao (2022)**, *Decision-making method of autonomous vehicles for
   right of way on road segments*, Journal of Zhejiang University (Engineering
   Science), 56(1), 118–127, DOI 10.3785/j.issn.1008-973X.2022.01.013.
   [Original journal record and abstract](https://www.zjujournals.com/eng/EN/10.3785/j.issn.1008-973X.2022.01.013).
   Metadata verified. The abstract describes pedestrian–vehicle right-of-way
   decisions; the title alone should not be read as a narrow-road AV–AV study.

4. **Rettenmaier, Dinkel and Bengler (2021)**, *Communication via motion –
   Suitability of automated vehicle movements to negotiate the right of way in
   road bottleneck scenarios*, Applied Ergonomics 95, 103438,
   DOI 10.1016/j.apergo.2021.103438.
   [TUM institutional record](https://portal.fis.tum.de/de/publications/communication-via-motion-suitability-of-automated-vehicle-movemen/)
   and [publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0003687021000855).
   Metadata and study context verified; useful lead for motion cues and human
   interpretation, not a justification for our sideways translation simplification.

5. **Ítalo Romani de Oliveira**, *Analyzing the performance of distributed
   conflict resolution among autonomous vehicles*.
   [Publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0191261516304854)
   and [author preprint](https://arxiv.org/abs/2110.08127).
   Title and author identified. The supplied 2017 publication lead must be
   distinguished from the 2021 arXiv posting. Final journal-year/DOI reconciliation
   remains open here. No detailed quantitative finding is asserted.

## Questions before designing v0.2–v0.3

- Which scenarios require cooperation rather than a fixed yielding rule?
- How should local geometry constrain an offered agreement?
- What defines progress, timeout, deadlock and fairness under identical conditions?
- What information should each independent controller receive?
- How do we separate policy benefits from privileged information or simplified motion?
- Which original studies supply reusable definitions, and which address different interactions?

Future literature work should read methods and assumptions in full, verify the
ambiguous citations and document experimental differences before claiming novelty.
