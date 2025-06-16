from setuptools import setup, find_packages
from typing import List

def requirements() -> List[str]:
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            r = [req.strip() for req in lines if req.strip() != '-e .']
            return r
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        return []

# print(requirements())


setup(
    name='NetworkSecurity',
    version="0.0.1",
    author="Kanishka Rani",
    author_email="kanishka22043@gmail.com",
    packages=find_packages(),
    install_requires=requirements(),
)
