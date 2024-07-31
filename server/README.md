# Install dependencies
conda create -n final python=3.8
conda activate final
pip install -r requirements.txt

# Add env file
1. Create .env file
2. Add a line `DEBUG = True` to run swagger

# Run the app
python app.py

# Access swagger
http://127.0.0.1:5000
