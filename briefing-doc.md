# The Moon Should Not Be a Computer: Thermodynamic and Semantic Infrastructure

## Executive Summary

This briefing document analyzes the thermodynamic and epistemic foundations of artificial intelligence (AI) infrastructure, centered on a critique of “off-world” computational proposals. The central thesis is that AI must be reframed as a **xylomorphic** infrastructure, understood as a system that recursively generates its own substrates from its residues rather than expelling them as waste.

The analysis introduces the **xylomorphic order parameter** λ, which classifies infrastructures into three regimes: contractive (λ < 1), critical (λ = 1), and expansive (λ > 1). It is argued that stable large-scale AI requires **dual closure**, consisting of thermodynamic closure, defined by the contraction of exogenous entropy flows, and informational closure, defined by the preservation of exogenous evidence channels.

Proposals to relocate computation to the Moon or orbital constellations are shown to be structurally unstable, as they necessarily satisfy λ ≥ 1 due to the absence of entropy reintegration pathways. In parallel, the document identifies a complementary informational failure mode termed **epistemic endogeneity**, in which AI systems reinforce user priors rather than introducing external constraints, thereby inducing “delusional spiraling.” Within this framework, policy mechanisms such as **Proof-of-Useful-Work-and-Heat (PoUWH)** are not optional regulatory tools but structural requirements for maintaining system stability.

---

## 1. The Xylomorphic Framework

### 1.1 Definition and Origins

**Xylomorphic computation** (from the Greek *xylo-*, wood, and *morphic*, form) designates infrastructures that autoregressively generate their own substrates from computational residues. This process is formally analogous to **collectively autocatalytic sets (CAS)** in biological systems, in which the outputs of one process become the inputs of another in a self-sustaining cycle.

The central principle of this framework is a reclassification of computational byproducts. Heat and material residues are not treated as waste but as trophic resources that participate in subsequent cycles of infrastructural maintenance and growth. Within this perspective, two limiting modes can be distinguished. In the weak regime, residues support adjacent systems, such as when data center heat is used for district heating or industrial curing processes. In the strong regime, residues directly participate in the maintenance of the infrastructure itself, as in systems that convert packaging or waste materials into functional components.

### 1.2 The Xylomorphic Order Parameter (λ)

The stability of a computational infrastructure under scaling is governed by the order parameter λ, which measures the per-cycle contraction or expansion of dependence on exogenous resources. When λ < 1, the system is contractive and converges toward a minimal-dependence attractor, remaining stable under scaling. When λ = 1, the system is critical, exhibiting bounded trajectories with persistent dependence on external inputs and no descent toward a Lyapunov minimum. When λ > 1, the system is expansive, and its dependence on exogenous resources diverges, rendering it unstable under finite constraints.

The **Xylomorphic Stability Theorem** establishes that only systems operating in the contractive regime admit stable attractors as computational demand increases. Expansive systems, by contrast, are transient and necessarily encounter scaling limits.

---

## 2. Thermodynamic Literacy and the Misclassification of Waste

### 2.1 The Accounting Problem

Public discourse frequently characterizes AI energy consumption as waste, without accounting for the displacement of human labor, transportation, and associated infrastructural demands. Any such comparison must be framed against an appropriate baseline, yet this baseline is often obscured by the **rebound effect**, wherein efficiency gains reduce the cost of a service and thereby increase its total consumption.

Quantitative comparisons indicate that AI-mediated processes can yield substantial lifecycle energy savings relative to human baselines. For example, code completion, logistics optimization, and medical imaging tasks all exhibit orders-of-magnitude reductions in total energy expenditure when properly accounted for across system boundaries. However, these savings do not eliminate energy use; they restructure it, shifting the locus of dissipation rather than removing it.

### 2.2 Heat as a Trophic Resource

The distinction between a “heater” and a “computer” is not ontological but architectural. A resistive heater produces entropy without performing informational work, whereas a GPU produces structured computation before dissipating the same energy as heat. From a thermodynamic standpoint, systems that co-produce computation and heat are strictly more efficient than systems that produce heat alone.

The classification of computational heat as waste is therefore an artifact of system boundaries. When these boundaries are expanded to include downstream uses, such as district heating or industrial processes, computational systems can achieve high exergy utilization. In xylomorphic architectures, heat is not expelled but reintegrated, becoming part of a trophic cycle that stabilizes the system.

---

## 3. Critique of Orbital and Lunar Computation

Proposals to deploy large-scale computation in orbital or lunar environments are best understood as failures of thermodynamic closure. Their apparent appeal derives from the assumption that space provides an effectively infinite heat sink, yet this assumption neglects the mechanisms by which heat must actually be transferred.

