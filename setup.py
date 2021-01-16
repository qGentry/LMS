from setuptools import setup, find_packages


def main():
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    setup(
        name='elms',
        version='1.0',
        author='Philipp Fisin',
        packages=find_packages("src"),
        package_dir={'': 'src'},
        description='Backed for Learning Management System with HTTP API',
        install_requires=required,
    )


if __name__ == "__main__":
    main()
