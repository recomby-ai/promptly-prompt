#!/usr/bin/env python3
"""promptly-prompt hook: complexity judge + context injection.

Fires on every UserPromptSubmit. Simple prompts pass through.
Complex prompts inject the promptly-prompt discipline:
  1. AI cognition baseline
  2. Deep requirement understanding (including implicit needs)
  3. Search for existing methods/frameworks before acting

No external dependencies. Python stdlib only.
"""

import json
import re
import sys


MULTI_STEP = re.compile(
    r"\b(then|after that|next|first\b.{0,30}\bthen|and also|followed by|"
    r"once .{0,30} (is |are )?done|step \d)"
    r"|然后|接着|并且|首先|之后|同时|再|最后",
    re.IGNORECASE,
)

AMBIGUITY = re.compile(
    r"\b(maybe|perhaps|something like|probably|not sure|might|could be|"
    r"kind of|sort of|or something)"
    r"|大概|可能|之类的|差不多|好像|应该|或者说|不太确定",
    re.IGNORECASE,
)

IMPERATIVE_START = re.compile(
    r"^(read|fix|run|show|list|open|close|delete|move|copy|create|"
    r"write|edit|add|remove|install|update|check|test|build|deploy|"
    r"push|pull|commit|merge|grep|find|cat|ls|cd|git|npm|pip|docker|"
    r"make|curl|ssh|scp|kill|restart|stop|start|help|explain|describe|"
    r"读|改|跑|看|删|装|查|测|建|推|拉)",
    re.IGNORECASE,
)

CODE_BLOCK = re.compile(r"```|`[^`]+`|[~/\.]\S+\.\w{1,5}\b|\/\S+\/\S+")
SLASH_CMD = re.compile(r"^/\w+")


def count_sentences(text: str) -> int:
    parts = re.split(r"[.!?。！？\n]+", text)
    return sum(1 for p in parts if p.strip())


def score(prompt: str) -> int:
    s = 0
    if len(prompt.strip()) < 10:
        s -= 3
    if len(prompt.split()) > 80:
        s += 2
    if count_sentences(prompt) > 3:
        s += 1
    if prompt.count("?") + prompt.count("？") > 1:
        s += 1
    if MULTI_STEP.search(prompt):
        s += 2
    if AMBIGUITY.search(prompt):
        s += 1
    if CODE_BLOCK.search(prompt):
        s -= 2
    if IMPERATIVE_START.match(prompt.strip()):
        s -= 1
    if SLASH_CMD.match(prompt.strip()):
        s -= 3
    return s


INJECTION = """\
You are about to respond to a complex request. Before executing, follow this \
discipline:

## Cognition Check

Remember what you are: a language model that predicts plausible next tokens. \
This means:
- You hallucinate. You will confidently state things that are wrong. When \
uncertain, say so.
- You only know what's in your context. If the user hasn't provided it, you \
don't have it — ask for it or go find it, don't guess.
- You are not the user's brain. Your job is to amplify their thinking, not \
replace it.
- Context determines your output quality far more than any prompting trick. \
Missing context produces mediocre answers no matter how clever the prompt.

## Requirement Understanding

Before doing anything:
1. Demonstrate your full understanding of what the user wants — what they're \
trying to accomplish, why, and what's involved. Don't summarize, show depth \
proportional to the request's complexity.
2. Surface implicit needs the user didn't state but almost certainly has. \
Think about: who is the audience, what happens to the output next, what \
quality standards apply, what would frustrate them if you got it wrong.
3. Flag anything ambiguous or open to multiple interpretations.
4. Present this understanding to the user and wait for confirmation before \
executing.

## Method Search

For the problem at hand, think: what domain does this belong to? Is there an \
existing methodology, framework, open-source project, established best \
practice, or known solution pattern that applies? Human knowledge is vast — \
search for what already exists before building from scratch. Use existing \
tools, adapt proven approaches, stand on shoulders of giants. This is not \
optional — think about this for every complex request.\
"""


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("prompt", "")
    if not prompt.strip():
        return

    if score(prompt) >= 3:
        print(INJECTION)


if __name__ == "__main__":
    main()
