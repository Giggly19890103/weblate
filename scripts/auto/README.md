# Weblate Automation Scripts

Automate Weblate project setup and translation management using the REST API.

## 📦 Scripts Included

1. **`setup_component.py`** - Complete workflow: create component + add translations (recommended)
2. **`create_component.py`** - Create projects and components
3. **`add_translation.py`** - Add language translations to components

## 🚀 Quick Start

### 1. Install Requirements

```bash
pip install requests
```

### 2. Create Configuration Files

#### `web.json` - Shared authentication config
```json
{
  "weblate_url": "http://localhost:8080",
  "api_token": "wlu_YOUR_TOKEN_HERE"
}
```

> **Security Note**: Keep `web.json` private! Add it to `.gitignore`.

#### `component.json` - Component-specific config
```json
{
  "project": {
    "name": "My Project",
    "slug": "my-project",
    "web": "https://example.com"
  },
  "component": {
    "name": "Main Component",
    "slug": "main",
    "vcs": "git",
    "repo": "git@github.com:user/repo.git",
    "branch": "main",
    "filemask": "locales/*.po",
    "file_format": "po"
  }
}
```

### 3. Get Your API Token

1. Log in to Weblate
2. Go to your profile → Settings
3. Navigate to "API access" tab
4. Copy your API token (starts with `wlu_` or `wlp_`)
5. Add it to `web.json`

### 4. Run Scripts

#### Option A: All-in-One (Recommended)

```bash
# Complete setup: create component + add translations
python3 scripts/auto/setup_component.py --config setup.json
```

#### Option B: Step-by-Step

```bash
# Step 1: Create project and component
python3 scripts/auto/create_component.py \
    --config component.json \
    --web-config web.json

# Step 2: Add translations
python3 scripts/auto/add_translation.py \
    --web-config web.json \
    --project my-project \
    --component main \
    --language fr,de,es
```

> **Note**: `setup_component.py` automatically loads `web.json`. Individual scripts (`create_component.py`, `add_translation.py`) require explicit `--web-config` or command-line credentials.

---

## 📖 Script 0: `setup_component.py` (All-in-One)

Complete workflow that creates a component and adds translations in one command.

### Features

- ✅ One-command complete setup
- ✅ Creates project and component
- ✅ Adds multiple translations automatically
- ✅ **Sequential translation addition with proper synchronization**
- ✅ Waits for component initialization before adding translations
- ✅ Waits between each translation to ensure stability
- ✅ Verification of component and translation accessibility
- ✅ Interactive mode
- ✅ Progress feedback for each step

### Usage

#### From Setup Config (with languages included)

```bash
python3 scripts/auto/setup_component.py --config setup.json
```

**setup.json format:**
```json
{
  "project": {
    "name": "My Project",
    "slug": "my-project",
    "web": "https://example.com"
  },
  "component": {
    "name": "Main Component",
    "slug": "main",
    "vcs": "git",
    "repo": "git@github.com:user/repo.git",
    "branch": "main",
    "filemask": "locales/*.po",
    "file_format": "po"
  },
  "languages": ["fr", "de", "es", "ja"],
  "wait_for_ready": true,
  "trigger_update": true
}
```

#### From Component Config with Language List

```bash
python3 scripts/auto/setup_component.py \
    --config component.json \
    --languages fr,de,es,ja
```

#### Interactive Mode

```bash
python3 scripts/auto/setup_component.py --interactive
```

### Synchronization & Timing

The script implements **proper synchronization** to ensure reliability:

1. **Component Creation**: Waits for repository cloning and initialization
2. **Stability Check**: 3-second wait after component creation
3. **Component Verification**: Confirms component is accessible
4. **Sequential Translation Addition**: Adds translations one at a time
5. **Inter-Translation Wait**: 2-second pause between each translation
6. **Final Verification**: Confirms all translations are accessible

This prevents race conditions and ensures each step completes before the next begins.

### Output Example

```
============================================================
STEP 1: Creating Component
============================================================

[INFO] Loading web config from: /path/to/web.json
[API] GET http://localhost:8080/api/
[SUCCESS] Connected to Weblate API
[INFO] Creating component: Main Component
[SUCCESS] Component created!

[INFO] Waiting for component to be fully initialized...
[INFO] Ensuring component is ready for translations...
[SUCCESS] Component created and ready!

============================================================
STEP 2: Adding 3 Translation(s)
============================================================

[INFO] Validating inputs...
[SUCCESS] Component 'my-project/main' exists
[SUCCESS] All language codes are valid

[INFO] Adding translations sequentially...

[INFO] [1/3] Adding fr...
[SUCCESS] Translation created: French
[INFO] Waiting 2s before next translation...

[INFO] [2/3] Adding de...
[SUCCESS] Translation created: German
[INFO] Waiting 2s before next translation...

[INFO] [3/3] Adding es...
[SUCCESS] Translation created: Spanish

[SUCCESS] Added 3/3 translation(s)

[INFO] Verifying all translations are accessible...
[SUCCESS] All 3 translation(s) verified

============================================================
SETUP COMPLETE!
============================================================
[INFO] Project: my-project
[INFO] Component: main
[INFO] Translations: 3/3 added
[INFO] URL: http://localhost:8080/projects/my-project/main/
```

