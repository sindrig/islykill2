try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup


setup(
    name='Islykill2',
    version='0.9rc2',
    description='Utility to parse and verify Islykill authentication, '
                'using SAML 2.0',
    author='Sindri Gudmundsson',
    author_email='sindrigudmundsson@gmail.com',
    url='http://www.irdn.is/',
    package_dir={'islykill2': 'src'},
    packages=['islykill2'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['signxml']
)
