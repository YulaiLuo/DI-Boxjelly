# Comment the following two lines if you already have a environments called di
conda create --name di --file requirements.txt
conda activate di

# run the gateway service
python src/di-gateway/app.py

# run the auth service
python src/di-auth/app.py

