try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup


setup(
    name='Islykill2',
    version='1.0.1.rc0',
    description='Utility to parse and verify Islykill authentication, '
                'using SAML 2.0',
    author='Sindri Gudmundsson',
    author_email='sindrigudmundsson@gmail.com',
    url='http://www.irdn.is/',
    packages=['islykill2'],
    include_package_data=True,
    zip_safe=False,
    licence='MIT',
    install_requires=['signxml']
)
