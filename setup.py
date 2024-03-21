from setuptools import setup, find_packages

setup(
    name='nonebot_plugin_duel',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'nonebot-adapter-onebot>=2.0.0',
        'nonebot2>=2.0.0'
    ],
    author='Redmomn',
    author_email='109732988+Redmomn@users.noreply.github.com',
    description='nonebot-plugin-duel',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=['nonebot2', 'duel'],
    url='https://github.com/Redmomn/nonebot-plugin-duel'
)
