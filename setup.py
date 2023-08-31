import subprocess

subprocess.run(["pip", "install", "-r", "requirements.txt"])
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
