# importing libraries
from setuptools import find_packages, setup
from typing import List

requirement_file_name = "requirements.txt"

REMOVE_PACKAGE = "-e ."


# defining method to get the requirements.txt file
def get_requirements() -> List[str]:
    """
    Task: returns the required packages
    from requirements.txt in string format
    """
    # opening the requirement.txt file
    with open(requirement_file_name) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [
        requirement_name.replace("\n", "") for requirement_name in requirement_list
    ]

    # removing unnecessary items from requirements.txt file
    if REMOVE_PACKAGE in requirement_list:
        requirement_list.remove(REMOVE_PACKAGE)
    return requirement_list


# setting up the setup file details
setup(
    name="Insurance",
    version="0.0.1",
    description="Insurance Industry level Project",
    author="Nilutpal Das",
    author_email="nilutpaldas992@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)

# timstamp 27 min
