try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup


setup(
    name='Islykill2',
    version='1.0.1',
    description='Utility to parse and verify Islykill authentication, '
                'using SAML 2.0',
    author='Sindri Gudmundsson',
    author_email='sindrigudmundsson@gmail.com',
    url='https://github.com/sindrig/islykill2/',
    packages=['islykill2'],
    include_package_data=True,
    zip_safe=False,
    licence='MIT',
    install_requires=['signxml']
)
