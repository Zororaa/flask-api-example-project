"""
BlockList

Contains blocklist of JWT Tokens 
Imported by the app and the logout resource so its not used again.
Ideally this can be used in a database or Redis application
"""

BLOCKLIST = set()