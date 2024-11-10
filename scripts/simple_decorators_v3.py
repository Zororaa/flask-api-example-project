import functools

user = {"username": "jose", "access_level": "admin"}

def make_secure(func):
    @functools.wraps(func) # This library helps with referencing the origianl function inside the decorator which is called get_admin_password
    def secure_function():
        if user["access_level"] == "admin":
            return func()
        else:
            return f"user does not have admin permissions {user["username"]}"
    
    return secure_function


@make_secure
def get_admin_password():
    return "1234"

print(get_admin_password.__name__) # Identifies which is the function being called after the decorator call
        


