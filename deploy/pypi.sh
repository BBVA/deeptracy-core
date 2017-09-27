# Upload to PyPI
python setup.py check --restructuredtext
python setup.py sdist bdist_wheel
pip install twine && (twine upload -u $PYPI_USER -p $PYPI_PASSWD dist/* || /bin/true)
