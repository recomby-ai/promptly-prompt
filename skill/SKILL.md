---
name: promptly-prompt
description: |
  Prompt optimization through context, not decoration. Trigger when user asks
  to optimize, improve, or write a prompt for any AI model. Applies three
  disciplines: AI cognition awareness (hallucination, context dependency),
  deep requirement understanding (including implicit needs), and method search
  (find existing frameworks/tools before building from scratch).
---

# promptly-prompt

AI answer quality depends on context quality, not prompt tricks.

This skill operates via a `UserPromptSubmit` hook that automatically injects
three disciplines into complex requests:

1. **Cognition check** — remind the AI what it is: a model that hallucinates,
   only knows what's in context, and amplifies thinking rather than replacing it.

2. **Requirement understanding** — deeply understand what the user wants,
   surface implicit needs, flag ambiguities, show understanding to user, wait
   for confirmation before executing.

3. **Method search** — for every complex problem, think about what domain it
   belongs to and search for existing methodologies, frameworks, open-source
   projects, or proven patterns before building from scratch.

The hook script at `scripts/intercept.py` scores prompt complexity using
rule-based signals (word count, multi-step indicators, ambiguity words, etc.).
Simple commands pass through untouched. Complex requests get the full injection.

## Explicit Invocation

When invoked directly (e.g., user says "optimize this prompt"), take the user's
raw prompt and apply the three disciplines manually: check what AI cognition
gaps might cause problems, deeply understand the requirement, and search for
existing methods. Then rewrite the prompt with the missing context filled in.
