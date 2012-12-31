from setuptools import setup, find_packages
import os
import auction

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    author="Joe Curlee",
    author_email="joe.curlee@gmail.com",
    name='django-auction',
    version=auction.__version__,
    description='Based on django-shop, Django Auction aims to allow easy development of auction apps.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='http://joecurlee.com/django-auction/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.3',
        'South==0.7.6',
        'django-polymorphic==0.2',
        'wsgiref==0.1.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,
)
