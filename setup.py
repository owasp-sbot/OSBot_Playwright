from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version                       = "v0.3.2"               , # change this on every release
    name                          = "osbot_playwright"  ,
    author                        = "Dinis Cruz",
    author_email                  = "dinis.cruz@owasp.org",
    description                   = "OWASP Security Bot - Playwright",
    long_description              = long_description,
    long_description_content_type = " text/markdown",
    url                           = "https://github.com/owasp-sbot/OSBot-Playwright",
    packages                      = find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])