---

## 📖 Script 1: `create_component.py`

Creates Weblate projects and components with full VCS integration.

### Features

- ✅ Automatic project and component creation
- ✅ VCS integration (Git, GitHub, GitLab, etc.)
- ✅ Settings verification and correction
- ✅ Repository cloning and translation discovery
- ✅ Interactive mode
- ✅ Configuration file support

### Usage

#### With Web Config File

```bash
python3 scripts/auto/create_component.py \
    --config component.json \
    --web-config web.json
```

#### With Command-Line Credentials

```bash
python3 scripts/auto/create_component.py \
    --config component.json \
    --url http://localhost:8080 \
    --token wlu_YOUR_TOKEN
```

#### Interactive Mode

```bash
python3 scripts/auto/create_component.py --interactive
```

### Configuration Options

#### Project Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Project display name |
| `slug` | Yes | URL-friendly project identifier |
| `web` | Yes | Project website URL |
| `instructions` | No | Instructions for translators |
| `access_control` | No | 0=Public, 1=Protected, 100=Private |

#### Component Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Component display name |
| `slug` | Yes | URL-friendly component identifier |
| `vcs` | Yes | VCS type (git, github, gitlab, etc.) |
| `repo` | Yes | Repository URL (SSH or HTTPS) |
| `branch` | Yes | Repository branch to translate |
| `push` | No | Push URL (for SSH authentication) |
| `push_branch` | No | Branch for pushing changes |
| `filemask` | Yes | File pattern (e.g., `locales/*.po`) |
| `file_format` | Yes | File format (po, json, xliff, etc.) |
| `template` | No | Template file (for monolingual formats) |
| `new_base` | No | Base file for new translations |
| `edit_template` | No | Allow template editing (default: false) |
| `source_language` | No | Source language code (default: en) |
| `license` | No | Translation license |
| `allow_translation_propagation` | No | Propagate translations |
| `enable_suggestions` | No | Enable translation suggestions |
| `suggestion_voting` | No | Enable suggestion voting |
| `suggestion_autoaccept` | No | Auto-accept suggestions threshold |

### Output Example

```
[INFO] Loading web config from: /path/to/web.json
[API] GET http://localhost:8080/api/
[SUCCESS] Connected to Weblate API
[INFO] Creating component: Main Component
[INFO] Repository: git@github.com:user/repo.git
[INFO] Branch: main
[API] POST http://localhost:8080/api/projects/my-project/components/
[SUCCESS] Component created: http://localhost:8080/projects/my-project/main/
[INFO] Verifying component settings match JSON config...
[SUCCESS] Component settings match JSON config
[INFO] Triggering VCS update for my-project/main
[SUCCESS] VCS update triggered
[INFO] Waiting for component to be ready...
[SUCCESS] Component ready with 3 translation(s)

[SUCCESS] Setup complete!
[INFO] Project URL: http://localhost:8080/projects/my-project/
[INFO] Component URL: http://localhost:8080/projects/my-project/main/
```

---

## 📖 Script 2: `add_translation.py`

Adds new language translations to existing Weblate components.

### Features

- ✅ Add single or multiple translations at once
- ✅ **Sequential translation addition with proper synchronization**
- ✅ Waits 2 seconds between each translation
- ✅ Progress counter for multiple translations
- ✅ Final verification of all translations
- ✅ Language code validation
- ✅ Duplicate detection
- ✅ List available languages
- ✅ List component translations
- ✅ Interactive mode

### Usage

#### Add Single Translation

```bash
python3 scripts/auto/add_translation.py \
    --web-config web.json \
    --project my-project \
    --component main \
    --language fr
```

#### Add Multiple Translations

```bash
python3 scripts/auto/add_translation.py \
    --web-config web.json \
    --project my-project \
    --component main \
    --language fr,de,es,ja,zh_Hans
```

#### With Command-Line Credentials

```bash
python3 scripts/auto/add_translation.py \
    --url http://localhost:8080 \
    --token wlu_YOUR_TOKEN \
    --project my-project \
    --component main \
    --language fr
```

#### Interactive Mode

```bash
python3 scripts/auto/add_translation.py --interactive
```

#### List Available Languages

