from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.1',
    author='Vishaka Gangurde',
    author_email='vishakag25@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)