## Synopsis

HTMLTestRunner.py is a module extension above unittest in Python.  With it, you
can quickly generate an HTML test report.  HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

## Code Example

### The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()


### For more customization options, instantiates a HTMLTestRunner object.


    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)


## Motivation

HTMLTestRunner was an easy to use library as a developer to quickly see a webpage
based report.  It was originally created by tungwaiyip and upgraded recently for Python 3
by dash0002.  In it's current iteration and maintenance, our goals are still the same;
to be able to quickly generate an HTML test report.

## Installation
Supporting Python 3 - 3.5

### PIP (recommended)

### Copy and paste
You can take a copy of the HTMLTestRunner.py and include it directly in your Project
as-is.

## Tests

    python test_HTMLTestRunner.py

## Contributors

Way Yip Tung - https://github.com/tungwaiyip
Asish Dash - https://github.com/dash0002
Dhruv Paranjape - https://github.com/dark-passenger
Ethan Estrada - https://github.com/eestrada

Contributions are gladly accepted as this is a side project at best.  Please, also
consider this when looking at feedback cycles, issues, pull requests, etc.

## License

HTMLTestRunner is licensed under http://choosealicense.com/licenses/bsd-3-clause/
