---
name: promptly-prompt
description: |
  Prompt optimization through context, not decoration. Trigger when user asks
  to optimize, improve, or write a prompt for any AI model. Applies three
  disciplines: AI capability boundaries (what AI can/can't do for this task),
  deep requirement understanding (including implicit needs, audience, constraints,
  failure modes), and method search (find existing frameworks/tools/patterns
  before building from scratch).
---

# promptly-prompt

AI answer quality depends on context quality, not prompt tricks.

This skill operates via a `UserPromptSubmit` hook that automatically injects
three disciplines into complex requests:

1. **AI capability boundaries** — force AI to state what it can and can't do
   for this task, what context it's missing, and what biases it has.

2. **Requirement understanding** — deeply understand what the user wants,
   surface implicit needs (audience, downstream use, unstated constraints,
   failure modes), flag ambiguities, show understanding to user, wait for
   confirmation before executing.

3. **Method search** — for every complex problem, search for existing
   methodologies, frameworks, open-source projects, or proven patterns.
   Use tools to search, give specific names with reasoning, not vague
   suggestions. If nothing fits, say so.

The hook script at `scripts/intercept.py` scores prompt complexity using
rule-based signals. Simple commands pass through untouched. Complex requests
get the full injection.

## Explicit Invocation

When invoked directly (e.g., user says "optimize this prompt"), take the user's
raw prompt and apply the three disciplines manually: assess AI capability
boundaries for the task, deeply understand the requirement including implicit
needs, and search for existing methods. Then rewrite the prompt with the
missing context filled in.
