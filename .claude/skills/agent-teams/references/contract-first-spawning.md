# Contract-First Spawning — Deep Dive

Contract-first spawning is the core orchestration pattern for Agent Teams. It ensures all parallel agents build against verified interfaces, preventing the #1 failure mode: interface divergence.

---

## 1. The Problem: Interface Divergence

When agents run in parallel without coordination, each makes assumptions about the other's interfaces. The backend builds endpoints the frontend doesn't expect. The API uses a database schema that hasn't been finalized. From Cole Medin's testing: "the backend agent almost was done with its work" before getting the correct database schema — wasting most of its implementation.

**Why it happens:** Agents don't have shared context. Each works from its own interpretation of the plan. Without explicit contracts, interpretations diverge.

---

## 2. The Solution: Contract-First Spawning

Instead of spawning all agents simultaneously, spawn them in **dependency order**. Each upstream agent publishes its interface contract BEFORE downstream agents start. The lead verifies and relays every contract.

```
Upstream Agent → publishes contract → Lead verifies → relays to Downstream Agent
```

Contracts are the source of truth. Once verified, downstream agents build against the contract — not assumptions.

---

## 3. Identifying the Contract Chain

Analyze the plan to determine: **what depends on what?**

**Common patterns:**

| Pattern | Chain | Example |
|---------|-------|---------|
| Web application | `Database → Backend → Frontend` | Most full-stack features |
| Data-driven app | `Schema → API → UI` | Dashboard, analytics |
| Library project | `Core library → Consumers` | SDK development |
| Shared types | `Shared types → Backend + Frontend` | TypeScript monorepo |
| Independent modules | No chain — all parallel | Documentation, DevOps, unrelated features |

**How to identify:**
1. Read the plan's task list and file dependencies
2. Look for: database schemas, API endpoints, type definitions, shared interfaces
3. Ask: "If Agent A changes its output, does Agent B break?" If yes → A is upstream of B
4. If no dependencies exist → agents are independent (use Independent template)

---

## 4. The Lead's Role: Active Contract Relay

The lead is the **single source of truth** for all contracts. Responsibilities:

1. **Analyze the plan** to identify the contract chain
2. **Spawn the most upstream agent first** with instructions to publish its contract before implementing
3. **Wait for contract publication** — not full completion, just the contract (schema, types, signatures)
4. **Verify the contract** — check for:
   - Completeness (all tables, endpoints, types defined?)
   - Ambiguities (vague types, unclear naming?)
   - Missing fields (foreign keys, error responses, edge cases?)
5. **Forward verified contract** to the next downstream agent's spawn prompt
6. **Continue** until all agents are spawned

**Anti-pattern: "Just share your API with the frontend agent."** Agents messaging each other directly leads to unverified, ambiguous interfaces. The lead must be the relay — it's the only agent that has context across all contracts.

---

## 5. Spawn Prompt Template

Every teammate spawn prompt must include these 5 sections:

```markdown
You are the [ROLE] agent for [FEATURE].

**Ownership**:
- Files you OWN: [specific directories/files — only these]
- Files you must NOT touch: [everything else]

**Scope**: [What this agent builds — specific deliverables]

**Mandatory Communication — CONTRACT FIRST**:
Before implementing ANYTHING, publish your contract to the lead:
- [What to publish: schema, API endpoints, type definitions, etc.]
The lead will verify and forward your contract to downstream agents.
Only begin implementation AFTER the lead confirms your contract.

**Contract you MUST conform to** (verified by lead):
[Paste the verified upstream contract here — exact schema, signatures, types]

**Cross-Cutting Concerns**:
- [Shared conventions: URL patterns, error shapes, auth approach, etc.]
- [Which agent owns each concern]

**Validation**: Before reporting done, run: [domain-specific commands]

**Turn limit**: If 30+ turns without progress, report blockers to the lead.
**Logging**: Write progress to logs/team-{feature}/, send concise summaries via messages.
```

See `templates/TEAM-SPAWN-PROMPTS.md` for 4 ready-to-use template variants (upstream, downstream, terminal, independent).

---

## 6. 5-Phase Collaboration Flow

### Phase 1: Contracts (Sequential, Lead-Orchestrated)

The most critical phase. Gets interfaces right before any coding begins.

