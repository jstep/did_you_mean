import os

def clear() -> None:
    """Calls the system's clear screen function"""
    _ = os.system('clear' if os.name =='posix' else 'cls')
