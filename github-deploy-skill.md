# GitHub Multi-Account Deploy Skill

## Overview

This skill enables deploying code to different GitHub accounts by dynamically overriding remote URLs, regardless of how repositories were originally cloned.

### Account Mapping
- **Personal**: `github-personal` → `Arpit-Singh320` (arpit2005singh@gmail.com)
- **Work**: `github-work` → `AP-Compliledger` (arpit@compliledger.com)

### SSH Configuration
- `~/.ssh/id_ed25519` → Personal account
- `~/.ssh/id_ed25519_work` → Work account
- SSH aliases in `~/.ssh/config` handle identity selection

---

## Core Problem Solved

Most repositories are cloned with standard GitHub URLs:
```bash
git@github.com:username/repo.git
```

This doesn't specify which SSH key/account to use. This skill **dynamically rewrites the remote URL** before pushing.

---

## Skill: Deploy to Personal Account

### Command Sequence:
1. **Get current repository name**:
   ```bash
   REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
   ```

2. **Override remote to personal account**:
   ```bash
   git remote set-url origin git@github-personal:Arpit-Singh320/$REPO_NAME.git
   ```

3. **Push to personal account**:
   ```bash
   git push origin main
   ```

### AI Agent Execution:
```bash
#!/bin/bash
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
git remote set-url origin git@github-personal:Arpit-Singh320/$REPO_NAME.git
echo "🚀 Deploying to PERSONAL account (Arpit-Singh320)..."
git push origin main
```

---

## Skill: Deploy to Work Account

### Command Sequence:
1. **Get current repository name**:
   ```bash
   REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
   ```

2. **Override remote to work account**:
   ```bash
   git remote set-url origin git@github-work:AP-Compliledger/$REPO_NAME.git
   ```

3. **Push to work account**:
   ```bash
   git push origin main
   ```

### AI Agent Execution:
```bash
#!/bin/bash
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
git remote set-url origin git@github-work:AP-Compliledger/$REPO_NAME.git
echo "🚀 Deploying to WORK account (AP-Compliledger)..."
git push origin main
```

---

## Universal Deploy Script (AI Agent Ready)

### Complete Script:
```bash
#!/bin/bash

ACCOUNT=$1
BRANCH=${2:-main}

# Validate input
if [ "$ACCOUNT" != "personal" ] && [ "$ACCOUNT" != "work" ]; then
    echo "❌ Usage: deploy [personal|work] [branch]"
    exit 1
fi

# Get current repository name automatically
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))

if [ "$ACCOUNT" == "personal" ]; then
    USERNAME="Arpit-Singh320"
    HOST="github-personal"
elif [ "$ACCOUNT" == "work" ]; then
    USERNAME="AP-Compliledger"
    HOST="github-work"
fi

# Set correct remote dynamically
git remote set-url origin git@$HOST:$USERNAME/$REPO_NAME.git

echo "🚀 Deploying to $ACCOUNT account ($USERNAME)..."
echo "📁 Repository: $REPO_NAME"
echo "🌿 Branch: $BRANCH"
echo "🔗 Remote: git@$HOST:$USERNAME/$REPO_NAME.git"

# Push to specified branch
git push origin $BRANCH

echo "✅ Deploy completed to $ACCOUNT account"
```

---

## Usage Examples

### Deploy to Personal Account:
```bash
deploy personal
# or with specific branch
deploy personal dev
```

### Deploy to Work Account:
```bash
deploy work
# or with specific branch  
deploy work staging
```

---

## Critical Requirements

### 1. Repository Name Consistency
Local repository names must match GitHub repository names:
```bash
# Local folder: my-project
# Must exist as: 
# - github.com/Arpit-Singh320/my-project (personal)
# - github.com/AP-Compliledger/my-project (work)
```

### 2. SSH Configuration
Your `~/.ssh/config` must contain:
```bash
# Personal account
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# Work account  
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

### 3. Repository Existence
Target repositories must exist on the respective GitHub accounts before deployment.

---

## Safety Rules

✅ **Safe Operations:**
- Only modifies remote URL temporarily
- Uses SSH keys (no password exposure)
- Validates account parameters

❌ **Never Do:**
- Expose private SSH keys
- Hardcode credentials in scripts
- Push to non-existent repositories

---

## Error Handling

### Common Issues & Solutions:

1. **Repository doesn't exist on target account**:
   ```bash
   # Error: remote: Repository not found
   # Solution: Create repository on GitHub first
   ```

2. **SSH key not working**:
   ```bash
   # Test connection:
   ssh -T git@github-personal
   ssh -T git@github-work
   ```

3. **Wrong branch name**:
   ```bash
   # Check available branches:
   git branch -a
   ```

---

## Advanced Features

### Auto-Detect Account from Git Email:
```bash
CURRENT_EMAIL=$(git config user.email)
if [ "$CURRENT_EMAIL" == "arpit2005singh@gmail.com" ]; then
    ACCOUNT="personal"
elif [ "$CURRENT_EMAIL" == "arpit@compliledger.com" ]; then
    ACCOUNT="work"
fi
```

### Multi-Branch Support:
```bash
# Deploy specific branch
deploy personal feature-branch
deploy work hotfix-branch
```

### Pre-Deploy Validation:
```bash
# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory not clean. Commit changes first."
    exit 1
fi
```

---

## AI Agent Integration

### Command Mapping:
```json
{
  "deploy_personal": "deploy personal",
  "deploy_work": "deploy work",
  "deploy_personal_branch": "deploy personal {branch}",
  "deploy_work_branch": "deploy work {branch}"
}
```

### Execution Flow:
1. Read skill file for context
2. Validate parameters
3. Execute command sequence in order
4. Handle errors gracefully
5. Report success/failure

---

## Why This Architecture Works

✅ **No per-repo scripts needed**
✅ **Works with any existing repository**
✅ **Explicit account selection**
✅ **SSH handles identity automatically**
✅ **AI agent can read and execute**
✅ **Centralized skill definition**

---

## SSH Agent Notes

### With Passphrase (Optional):
```bash
# Load keys into memory
ssh-add ~/.ssh/id_ed25519
ssh-add ~/.ssh/id_ed25519_work

# Check loaded keys
ssh-add -l
```

### Without Passphrase (Your Setup):
- SSH agent is optional
- Keys work directly
- No additional setup needed

---

## One-Command Setup

Create the universal deploy command:
```bash
# Create global script
sudo nano /usr/local/bin/deploy
# Paste the universal script above
sudo chmod +x /usr/local/bin/deploy
```

Now you can run from any directory:
```bash
deploy personal
deploy work
```