1. Lead spawns **upstream agent** (e.g., Database) with instructions to publish contract first
2. Upstream agent publishes contract (schema, types, function signatures)
3. Lead **verifies** contract — checks completeness, flags ambiguities
4. Lead spawns **downstream agent** (e.g., Backend) with verified contract pasted in prompt
5. Downstream agent publishes its own contract (API endpoints, response shapes)
6. Lead verifies and relays to the next downstream agent (e.g., Frontend)
7. Independent agents (testing, docs) can be spawned in parallel — they don't need upstream contracts

### Phase 2: Implementation (Parallel)

All agents code against verified contracts. This phase runs in parallel because contracts are settled.

- Each agent works in its own worktree
- Agents follow ownership boundaries — only modify their own files
- Progress updates via messages to the lead

### Phase 3: Pre-Completion Contract Verification (Lead-Driven)

Before agents report done, the lead verifies implementations match contracts:

- Compare actual database schema against published schema contract
- Compare actual API endpoints against published API contract
- Flag any drift — if an agent deviated from contract, they must fix before completing

### Phase 4: Polish (Cross-Review)

Agents review each other's integration points:

- Backend agent reviews frontend's API calls against its endpoints
- Database agent reviews backend's queries against its schema
- Fix any mismatches found

### Phase 5: Lead End-to-End Validation

Lead performs final validation:

1. Merge worktrees sequentially (upstream first)
2. Run full test suite after each merge
3. Run integration tests across all components
4. If all pass → implementation complete
5. If failures → identify which contract was violated, fix, re-validate

---

## 7. Validation Within the Team

Two levels of validation ensure quality:

**Agent-level** (each agent, before reporting done):
- Run domain-specific tests (unit tests, type checks, linting)
- Verify implementation matches the contract they were given
- Report validation results to the lead

**Lead-level** (after all agents complete):
- Pre-completion contract verification (Phase 3)
- Cross-agent integration review (Phase 4)
- End-to-end validation after merging (Phase 5)

---

## 8. Cross-Cutting Concerns

Shared conventions that multiple agents must follow. Assign ownership to ONE agent (usually the most upstream).

| Concern | Owner | Consumers | Example |
|---------|-------|-----------|---------|
| URL patterns | Backend | Frontend | `/api/v1/users` (trailing slash? plural?) |
| Error response shape | Backend | Frontend | `{ error: string, code: number }` |
| Date format | Database | Backend, Frontend | ISO 8601 strings vs Unix timestamps |
| Auth approach | Backend | Frontend | JWT in header vs cookie |
| Streaming protocol | Backend | Frontend | SSE vs WebSocket vs polling |

Include cross-cutting concerns in EVERY spawn prompt. The owning agent defines the convention; all others follow it.

---

## 9. Example: 3-Agent Full-Stack Team

**Feature**: User authentication with login, registration, and session management.

**Contract chain**: `Database → Backend → Frontend`

**Step 1**: Lead spawns Database agent.
- Prompt includes: own `db/` directory, publish schema before implementing
- Database agent publishes:
  ```
  Contract: users table (id, email, password_hash, created_at)
  Functions: create_user(email, password) → User, get_user_by_email(email) → User | null
  ```

**Step 2**: Lead verifies schema. Checks: password_hash not password, created_at has default, functions return types clear. Verified.

**Step 3**: Lead spawns Backend agent with verified schema.
- Prompt includes: own `api/` directory, conform to DB schema, publish API endpoints
- Backend agent publishes:
  ```
  Contract: POST /api/auth/register { email, password } → 201 { user }
  POST /api/auth/login { email, password } → 200 { token, user }
  GET /api/auth/me (Authorization: Bearer) → 200 { user }
  Error shape: { error: string, status: number }
  ```

**Step 4**: Lead verifies API contract. Checks: endpoints match DB functions, error shape consistent, auth header documented. Verified.

**Step 5**: Lead spawns Frontend agent with verified API contract.
- Prompt includes: own `ui/` directory, conform to API contract, no contract to publish (terminal agent)

**Step 6**: All three agents implement in parallel. Lead monitors progress.

**Step 7**: Lead runs contract verification — compares actual implementations against published contracts. Fixes any drift.

**Step 8**: Lead merges worktrees: database → backend → frontend. Runs tests after each merge. Full suite passes. Done.
