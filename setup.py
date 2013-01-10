from setuptools import setup, find_packages

setup(
    name='django-captchapy',
    version='1.0',
    description='Captcha para django simples.',
    author='Rafael Feijo da Rosa',
    author_email='rafael@desenvolvendoweb.com.br',
    url='http://www.desenvolvendoweb.com.br/',
    packages=['captchapy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    # Tells setuptools to download setuptools_git before running setup.py so
    # it can find the data files under Git version control.
    zip_safe=False,
)
