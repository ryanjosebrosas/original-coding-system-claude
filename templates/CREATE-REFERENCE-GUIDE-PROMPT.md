# Create On-Demand Reference Guide

> Copy this prompt into a conversation to generate a task-specific reference guide.
> Save the output to `reference/{task_type}_guide.md`.

---

Help me create an on-demand reference guide for a specific task type in my project. This guide will be stored in a `reference/` folder and loaded only when working on this specific type of task.

## What I Need

I want to create a reference guide for: **[DESCRIBE TASK TYPE]**

Research best practices and conventions from this resource: **[PASTE LINK HERE]**

## Instructions

Create a concise, actionable reference guide following this structure:

### Required Sections:

1. **Title and Purpose** — what task type this covers, when to use it
2. **Overall Pattern** — high-level overview, visual diagram if applicable
3. **Step-by-Step Instructions** — 3-6 clear steps, each with code examples and key rules
4. **Quick Checklist** — checkbox summary of all steps

### Critical Requirements:

- **Length: 50-200 lines MAXIMUM**
- **Code-heavy, explanation-light** — show more than tell
- **No generic advice** — specific to this task type and codebase
- **Real examples** — based on best practices from the provided resource
- **Actionable** — a developer should be able to follow it step-by-step

## Process:

1. Research the provided link thoroughly
2. Analyze the existing codebase for matching patterns
3. Create the guide following the structure above
4. Keep it focused — ONE task type only, no general principles (those belong in CLAUDE.md)

Save the guide as `reference/{task_type}_guide.md`.
