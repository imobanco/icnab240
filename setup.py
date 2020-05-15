from setuptools import setup

# versioning
import versioneer


with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="icnab240",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Imobanco",
    description="Gerador e leitor de CNAB 240",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imobanco/icnab240",
    packages=["icnab240", "icnab240.controllers", "icnab240.data", "icnab240.pipe_and_filter"],
    package_data=('icnab240', ['data/*']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["pycpfcnpj>=1.5", "pydantic>=1.4"],
    keywords="Zoop API client wrapper",
    project_urls={
        "Documentation": "https://icnab240.readthedocs.io",
        "Source": "https://github.com/imobanco/icnab240",
        "Tracker": "https://github.com/imobanco/icnab240/issues",
    },
)
