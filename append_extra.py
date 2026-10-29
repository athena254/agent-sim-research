extra = '''

## 9. Software Factory — Full Domain Coverage

The Agency software factory (when fully built) was evaluated against multiple
software domains. Here is how the factory maps to each:

### 9.1 Vehicles (Cars, Yachts, Planes)

Builders:
- C06 Systems, Embedded and Hardware Builder — firmware, drivers, toolchains for ECUs, flight controllers, marine electronics
- Controls Engineer — feedback and control loops (steering, throttle, stabilization)
- Robotics Engineer (ROS) — sensor/actuator integration, perception stacks
- IoT Cloud / Device Management Engineer — fleet provisioning, OTA updates, telemetry

Verification:
- Automotive / Avionics Safety Engineer (in D03) — ISO 26262 (automotive), DO-178C (avionics)
- HIL / Hardware Test Engineer (in D04) — hardware-in-the-loop testing
- D03 Deep Verification — fuzzing, mutation testing, formal proofs

Human gates (mandatory, cannot be bypassed):
- Safety-critical releases — Tier 3. Human life at stake. No autonomous deploy.
- External attestation — FCC, CE, UL hardware certification requires independent assessor signature
- Irreversible actions — key rotation, destructive migrations are human-gated

### 9.2 Palantir-Type Software (Data Integration, Ontology, Analytics)

Data and Analytics:
- C04 Data and Schema Builder — schemas, migrations, pipelines, analytics models
- Data Engineer — ETL/ELT, data lakes, warehouses
- Analytics Engineer / BI Developer — metrics layers, models, dashboards
- Data Architect — enterprise data models, flows, ownership
- Search / Relevance Engineer — ranking, vector search, retrieval
- Data Scientist + ML Research Scientist — statistics, modeling

AI/ML Layer:
- C05 AI/ML Builder — models, prompts, agents, retrieval systems
- ML/AI Architect — model lifecycle, serving strategy
- MLOps / AI Infrastructure Engineer — inference pipelines, quantization, GPU acceleration
- LLMOps / Evaluation Engineer — eval harnesses, guardrails, drift monitoring

Integration and Platform:
- C02 Backend and Integration Builder — services, APIs, SDKs, integrations
- Integration / API Architect — event buses, API gateways, inter-service contracts
- Platform Engineer — internal developer portals, self-service provisioning
- Kubernetes / Container Platform Engineer — clusters, service mesh

Security and Compliance:
- B07 Threat Modeling and Security Architecture — attack paths, security requirements at design time
- D05 AppSec Critic — SAST/DAST, vulnerability triage, crypto review
- D07 Adversarial Red Team — attacks the product and the factory itself
- E10 Security Operations and Identity — SOC, detection engineering, IAM
- B04 Regulatory and Privacy Analyst — GDPR, HIPAA, SOC 2, PCI, sector rules
- Data Governance / Compliance Engineer — lineage, anonymization, privacy rules
- Data Retention / Deletion Specialist — retention windows, right-to-erasure

### 9.3 NASA-Type Software (Flight, Scientific, Ground Systems)

Flight and Avionics:
- C06 Systems, Embedded and Hardware Builder — firmware, drivers, toolchains for spacecraft, rovers, satellites
- Automotive / Avionics Safety Engineer (in D03) — DO-178C compliance
- Formal Verification Engineer (in D03) — proves safety/liveness properties with TLA+, Coq, model checkers
- HIL / Hardware Test Engineer (in D04) — hardware-in-the-loop testing
- Controls Engineer — feedback and control loops (attitude control, trajectory correction)
- Autonomy / Perception Engineer — planning and sensing for rovers

Scientific and Simulation:
- Scientific / HPC Engineer (C14) — simulations, GPU-cluster workloads, digital twins
- Digital Twin / Simulation Engineer — virtual replicas of spacecraft
- Computer Vision / SLAM Engineer — tracking, mapping, spatial understanding
- DSP / Audio Engineer — signal processing for telemetry
- Telecom / 5G Engineer (C14) — carrier-grade network functions, deep space communications

Ground Systems and Operations:
- Backend and Integration Builder (C02) — mission control systems, telemetry processing
- Observability and SRE (E04) — monitoring, dashboards, alerts
- Incident and Recovery (E05) — incident response, postmortems, disaster recovery
- Data Governance (E09) — lineage, retention, deletion

Safety Gates (mandatory, human-gated, cannot be bypassed):
- Safety-critical releases — Tier 3. Human life at stake. No autonomous deploy.
- Formal verification proofs — D03 produces proofs, but human signs off
- External attestation — independent assessor signature required

## 10. Skill Repos Merged into The Agency

Three skill repositories were cloned and merged into D:/software factory (The Agency):

| Repo | Skills | Notable |
|------|--------|---------|
| mmondora/claude-skills | 1,369 | Broad coverage |
| borghei/claude-skills | 386 | Incident commander, observability designer, release manager, feature flags architect, delivery manager |
| popey/claude-code-skills | 4,497 | observability-engineer and others |

Installed via: npx skills add repo --skill * --global --agent * -y

These provide the skill library that The Agency factory uses for domain-specific agent capabilities. The factory plan (Phase 1-6) describes how these skills get integrated into the governed execution pipeline.

## 11. Complete Factory Plan (from docs/FORGE_FACTORY_PLAN.md)

Phase 1 — Governance files (markdown, model-agnostic) [low risk, high leverage]
- Write MISSION.md (what the product is + out-of-scope list of >=5 plausible-but-wrong requests)
- Write AGENTS.md / FACTORY_RULES.md (triage rules, PR size limits, quality gates, mandatory browser testing)
- Write harness/END-TO-END.md (2-5 user journeys in plain English, naming expected value)
- Write .factory/holdout/HOLDOUT.md (independent scenarios; keep private from builder)

Phase 2 — Isolation
- Git worktree per feature/issue. Each agent gets its own station; never edit main directly.

Phase 3 — Build
- Bounded coding agent: takes a plan, applies edits via patch, then runs inspection + scan + tests
- Code-structure skill: service layer with explicit inputs/structured returns

Phase 4 — Prove (evidence-driven)
- Before/after capture: screenshots, video, or numbers
- Scenario-based validation: run real user journeys against a running app
- Holdout runner: separate validator workflow the builder cannot see

Phase 5 — Ship
- AI reviewer loop: independent reviewer scores the PR; loop back to build until threshold
- Merge queue: reads required checks + protected paths, seals plan by script. Human approves merge.
- Protected paths list: factory never touches infra/secrets/config without approval

Phase 6 — Autonomy (optional, last)
- Scheduling via systemd/cron timer; discovery publishes verified findings as new issues
- PRD to backlog slicing
- Cost instrumentation: token tracking, medium models routine, large for reasoning

Safety rails throughout:
- Never let the builder see holdout scenarios
- Keep inspection gate process-free; subprocess only in isolated test runner
- Merge never auto-deploys without human approval (at least at first)
- Protected paths enforced by script, not by prompt

Suggested first concrete step: Do Phase 1 (four markdown files) + Phase 2 (worktree isolation helper) first. Then Phase 4 (evidence + holdout runner). Coding agent (Phase 3) comes after the gates exist.

## 12. The Agency — Current Architecture

                    HUMAN
                      |
                    BUTLER (human interaction + scoped context)
                      v
                ORCHESTRATOR (task submit/execute)
                      |
        +-------------+-------------+
        |                           |
      AGENTS                       TOOLS
      - research                    - registry + driver
      - general                     - web_search / web_fetch / memory /
      - demo / planner /              sandbox_exec adapters
        executor / verifier
                      |
        +-------------+-------------+
        |             |             |
      LATTICE       MEMORY      POLICIES / AUDIT / SANDBOX
      coordination/ governance  scoped stores   kernel policies,
      substrate     + retrieval audit log,      secrets, sandbox
                    (src/agency/  (src/agency/  isolation
                     memory/sms/) kernel/)

PARTIAL: thread/workspace store, skill registry, workflow runner, Agent Factory v1, read-only Forge inspection gate.
PLANNED: integrated coding/release Forge, authenticated thread API.

Cross-cutting (partial, code-enforced where noted): security policies, audit, provenance/evidence, sandbox isolation, adversarial QA critics.

## 13. Platform Boundary

- ATHENA is a separate peer platform, not an Agency component. No Agency core capability depends on ATHENA.
- NYX is a separate critic service. The Agency reviewer must be Agency-native (local heuristic or configured LLM provider), never NYX.
- External bridges (Claude, Codex, Hermes, OpenClaw) are partial adapters behind explicit boundaries, never architectural dependencies.

## 14. Honest Assessment

The knowledge base (skills, patterns, research, hardware sizing) covers a complete SDLC on paper. The system to execute it at scale does not exist yet:

- Forge: partial v1 (read-only inspection only)
- Agent Factory: partial v1 (no autonomous creation/evaluation)
- Lattice: partial (in-memory proposals, best-effort backend mirror)
- Memory: partial (scoped per sender, hierarchical isolation planned)
- Sandbox/security/audit: partial (not production-hardened)
- CI: verified on PR #7 (7 checks passed), but CD and live deployment unverified
- Threads/workspaces: partial (no authenticated API or UI)
- Skills/workflows: partial (versioned metadata + bounded allowlisted runner, not integrated with Forge)

Bottom line: Blueprint and parts list — not a built factory. Phase 1+2 of the factory plan is the honest first step.

---

Compiled from research sessions. Last updated: October 2026.
'''

with open('README.md', 'a') as f:
    f.write(extra)
print('appended', len(extra))
'''

with open('/c/Users/PC/agent-sim-research/append_extra.py', 'w') as f:
    f.write(script)
print("script written")