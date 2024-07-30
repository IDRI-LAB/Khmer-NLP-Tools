from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

def requirement():
    return [
        'tqdm==4.61.0',
        'sklearn-crfsuite==0.3.6',
        'scikit-learn==0.23.2',
        'pydub==0.25.1'
    ]

setup(
    name='khnlp',
    version='0.0.1',
    description='Khmer NLP Toolkit',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='LEANG Sotheara',
    author_email='leangsotheara@gmail.com',
    url='https://github.com/NiptictLab/khnlp',
    keywords=['', '', ''],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirement(),
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
