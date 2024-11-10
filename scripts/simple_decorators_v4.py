import functools
####Passing Parameters into @decorator functions
#This will need to make the function avaialble for any amount of argumanets
user = {"username": "jose", "access_level": "admin"}

def make_secure(func):
    @functools.wraps(func) # This library helps with referencing the origianl function inside the decorator which is called get_admin_password
    def secure_function(*args, **kwargs):
        if user["access_level"] == "admin":
            return func(*args, **kwargs)
        else:
            return f"user does not have admin permissions {user["username"]}"
    
    return secure_function


@make_secure
def get_password(panel):
    if panel == "admin":
        return "1234"
    elif panel == "billing":
        return "super_secure_password"

print(get_password("billing")) # Identifies which is the function being called after the decorator call
        


