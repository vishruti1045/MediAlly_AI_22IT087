from werkzeug.security import generate_password_hash

password = "your_password_here"  # Replace with the actual password
new_hash = generate_password_hash(password)

print("Generated Hash:", new_hash)
