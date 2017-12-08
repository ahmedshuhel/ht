from pip.download import PipSession
from pip.index import PackageFinder
from pip.req import parse_requirements
from setuptools import setup, find_packages

pip_session = PipSession()
finder = PackageFinder(find_links=[], index_urls=[], session=pip_session)
requirements = list(parse_requirements(
    'requirements.txt',
    finder,
    session=pip_session)
)
install_requires = [str(r.req) for r in requirements]


def get_version():
    try:
        return open('version.txt').read().strip()
    except IOError:
        return ''


setup(
    name='ht',
    version=get_version() or '0.0-dev',
    packages=find_packages(exclude=('tests', 'tests.*')),
    py_modules=['ht'],
    install_requires=install_requires,
    entry_points='''
        [console_script]
        t=ht.main:cli
    '''
)
