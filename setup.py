from setuptools import setup, find_namespace_packages

setup(
    name='clean-folder',
    version='1.0.0',
    description='Script to sort files in a folder by extension',
    url='https://github.com/AskarovVlad/clean-folder',
    author='Vladislav Askarov',
    author_email='vladislav.oskarov30@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder= clean-folder.clean:main']}
)
