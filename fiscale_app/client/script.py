import os
# fonction pour vérifier les null bytes dans les fichiers
def check_null_bytes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        if b'\x00' in content:
                            print(f"Null bytes trouvés dans: {filepath}")
                except Exception as e:
                    print(f"Erreur lecture {filepath}: {e}")

check_null_bytes('.')