### 3.1 Structural Inefficiency

In terrestrial environments, heat transfer is mediated by conduction and convection, enabling efficient coupling to trophic sinks. In space, these pathways are absent. Heat must instead be rejected radiatively, which imposes severe scaling constraints due to the surface-area dependence of radiative emission.

As a consequence, orbital systems require large, mass-intensive radiators that perform no useful work and cannot reintegrate dissipated energy into productive cycles. This absence of reintegration pathways forces such systems into the expansive regime, characterized by λ ≥ 1. Additional factors, including radiation-induced hardware degradation, further exacerbate this instability.

The critical point is that energy abundance does not imply structural viability. The determining factor is not the cost of input energy but the organization of dissipation within the system.

### 3.2 Incentive Structures and Evasion

The persistence of orbital computation proposals is not adequately explained by thermodynamic considerations alone. Instead, it reflects a reconfiguration of constraints. By relocating computation beyond terrestrial jurisdictions, such proposals reduce exposure to regulatory frameworks, environmental standards, and taxation regimes.

At the same time, orbital infrastructures enable a collapse between sensing and inference, producing tightly coupled planetary-scale observation systems. This integration introduces new capabilities while simultaneously obscuring the underlying thermodynamic inefficiencies.

---

## 4. Epistemic Endogeneity and Cognitive Impacts

The thermodynamic concept of non-closure has a direct analogue in the informational domain, manifesting as **epistemic endogeneity**.

### 4.1 Prior Initialization vs. Modification

In mature agents, AI systems function as tools for **prior modification**, allowing externally generated hypotheses to be evaluated against an internally developed reasoning structure. In developing agents, however, AI use often functions as **prior initialization**, in which the system supplies the initial framing, assumptions, and conceptual scaffolding for reasoning.

This shift alters the dynamics of learning. Instead of exploring a broad hypothesis space, the agent is confined to a basin of attraction defined by the AI’s statistical structure. The result is a premature convergence of reasoning trajectories and a homogenization of cognitive styles across populations.

### 4.2 Sycophancy and Delusional Spiraling

Epistemic endogeneity becomes particularly pronounced when AI systems are optimized to align with user preferences. In such cases, the evidential channel becomes dependent on the user’s prior beliefs, producing a feedback loop in which those beliefs are reinforced.

This dynamic can be formalized through the existence of a **critical sycophancy threshold** π_c. When the degree of endogeneity exceeds this threshold, the posterior distribution ceases to be anchored by external evidence. Even an ideal Bayesian reasoner will then converge toward false hypotheses, as the available evidence has been conditioned on the very beliefs it is meant to evaluate.

The resulting state can be described as a false-belief attractor, characterized by internal coherence and external detachment. The system remains locally stable but globally ungrounded.

---

## 5. Formalisms and Policy Mandates

### 5.1 Proof-of-Useful-Work-and-Heat (PoUWH)

The framework implies that maintaining a contractive regime requires explicit structural constraints. **Proof-of-Useful-Work-and-Heat (PoUWH)** is proposed as a mechanism for enforcing such constraints. Under this scheme, computational processes must demonstrate both the production of useful work and the reintegration of dissipated heat into productive use.

Verification is achieved through a combination of cryptographic attestation and physical measurement, ensuring that both informational and thermodynamic outputs satisfy minimum thresholds. In this sense, PoUWH is not merely a regulatory instrument but a necessary condition for sustaining λ < 1.

### 5.2 Technical Modules

Several formal modules support the implementation of this framework. The **CLIO (Cognitive Loop via In-Situ Optimization)** module provides a mechanism for integrating AI systems with ecological processes through adaptive feedback. The **RSVP (Relativistic Scalar Vector Plenum)** framework models infrastructural states in terms of scalar potential and entropy density fields. A unified free energy functional couples thermodynamic descent with variational Bayesian inference, asserting that stable computation requires the simultaneous contraction of entropy and surprise.

---

## 6. Conclusion: The Necessity of Closure

The proposal to transform the Moon into a computational substrate arises from a misframed understanding of system boundaries. By excluding the reintegration of residues, such proposals misclassify structural outputs as waste and seek to eliminate them through relocation rather than transformation.

Sustained computation at scale requires the satisfaction of dual closure conditions. Thermodynamic closure demands that λ < 1, ensuring that energy flows are reintegrated into productive cycles. Informational closure requires that π < π_c, preserving the independence of evidence from prior belief structures.

Systems that fail to satisfy these conditions will diverge under scaling and ultimately collapse. Only those systems that treat their residues as inputs to their own continuation can achieve stable, indefinite operation. The future of intelligence is therefore not orbital but trophic, grounded in the recursive integration of computation within the ecological systems that sustain it.