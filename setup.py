import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Detail see: https://packaging.python.org/tutorials/packaging-projects/#creating-setup-pypip install -i https://test.pypi.org/simple/ pysetup
setuptools.setup(
    name="ResistorDecoder",
    version="1.0",
    author="Voxel",
    author_email="voxel.aur@gmail.com",
    description="Qt GUI tool for through-hole resistors and SMD parts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU Public License version 3 or later",
    url="https://github.com/VoxelCubes/Resistor-Color-and-SMD-Decoder",
    python_requires='>=3.6',
    packages=setuptools.find_packages(exclude=["release"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyside6"],
    entry_points={
        "gui_scripts": ["resistor_decoder = ResistorDecoder.src.main:main"],
    },
)