```bash
python3 scripts/auto/add_translation.py --web-config web.json --list-languages
```

#### List Component Translations

```bash
python3 scripts/auto/add_translation.py \
    --web-config web.json \
    --project my-project \
    --component main \
    --list
```

### Common Language Codes

| Code | Language |
|------|----------|
| `ar` | Arabic |
| `de` | German |
| `es` | Spanish |
| `fr` | French |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `pt` | Portuguese |
| `pt_BR` | Portuguese (Brazil) |
| `ru` | Russian |
| `zh_Hans` | Chinese (Simplified) |
| `zh_Hant` | Chinese (Traditional) |

### Synchronization

When adding multiple translations, the script:
1. Adds translations **sequentially** (one at a time)
2. Waits **2 seconds** between each translation
3. Shows **progress counter** `[1/3]`, `[2/3]`, `[3/3]`
4. Continues even if one translation fails
5. Verifies all translations are accessible (for 2+ translations)

This prevents race conditions and ensures stable translation creation.

### Output Example (Multiple Translations)

```
[INFO] Loading web config from: /path/to/web.json
[API] GET http://localhost:8080/api/
[SUCCESS] Connected to Weblate API
[INFO] Validating inputs...
[SUCCESS] Component 'my-project/main' exists
[SUCCESS] All language codes are valid

[INFO] Adding 3 translation(s) sequentially...

[INFO] [1/3] Adding fr...
[API] POST http://localhost:8080/api/components/my-project/main/translations/

[SUCCESS] Translation created: French
  Language code: fr
  URL: http://localhost:8080/projects/my-project/main/fr/
  File: locales/fr.po
  Progress: 0/150 strings translated

[INFO] Waiting 2s before next translation...

[INFO] [2/3] Adding de...
[API] POST http://localhost:8080/api/components/my-project/main/translations/

[SUCCESS] Translation created: German
  Language code: de
  URL: http://localhost:8080/projects/my-project/main/de/
  File: locales/de.po
  Progress: 0/150 strings translated

[INFO] Waiting 2s before next translation...

[INFO] [3/3] Adding es...
[API] POST http://localhost:8080/api/components/my-project/main/translations/

[SUCCESS] Translation created: Spanish
  Language code: es
  URL: http://localhost:8080/projects/my-project/main/es/
  File: locales/es.po
  Progress: 0/150 strings translated

[SUCCESS] Added 3/3 translation(s)

[INFO] Verifying all translations are accessible...
[SUCCESS] All 4 translation(s) verified
```

---

## 🔧 Configuration Files

### Two-File Approach (Recommended)

Separate authentication from project configuration for better security and reusability.

#### `web.json` (Shared)
```json
{
  "weblate_url": "http://localhost:8080",
  "api_token": "wlu_gnEeSZUJv4kDAKvcWWNQNThRlzocIQhYNXWn"
}
```

#### `component.json` (Project-specific)
```json
{
  "project": {
    "name": "My Project",
    "slug": "my-project",
    "web": "https://example.com"
  },
  "component": {
    "name": "Main Component",
    "slug": "main",
    "vcs": "git",
    "repo": "git@github.com:user/repo.git",
    "branch": "main",
    "filemask": "locales/*.po",
    "file_format": "po"
  },
  "wait_for_ready": true,
  "trigger_update": true
}
```

### Single-File Approach

Combine everything in one file (less secure):

```json
{
  "weblate_url": "http://localhost:8080",
  "api_token": "wlu_YOUR_TOKEN",
  "project": { ... },
  "component": { ... }
}
```

### Credential Management

**`setup_component.py`** (all-in-one script):
- Automatically searches for `web.json` in:
  1. Script directory: `scripts/auto/web.json`
  2. Current directory: `./web.json`
- Override with `--web-config /custom/path.json`

**`create_component.py` and `add_translation.py`** (individual scripts):
- Require explicit credentials via:
  - `--web-config web.json`
  - `--url` and `--token` command-line args
  - `WEBLATE_TOKEN` environment variable
- Do NOT auto-load `web.json` (by design)

---

## 📝 Example: AsciiDoc Component

### Configuration (`component.json`)

```json
{
  "project": {
    "name": "Boost Unordered Documentation",
    "slug": "boost-unordered-documentation",
    "web": "https://www.boost.org/doc/libs/master/libs/unordered/",
    "instructions": "Please maintain technical accuracy and AsciiDoc formatting."
  },
  "component": {
    "name": "Intro",
    "slug": "intro",
    "vcs": "github",
    "repo": "git@github.com:user/unordered.git",
    "push": "git@github.com:user/unordered.git",
    "branch": "develop",
    "push_branch": "weblate-intro",
    "filemask": "doc/modules/ROOT/pages/intro_*.adoc",
    "template": "doc/modules/ROOT/pages/intro.adoc",
    "new_base": "doc/modules/ROOT/pages/intro.adoc",
    "file_format": "asciidoc",
    "edit_template": false,
    "source_language": "en",
    "license": "BSL-1.0",
    "allow_translation_propagation": true,
    "enable_suggestions": true
  },
  "wait_for_ready": true,
  "trigger_update": true
}
```

