import os
from os import environ

def env_exists(name):
    return name in environ

def get_env(name):
    return environ.get(name)
