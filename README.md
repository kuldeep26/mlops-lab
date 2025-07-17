MLOps Lab – CI & Local Development Guide
This repository enforces CI checks for YAML formatting, Python linting, PR title validation, and Jupyter notebook output stripping.
Follow this guide to fix issues locally before committing or pushing code.

✅ CI Checks Overview
The CI pipeline validates the following:

PR Title → Must follow naming conventions:

For workflow/root changes: mlops-lab-admin:<message>

For pipeline changes: <pipeline-name>:<message>

YAML Formatting → Ensures correct structure in .github/workflows/

Python Linting → Enforces PEP8 standards

Notebook Output → All Jupyter notebook outputs must be cleared

Whitespace Check → No trailing whitespaces in files

Unit Tests → Runs pytest for changed pipeline code

🛠 Local Fix Instructions
1. YAML Checks & Auto-Fix
✅ Option 1: Using Prettier (Recommended if Node.js is available)
# Install Prettier
sudo apt install npm
sudo npm install --global prettier

# Auto-format all workflow YAML files
prettier --write ".github/workflows/*.yml"

✅ Option 2: Using yamllint + ruamel.yaml (Python-based)
Install linters & formatter:
pip install yamllint ruamel.yaml

Validate YAML files:
yamllint .github/workflows/

Auto-fix YAML formatting:
python -c "from ruamel.yaml import YAML; import sys; yaml=YAML(); yaml.preserve_quotes=True; [yaml.dump(yaml.load(open(f)), open(f,'w')) for f in sys.argv[1:]]" .github/workflows/*.yml

✅ Fixes:

Indentation

Preserves quotes

Proper YAML structure

Validate again:
yamllint .github/workflows/

2. Python Linting & Auto-Fix
Use a virtual environment to avoid breaking system Python.

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install autopep8
pip install autopep8

# Auto-fix Python code in pipelines
autopep8 --in-place --recursive pipeline/

3. Notebook Output Stripping
Ensure Jupyter notebooks do not contain output cells before committing.
# Activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install nbstripout
pip install nbstripout

# Strip outputs from all notebooks
nbstripout pipeline/**/*.ipynb

✅ One-Liner Commands
# Install everything
pip install yamllint ruamel.yaml autopep8 nbstripout

# Run all checks/fixes
yamllint .github/workflows/
python -c "from ruamel.yaml import YAML; import sys; yaml=YAML(); yaml.preserve_quotes=True; [yaml.dump(yaml.load(open(f)), open(f,'w')) for f in sys.argv[1:]]" .github/workflows/*.yml
autopep8 --in-place --recursive pipeline/
nbstripout pipeline/**/*.ipynb

🔍 Common Issues & Fix
Issue	Fix Command
YAML lint errors	prettier --write ".github/workflows/*.yml" OR ruamel script
Python lint errors	autopep8 --in-place --recursive pipeline/
Notebook outputs found in CI	nbstripout pipeline/**/*.ipynb
Trailing whitespace detected	Remove extra spaces and commit again

✅ Developer Tips
Always run these checks locally before pushing code.

Use feature branches that follow your team's naming convention.

Ensure unit tests pass locally using:
pytest pipeline/<pipeline_name>/tests/

✅ fix_yaml.sh
```sh
#!/bin/bash
set -e

echo "🔍 Fixing YAML files in .github/workflows/ ..."

# Step 1: Install ruamel.yaml if not installed
if ! python3 -c "import ruamel.yaml" &>/dev/null; then
    echo "📦 Installing ruamel.yaml..."
    pip install ruamel.yaml
fi

# Step 2: Fix indentation & structure using ruamel.yaml
echo "✅ Fixing indentation and structure..."
python3 - <<'EOF'
from ruamel.yaml import YAML
import glob

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

for file in glob.glob(".github/workflows/*.yml"):
    with open(file) as f:
        data = yaml.load(f)
    with open(file, 'w') as f:
        yaml.dump(data, f)
    print(f"✔ Reformatted {file}")
EOF

# Step 3: Remove trailing whitespace
echo "✅ Removing trailing spaces..."
find .github/workflows -type f -name "*.yml" -exec sed -i 's/[ \t]*$//' {} +

# Step 4: Add a newline at EOF ONLY if missing
echo "✅ Ensuring a single newline at EOF..."
for file in .github/workflows/*.yml; do
    if [ -f "$file" ]; then
        if [ -n "$(tail -c 1 "$file")" ]; then
            echo "" >> "$file"
            echo "✔ Added newline at EOF for $file"
        fi
    fi
done

echo "🎯 All YAML files fixed successfully!"
```
✅ How to Run
```sh
chmod +x fix_yaml.sh
./fix_yaml.sh
```

✅ What this script does:
✔ Fixes indentation & formatting using ruamel.yaml
✔ Removes trailing spaces
✔ Adds newline at EOF
✔ Works for all .yml files in .github/workflows/
