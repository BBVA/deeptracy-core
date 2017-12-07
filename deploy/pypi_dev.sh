# Upload to PyPI
python setup_dev.py check --restructuredtext
python setup_dev.py sdist bdist_wheel
pip install twine && (twine upload -u $PYPI_USER -p $PYPI_PASSWD dist/* || /bin/true)
