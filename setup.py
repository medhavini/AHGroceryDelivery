# setup.py

from setuptools import setup
setup(
    name='AHDelivery'
    packages = ['stores', 'notification'],
    entry_points={
        'console_scripts' : [
            'finddeliveryslot = stores.ah.main',
        ]
    },
    install_requires=[
        'argsparse','datetime', 'logging', 'twilio', 'selenium'
    ]
)