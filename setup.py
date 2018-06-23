from setuptools import setup, find_packages


def get_version():
    try:
        return open('version.txt').read().strip()
    except IOError:
        return ''


setup(
    name='h',
    version=get_version() or '0.0-dev',
    packages=find_packages(exclude=('tests', 'tests.*')),
    py_modules=['h'],
    include_package_data=True,
    setup_requires=[
        'setuptools_git==1.0',  # anything tracked in git gets packaged
        'wheel==0.29.0',
    ],
    entry_points={
        'console_scripts': [
            'h=h.main:cli'
        ]
    }
)