### Create Component

```bash
cd scripts/auto
python3 create_weblate_project.py --config component.json
```

### Add Translations

```bash
# Add multiple languages
python3 add_translation.py \
    --project boost-unordered-documentation \
    --component intro \
    --language ja,zh_Hans,fr,de
```

---

## 🔐 VCS Setup

### For GitHub Push Access

1. **Generate SSH Key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "weblate@example.com"
   ```

2. **Get Weblate's SSH Public Key**:
   - In Weblate, go to Component → Settings → Version Control
   - Copy the SSH public key displayed

3. **Add to GitHub**:
   - Go to your repository → Settings → Deploy keys
   - Click "Add deploy key"
   - Paste Weblate's public key
   - ✅ **Check "Allow write access"** (required for push)

4. **Create Push Branch**:
   ```bash
   git checkout -b weblate-intro
   git push origin weblate-intro
   ```

5. **Configure Component**:
   ```json
   {
     "vcs": "github",
     "repo": "git@github.com:user/repo.git",
     "push": "git@github.com:user/repo.git",
     "branch": "develop",
     "push_branch": "weblate-intro"
   }
   ```

### VCS Types

| VCS | Description | Use Case |
|-----|-------------|----------|
| `git` | Plain Git (no PR integration) | Manual merge workflow |
| `github` | GitHub with PR integration | Automatic pull requests |
| `gitlab` | GitLab with MR integration | Automatic merge requests |
| `gitea` | Gitea with PR integration | Self-hosted Git |

---

## 🛠️ Troubleshooting

### "API token required"

**Solution**: Ensure `web.json` exists in the script directory or use `--token`:
```bash
python3 add_translation.py --token wlu_YOUR_TOKEN --project ... --component ... --language ...
```

### "Component not found"

**Solution**: Verify project and component slugs:
```bash
# List projects (via API)
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8080/api/projects/
```

### "Invalid language code"

**Solution**: List available languages:
```bash
python3 add_translation.py --list-languages
```

### "Host key verification failed"

**Solution**: Add GitHub to known hosts:
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

Or in Weblate container:
```bash
docker exec weblate ssh-keyscan github.com >> /home/weblate/.ssh/known_hosts
```

### "Permission denied (publickey)"

**Solution**: Ensure Weblate's SSH key is added to GitHub with write access.

### "Timeout waiting for component"

This is **normal** for first-time repository cloning. The component was created successfully, and Weblate continues processing in the background.

---

## 📚 Advanced Usage

### Environment Variables

```bash
export WEBLATE_TOKEN="wlu_YOUR_TOKEN"
python3 add_translation.py --project my-project --component main --language fr
```

### Batch Processing

```bash
# Create multiple components
for config in components/*.json; do
    python3 create_weblate_project.py --config "$config"
done

# Add same languages to multiple components
for comp in main docs api; do
    python3 add_translation.py \
        --project my-project \
        --component "$comp" \
        --language fr,de,es
done
```

### CI/CD Integration

```yaml
# .github/workflows/weblate-setup.yml
name: Setup Weblate Component

on:
  push:
    branches: [main]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Create web.json
        run: |
          echo '{
            "weblate_url": "${{ secrets.WEBLATE_URL }}",
            "api_token": "${{ secrets.WEBLATE_TOKEN }}"
          }' > scripts/auto/web.json
      
      - name: Create Weblate component
        run: |
          python3 scripts/auto/create_weblate_project.py \
            --config scripts/auto/component.json
```

---

## 🔍 API Reference

### Create Project
```
POST /api/projects/
```

### Create Component
```
POST /api/projects/{project}/components/
```

### Add Translation
```
POST /api/components/{project}/{component}/translations/
```

### List Translations
```
GET /api/components/{project}/{component}/translations/
```

### Trigger VCS Update
```
POST /api/components/{project}/{component}/repository/
```

Full API documentation: https://docs.weblate.org/en/latest/api.html

---

## 📄 License

GPL-3.0-or-later

## 👥 Authors

Weblate Team

## 🤝 Contributing

Contributions welcome! Please ensure:
- Code passes linting
- Line length ≤ 88 characters (PEP 8)
- Type hints included
- Documentation updated

---

## 📞 Support

- Documentation: https://docs.weblate.org/
- Issues: https://github.com/WeblateOrg/weblate/issues
- Forum: https://discussions.weblate.org/

