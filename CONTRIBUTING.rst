.. highlight: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/lufvelasquezgo/llg/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

`llg` could always use more documentation, whether as part of the
official `llg` docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/lufvelasquezgo/llg/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `llg` for local development.

1. Fork the `llg` repo on GitHub.
2. Clone your fork locally:

    $ git clone git@github.com:your_name_here/llg.git

3. We use [Poetry](https://python-poetry.org/) to manage dependencies. Install it (we recommend to use [pipx](https://github.com/pypa/pipx)) and install the dependencies:

    $ poetry install

4. Install pre-commit hooks:

    $ poetry run pre-commit install

4. Create a branch for local development from `develop`:

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass pre-commit hooks and tests. You can only run the tests into the python you are using, using pytest:

    $ pytest

   But we highly recommend to run the tests in all supported Python versions. You can use tox for that:

    $ poetry run tox

6. Commit your changes and push your branch to GitHub:

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
3. The pull request should work for Python >= 3.9. Check
   [https://github.com/lufvelasquezgo/llg/actions](https://github.com/lufvelasquezgo/llg/actions)
   and make sure that the tests pass for all supported Python versions.


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:

$ poetry version VERSION # possible: patch, minor, major

Create a release branch from `develop`:

    $ git checkout develop
    $ git pull
    $ git checkout -b release/VERSION
    $ git push
    $ git push --tags

Once merged, the GitHub Actions will deploy the package to test-PyPI.
Check that everything is working as expected, and then create a pull request to merge the release branch into main.

Finally, create a new release on GitHub with the version number and the changes made.
