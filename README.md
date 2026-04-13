# promptly-prompt

A Claude Code skill that forces AI to **understand before executing**.

> AI answer quality depends on context quality, not prompt decoration.

## What It Does

A `UserPromptSubmit` hook that automatically intercepts complex requests and injects three disciplines:

1. **Cognition Check** — Reminds AI of its limitations: hallucination, context dependency, amplifier not replacer.
2. **Requirement Understanding** — Forces AI to deeply understand your request (including implicit needs), show its understanding, and wait for your confirmation before executing.
3. **Method Search** — Forces AI to search for existing methodologies, frameworks, open-source projects, and proven patterns before building from scratch.

Simple commands (`git status`, `read file.py`, `/commit`) pass through untouched.

## Why

When your brain is foggy, you write bad prompts, get bad answers, and spiral. This hook acts as a guardrail — it forces AI to pause, think, and confirm understanding before diving in. The core insight: most bad AI answers come from missing context, not missing prompt tricks.

## Install

### One-line install

```bash
git clone https://github.com/recomby-ai/promptly-prompt.git && cd promptly-prompt && bash install.sh
```

This copies skill files to `~/.claude/skills/promptly-prompt/` and auto-configures the hook in `settings.json`. Start a new Claude Code session to activate.

### Manual install

1. Copy to your Claude Code skills directory:

```bash
cp -r promptly-prompt ~/.claude/skills/promptly-prompt
```

2. Add the hook to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/promptly-prompt/scripts/intercept.py"
          }
        ]
      }
    ]
  }
}
```

3. Start a new Claude Code session. Done.

## How It Works

The hook script scores every prompt's complexity using rule-based signals:

| Signal | Effect |
|--------|--------|
| Long text (>80 words) | +complex |
| Multiple sentences | +complex |
| Multi-step words ("then", "after that", "然后", "接着") | +complex |
| Ambiguity words ("maybe", "probably", "大概", "可能") | +complex |
| Code blocks / file paths | -complex |
| Imperative verbs ("fix", "run", "git") | -complex |
| Very short (<10 chars) | -complex |

Score >= 3 triggers injection. Below 3 passes through silently.

No API calls. No dependencies beyond Python stdlib. Runs in < 50ms.

## Origin

Inspired by [promptly-prompt](https://www.promptly-prompt.com/), a prompt optimization project built during sophomore year. The original vision was a full prompt optimization pipeline — this skill distills the core insight: **understand first, find existing methods, then act**.

From prompt engineering to context engineering.

## License

MIT
