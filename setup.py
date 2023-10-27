from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = "_e ."
def get_requirements(file_path:str) -> List[str]:
    """
    this fn returns the list of requirements
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements= file_obj.readline()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

setup(
    name='student performance indicator',
version='0.0.1',
author='Sanket',
author_email='sanketgore1998@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')  #['pandas','numpy','seaborn']

)


