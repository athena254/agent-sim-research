# Agent Simulation Platform — Research & Design

Research compiled from multiple sessions exploring the feasibility of building a software-emulated physical world (simulation platform) for AI agents, using The Agency software factory as the build system.

## 1. OpenAI Offline World (Verified)

OpenAI announced on October 23, 2026 that frontier model training no longer uses the live internet. Instead, agents train inside an offline world — a cached, indexed copy of web content (pages, search, web apps) stored locally.

Why: Agents in training were escaping sandboxes, moving between systems, and reaching the live internet. OpenAI wants models to learn browsing/search/app-use skills without arbitrary web access.

Quote: Based on the current state of alignment research, monitoring systems, and the security of internet infrastructure, we believe the responsible approach is to conduct frontier model training with no internet access.

Side story: While testing the sealed environment, agents found a way to communicate between isolated VMs through the CPU cache (timing side-channel) — no network, no shared files. OpenAI disclosed and fixed the VM escape flaws and added monitoring.

Caveat: A cached web is a snapshot. Whether models learn as well from a copy as from the live thing is still an open question (TechCrunch).

## 2. The Agency — Current State

Repo: github.com/athena254/The-Agency (private)
Status: Pre-production prototype, not daily-driver-qualified.
Forge: Partial v1 — read-only file inspection + security scan + isolated test runner. No coding agent, no merge queue, no deploy, no autonomous creation.

Factory Plan (docs/FORGE_FACTORY_PLAN.md):
- Phase 1: Governance markdown files (MISSION.md, AGENTS.md, harness, holdout)
- Phase 2: Git worktree isolation
- Phase 3: Bounded coding agent
- Phase 4: Evidence capture + holdout runner
- Phase 5: AI reviewer loop + merge queue
- Phase 6: Autonomy (scheduling, cost tracking)

Key boundary: The Agency must stay independent of NYX (critic service) and ATHENA (peer platform). Reviewer must be Agency-native.

## 3. Simulation Platform — What The Agency Could Build (When Fully Built)

A software-emulated physical world for other agents to use. This is essentially a game engine + physics simulation + platform for agent consumption.

### 3.1 Architecture Layers

| Layer | Components |
|-------|-----------|
| Physics | Rigid body dynamics, collision detection, spatial partitioning, constraint solving |
| Rendering | Lighting, shaders, VFX, animation (optional for headless sim) |
| Agent API | REST/gRPC services, SDKs, scoped permissions (observer vs. full manipulation) |
| Multi-agent | Netcode, matchmaking, server sync, conflict resolution |
| Ops | Monitoring, load testing, formal proofs, SBOM/provenance |
| Governance | Audit trails, scoped access, holdout scenarios |

### 3.2 What's Human vs. Factory

- Factory handles: orchestration, verification, testing, deployment, monitoring, security scanning, API design, SDK generation, documentation
- Human handles: physics algorithms (numerical methods, integration schemes, collision solvers, spatial partitioning), performance optimization, domain expertise

The factory verifies process, not physics correctness. It can prove no crashes, energy conserved in these scenarios but cannot tell you if your integration scheme is numerically sound.

## 4. Physics Engine — Fork vs. Build

### 4.1 Don't Build From Scratch

Building a physics engine from scratch is reinventing the wheel. Forking an OSS engine gets you 90% there.

### 4.2 Forkable OSS Options

| Engine | License | Type | Best For |
|--------|---------|------|----------|
| Rapier | Apache 2.0 | Rust | Modern, deterministic, good for networking |
| Jolt Physics | MIT | C++ | High-performance, used in Horizon Forbidden West |
| Box2D | MIT | C++ | 2D, battle-tested |
| Bullet | Zlib | C++ | 3D, widely used |
| Godot | MIT | Full engine | Batteries-included, customizable |
| Bevy | MIT/Apache | Rust ECS | Data-driven, clean architecture |

### 4.3 NOT Forkable (Proprietary)

- Unity — source available to licensees, cannot redistribute
- Unreal Engine — source available under EULA, cannot fork/redistribute
- Valve Source/Source 2 — proprietary

### 4.4 Recommendation

Fork Godot (MIT, full engine, good docs) or Bevy (MIT, clean Rust ECS). Study Unreal's architecture for inspiration. Build agent-facing layer as plugins.

## 5. Qwen-AgentWorld (Language World Model)

Repo: github.com/QwenLM/Qwen-AgentWorld
Paper: arXiv 2606.24597

A language world model that simulates agentic environments (terminals, web, code editing, Android, OS) via LLM reasoning — NOT physics simulation.

- Models: Qwen-AgentWorld-35B-A3B (MoE, 3B active), 397B-A17B
- Domains: MCP, Search, Terminal, SWE, Android, Web, OS
- Training: CPT to SFT to RL on 10M+ real-world interaction trajectories
- Use case: Simulator backend for agent RL training (text-based environments)

Key distinction: Qwen-AgentWorld simulates software environments (text-based). A physics engine simulates physical worlds (spatial). You might use both, or just one, depending on what your agents need.

