def authenticate(username, password):
    if username == "admin" and password == "secret":
        return True
    else:
        raise ValueError("Invalid credentials")  # error source
