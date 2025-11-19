from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrape-kit',
    version='1.0.0',
    author='Priyanshu Maity',
    author_email='priyanshu.maity2006@gmail.com',
    description='A toolkit comprising multiple tools to help with web scraping.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cup-of-logic/encoding',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['beautifulsoup4', 'tzlocal'],
    include_package_data=True,
)
