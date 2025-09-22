from flask_bcrypt import generate_password_hash
hash_contrasena = generate_password_hash('usuario123').decode('utf-8')
print(hash_contrasena)