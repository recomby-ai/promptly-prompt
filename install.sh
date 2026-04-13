#!/bin/bash
# promptly-prompt installer
# Copies skill files + configures UserPromptSubmit hook

set -e

SKILL_DIR="$HOME/.claude/skills/promptly-prompt"
SETTINGS="$HOME/.claude/settings.json"

echo "Installing promptly-prompt..."

# 1. Copy skill files
mkdir -p "$SKILL_DIR/scripts"
cp skill/SKILL.md "$SKILL_DIR/"
cp skill/scripts/intercept.py "$SKILL_DIR/scripts/"
chmod +x "$SKILL_DIR/scripts/intercept.py"

echo "  Skill files copied to $SKILL_DIR"

# 2. Configure hook in settings.json
if [ ! -f "$SETTINGS" ]; then
    echo '{}' > "$SETTINGS"
fi

# Check if hook already configured
if python3 -c "
import json, sys
with open('$SETTINGS') as f:
    d = json.load(f)
hooks = d.get('hooks', {}).get('UserPromptSubmit', [])
for h in hooks:
    for sub in h.get('hooks', []):
        if 'promptly-prompt' in sub.get('command', ''):
            sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
    echo "  Hook already configured, skipping."
else
    python3 -c "
import json
with open('$SETTINGS') as f:
    d = json.load(f)
d.setdefault('hooks', {}).setdefault('UserPromptSubmit', []).append({
    'matcher': '',
    'hooks': [{
        'type': 'command',
        'command': 'python3 ~/.claude/skills/promptly-prompt/scripts/intercept.py'
    }]
})
with open('$SETTINGS', 'w') as f:
    json.dump(d, f, indent=2)
"
    echo "  Hook added to $SETTINGS"
fi

echo ""
echo "Done! Start a new Claude Code session to activate."
