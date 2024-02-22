from setuptools import find_packages, setup
from typing import List


with open("README.md", "r") as f:
    long_description = f.read()


def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file=file_path, mode='r') as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace('\n', '') for req in requirements]
            if "-e ." in requirements:
                  requirements.remove("-e .")
    return requirements


setup(
    name="hotel room reservation API",
    version="0.0.1",
    description="A website to reserve hotel room",
    packages=find_packages(),
    author="Nouri Muhammad",
    author_email="nouri.muhammad1991@gmail.com",
    install_requires=get_requirements('requirements.txt')
)

