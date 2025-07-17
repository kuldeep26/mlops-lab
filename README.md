# mlops-lab #
#YAML checks fix locally
sudo apt install npm
sudo npm install --global prettier
prettier --write ".github/workflows/*.yml"

# Python linting fix locally Use a Virtual Environment (Recommended)
# Create a virtual environment so your changes don’t affect the system Python:
python3 -m venv venv
source venv/bin/activate
pip install autopep8
# Then run:
autopep8 --in-place --recursive pipeline/inventory/

## Fix notebook output CI check
python3 -m venv venv
source venv/bin/activate
pip install nbstripout
nbstripout pipeline/**/*.ipynb