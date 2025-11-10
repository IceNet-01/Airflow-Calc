"""
Setup configuration for Cybertruck Airflow Calculator
"""

from setuptools import setup, find_packages
import os

# Read version from __init__.py
def get_version():
    init_path = os.path.join('src', 'airflow_calc', '__init__.py')
    with open(init_path, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return '1.0.0'

# Read long description from README
def get_long_description():
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='airflow-calc',
    version=get_version(),
    description='Cybertruck Airflow Calculator - Comprehensive aerodynamic analysis tool',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Airflow-Calc Team',
    author_email='',
    url='https://github.com/IceNet-01/Airflow-Calc',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.3.0',
    ],
    entry_points={
        'console_scripts': [
            'airflow-calc=airflow_calc.cli:main',
            'airflow-calc-gui=airflow_calc.gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='aerodynamics airflow cybertruck tesla cfd fluid-dynamics',
    project_urls={
        'Bug Reports': 'https://github.com/IceNet-01/Airflow-Calc/issues',
        'Source': 'https://github.com/IceNet-01/Airflow-Calc',
    },
)
