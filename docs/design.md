# promptly-prompt Design Spec

> AI answer quality depends on context quality, not prompt decoration.
> From prompt engineering to context engineering.

## Architecture

One hook script + one skill file. That's it.

```
promptly-prompt/
├── SKILL.md              # Skill description + installation guide
├── scripts/
│   └── intercept.py      # Hook: complexity judge + three-discipline injection
├── LICENSE
└── docs/
    └── design.md         # This file
```

## How It Works

`intercept.py` fires on every `UserPromptSubmit`. Reads prompt from stdin JSON.
Scores complexity via rule-based signals (word count, multi-step words, ambiguity
words, code blocks, imperative verbs — bilingual EN/CN). No API calls, stdlib only.

- **simple (score < 3):** output nothing, Claude proceeds normally
- **complex (score >= 3):** inject three disciplines as a single prompt block

## The Three Disciplines

1. **Cognition Check** — remind AI what it is: hallucinates, only knows what's
   in context, amplifies thinking not replaces it, context > prompt tricks

2. **Requirement Understanding** — deeply understand what user wants including
   implicit needs, flag ambiguities, show understanding to user, wait for
   confirmation before executing

3. **Method Search** — for every complex problem, think what domain it belongs
   to, search for existing methodologies/frameworks/open-source projects/proven
   patterns before building from scratch. Not optional, not "ask user if they
   want it" — forced thinking discipline.

## Design Decisions

1. **No prompt engineering techniques reference** — Claude already knows CoT,
   Few-shot, etc. Teaching it these wastes context.
2. **No separate AI cognition document** — baked directly into the injection
   prompt. One less file to load.
3. **No implicit patterns reference** — Claude can reason about implicit needs
   on its own when told to think about them.
4. **Method search is forced, not optional** — not "want me to recommend
   methods?" but "you must think about existing methods every time."
5. **Hook does everything** — SKILL.md is just documentation and installation
   guide, not a heavy processing pipeline.

## Installation

1. Copy to `~/.claude/skills/promptly-prompt/`
2. Add hook to `~/.claude/settings.json` under `hooks.UserPromptSubmit`
