# Install dependencies
conda create -n final python=3.8
conda activate final
pip install -r requirements.txt

# Run the app
conda activate final
python app.py
