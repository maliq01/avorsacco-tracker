import pickle
from pathlib import Path


import streamlit_authenticator as stauth


names = ["katana", "joy"]
user_name = ["ktn", "joy"]
passwords =["12345", "67890"]


hashed_passwords =stauth.Harsher(passwords).generate()

file_path =Path(__file__).partent/"hashed_pw.pk1"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
