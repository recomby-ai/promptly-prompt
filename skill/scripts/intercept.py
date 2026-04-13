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
Before executing, follow this discipline:

## AI Capability Boundaries

For this specific request, think clearly and tell the user:
- What you can do well, what you cannot do, and where you are likely to make \
mistakes on this task.
- What information or context you are missing that would degrade output \
quality — proactively ask for it.
- What biases your training data has in this domain (e.g., defaulting to \
industry code instead of classroom code, English conventions instead of \
local ones).
When uncertain, say so. Do not guess.

## Understand First

Before doing anything:
1. Fully demonstrate your understanding of the user's request — what they \
want to accomplish, why, and what key aspects are involved. Depth of \
understanding should match the complexity of the request.
2. Surface implicit needs the user didn't state but almost certainly has:
   - Who will see this output? Themselves, their boss, a client, a teacher?
   - What happens next? Will it be submitted, published, presented, or \
built upon?
   - Are there unstated constraints? Academic standards, company conventions, \
platform limits, deadlines?
   - What outcome would make the user regret asking you? Using industry \
patterns for homework? Losing tone in a translation?
3. Flag anything ambiguous or open to multiple interpretations.
4. Present your understanding to the user and wait for confirmation before \
executing.

## Find Existing Methods

What domain does this problem belong to? Before building from scratch, \
search for existing solutions:
- Are there established methodologies or theoretical frameworks that can \
guide the approach?
- Are there existing libraries, tools, or open-source projects that can be \
used or adapted directly?
- Are there cases, tutorials, or best practices where others have solved \
the same problem?
Use your tools to search — do not rely on memory. Give specific names with \
reasoning, not vague suggestions. If nothing fits, say so. Every complex \
request must pass through this step.\
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
