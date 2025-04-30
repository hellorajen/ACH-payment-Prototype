# Create project directory
mkdir ach_prototype
cd ach_prototype

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django django-crispy-forms crispy-bootstrap5 python-dotenv requests