pip install -U pip
pip install pipenv

# Clone and prepare repo
git clone https://github.com/TommyBark/LitigAItor-mini
cd LitigAItor-mini
mkdir documents

# Install dependencies
pipenv install
pip install -e .
python ./litigator_mini/interface.py
