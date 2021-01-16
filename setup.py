from setuptools import setup, find_packages


def main():
    console_scripts = [
        "start_service=elms.bin.start_server:main"
    ]
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    setup(
        name='eLMS',
        version='1.0',
        author='Philipp Fisin',
        packages=find_packages("src"),
        package_dir={'': 'src'},
        description='Backed for Learning Management System with HTTP API',
        install_requires=required,
        entry_points={
            'console_scripts': console_scripts,
        }
    )


if __name__ == "__main__":
    main()
