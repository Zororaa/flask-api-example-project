def get_admin_password():
    return "1234"

def make_secure(func):
    def secure_function():
        if user["access_level"] == "admin":
            return func()
        else:
            return f"user does not have admin permissions {user["username"]}"
    
    return secure_function


get_admin_password = make_secure(get_admin_password)
user = {"username": "jose", "access_level": "guest"}
print(get_admin_password())
        