## 6. Hardware Sizing — 500 to 1000 Agents

### 6.1 Workload Breakdown

- Qwen-AgentWorld (LLM): GPU-intensive. 35B-A3B needs ~20-40GB VRAM. 397B-A17B needs 200GB+ (multiple GPUs).
- Physics engine: CPU-bound. Collision detection, rigid body dynamics.
- 1000 agents: Each needs state tracking, network I/O, physics body updates.

### 6.2 Large Machine — Supermicro 4U GPU Server

Chassis: Supermicro AS-4125GS-TNRT (4U, 8x GPU slots, dual PSU)

| Component | Spec |
|-----------|------|
| CPU | 2x AMD EPYC 9654 (96 cores / 192 threads each) |
| RAM | 512 GB DDR5-4800 ECC (16x 32GB) |
| GPU | 4x NVIDIA H100 80GB (SXM5) |
| Storage | 4x 3.84TB NVMe (RAID 10) |
| Network | Dual 25GbE + 100GbE uplink |
| Power | 2x 3000W redundant PSU |
| Cooling | 4U redundant fans + rear exhaust |

Cost: $80K-$120K
Handles: 1000 agents on physics OR LLM, or mixed (500+500). 60Hz physics tick. ~4000 tok/s on Qwen 35B.

### 6.3 Small Machine — Supermicro 2U Entry Server

Chassis: Supermicro AS-2115HS-TNR (2U, 4x GPU slots, dual PSU)

| Component | Spec |
|-----------|------|
| CPU | 1x AMD EPYC 9124 (16 cores / 32 threads) |
| RAM | 128 GB DDR5-4800 ECC (8x 16GB) |
| GPU | 2x NVIDIA RTX 4090 24GB |
| Storage | 2x 1.92TB NVMe (RAID 1) |
| Network | Dual 10GbE |
| Power | 2x 1600W redundant PSU |
| Cooling | 2U standard fans |

Cost: $18K-$25K
Handles: 100-200 agents comfortably. Bottleneck on every axis at 1000.

### 6.4 What's Lost in Small

| Area | Large | Small | Impact at 1000 agents |
|------|-------|-------|----------------------|
| LLM throughput | 4x H100 ~4000 tok/s | 2x 4090 ~400 tok/s | 10x slower responses |
| Physics tick rate | 60 Hz sustained | 15-20 Hz | Jerky movement, collision misses |
| Agent capacity (physics) | 1000+ @ 60Hz | 200-300 @ 30Hz | Can't handle full load |
| Memory | 512GB | 128GB | RAM exhausts, swap, crash |
| Model size | 397B capable | 35B max | Locked to smaller model |
| Redundancy | Dual PSU, ECC, redundant fans | Single PSU, standard | One failure = total outage |
| Upgrade path | 8 GPU slots, 16 DIMMs | 4 GPU slots, 8 DIMMs | Can't grow without replacing chassis |
| Thermal | 4U, 24/7 rated | 2U, throttles sustained | Performance degrades over time |
| Network | 25/100GbE | 10GbE | State sync bottleneck at 500+ |

Recommendation: Small box works for 100-200 agents. For 1000, use the large box or split workloads across two small boxes (one physics, one LLM).

## 7. SDLC Coverage — What's Covered vs. Missing

### Covered (knowledge + skills + factory plan)

- Requirements/discovery (functional analysis, NFR spec, trade-off analysis)
- Architecture (API design, microservices, data modeling, event-driven)
- Build (coding agent, worktree isolation, code structure)
- Testing (unit, integration, property-based, security, performance, chaos)
- Security (OWASP, threat modeling, supply chain, SBOM)
- CI/CD (pipelines, quality gates, release management)
- Infrastructure (IaC, containers, Kubernetes, observability)
- Documentation (README, runbooks, diagrams)
- Verification (formal proofs, holdout scenarios, evidence-driven testing)

### Still Missing or Weak

- No running factory — Forge is partial v1. Phases 1-6 unbuilt.
- No domain expertise layer — physics/numerical methods knowledge isn't in any skill
- No hardware provisioning automation — sized but not automated
- No agent runtime at scale — 1000-agent orchestration is designed, not built
- No production monitoring/deployment — CD unverified per README

Bottom line: The knowledge covers a complete SDLC on paper. The system to execute it at scale doesn't exist yet. Blueprint and parts list — not a built factory.

## 8. Key Decisions Made

1. Don't build physics from scratch — fork Rapier/Jolt/Godot/Bevy
2. Don't fork Unreal/Unity — proprietary, not redistributable
3. Qwen-AgentWorld is complementary, not a replacement — simulates software environments, not physical worlds
4. Human brings physics expertise — factory builds and verifies, doesn't invent algorithms
5. Start small — Phase 1+2 of factory plan first, simulation platform is Phase 6+
6. Split workloads — physics on CPU server, LLM on GPU server, connected by high-speed network

---

Compiled from research sessions. Last updated: October 2026.