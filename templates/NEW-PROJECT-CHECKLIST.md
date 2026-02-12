# New Project Checklist

> Use this when starting a new project with the AI Coding Template.
> Follow the ordering — PRD first, then global rules, then on-demand context.

---

## Phase 1: PRD (Define What to Build)

- [ ] Start a vibe planning conversation — explore the problem space, research options
- [ ] Create your PRD using `templates/PRD-TEMPLATE.md`
- [ ] Define MVP scope clearly (in-scope vs out-of-scope)
- [ ] Save to `reference/PRD.md` (on-demand context for future sessions)
- [ ] Git commit the PRD: `git commit -m "plan: PRD for {project}"`

---

## Phase 2: Global Rules (Define How to Build)

- [ ] Run `/init-c` to generate your CLAUDE.md (or copy and fill in manually)
- [ ] Use the PRD to inform tech stack, architecture, and convention decisions
- [ ] Review the generated CLAUDE.md — does it match your project?
- [ ] Fill in or adjust all sections: Core Principles, Tech Stack, Architecture, Code Style, Logging, Testing, Dev Commands
- [ ] Create `sections/` directory if going modular (split sections into separate files with @references)
- [ ] Git commit your CLAUDE.md

See the example CLAUDE.md structure in your project's `sections/` directory for reference.

---

## Phase 3: On-Demand Context (Reference Guides)

- [ ] Create `reference/` directory for on-demand guides
- [ ] Create `requests/` directory for feature plans
- [ ] Identify your most common task types (e.g., "building API endpoints", "creating components")
- [ ] For each task type, use `templates/CREATE-REFERENCE-GUIDE-PROMPT.md` to generate a guide
- [ ] Save guides to `reference/{task_type}_guide.md`
- [ ] Add references to your CLAUDE.md so the AI knows when to load them
- [ ] Copy templates you need from this repo to your `templates/` directory

---

## Phase 4: Reconcile Layer 1

- [ ] Validate no contradictions between PRD, CLAUDE.md, and reference guides
- [ ] Ask the AI to inspect all Layer 1 artifacts for inconsistencies
- [ ] Resolve any conflicts — all Layer 1 planning must work together

---

## Phase 5: First Feature (Plan)

- [ ] Look at the PRD — pick the first small feature to build
- [ ] Start a conversation — vibe plan with the AI (see `templates/VIBE-PLANNING-GUIDE.md`)
- [ ] Explore the codebase, discuss options, add constraints
- [ ] Ask the AI to create a structured plan using `templates/STRUCTURED-PLAN-TEMPLATE.md`
- [ ] Review the plan — does it cover all 4 pillars? (Memory, RAG, Prompt Engineering, Task Management)
- [ ] Save to `requests/{feature}-plan.md`
- [ ] Git commit the plan: `git commit -m "plan: {feature} structured plan"`

---

## Phase 6: First Feature (Implement + Validate)

- [ ] Start a **new conversation** (fresh context)
- [ ] Feed the plan using `templates/IMPLEMENTATION-PROMPT.md`
- [ ] Let the AI implement — watch loosely, don't micromanage
- [ ] Run validation using `templates/VALIDATION-PROMPT.md`
- [ ] Review the git diff yourself
- [ ] If issues: fix small ones directly, revert big ones and tweak the plan
- [ ] Commit when satisfied

---

## Repeat

Every new feature follows Phase 5 + Phase 6. Reference the PRD to choose the next logical feature. That's the PIV Loop.
