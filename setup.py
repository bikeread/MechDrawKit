#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MechDrawKit - 机械工程图纸生成工具包
安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), '重构完成总结.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "机械工程图纸生成工具包 - 基于策略模式的模块化架构"

# 读取requirements.txt
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    requirements.append(line)
    return requirements

setup(
    name="mechdrawkit",
    version="1.0.0",
    author="bikeread",
    author_email="bikeread2008@gmail.com",
    description="机械工程图纸生成辅助工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/bikeread/mechdrawkit",
    project_urls={
        "Bug Reports": "https://github.com/bikeread/mechdrawkit/issues",
        "Source": "https://github.com/bikeread/mechdrawkit",
        "Documentation": "https://bikeread.github.io/mechdrawkit/",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Computer Aided Design (CAD)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipython>=8.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "mechdrawkit": [
            "config/*.json",
            "config/*.py",
        ],
    },
    entry_points={
        "console_scripts": [
            "mechdrawkit=mechdrawkit.__main__:main",
        ],
    },
    zip_safe=False,
    keywords="mechanical drawing CAD DXF GB standards engineering",
) 