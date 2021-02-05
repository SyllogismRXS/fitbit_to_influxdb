from setuptools import setup

setup(name='fitbit_to_influxdb',
      version='0.1',
      description='Pulls down your personal fitbit data and writes it to influxdb',
      url='http://www.kevindemarco.com',
      author='Kevin DeMarco',
      author_email='kevin@kevindemarco.com',
      license='BSD',
      packages=['fitbit_to_influxdb'],
      install_requires=[
          'fitbit',
          'pandas',
          'influxdb',
          'cherrypy',
          'argparse',
          'pyyaml'
      ],
      entry_points = {
          'console_scripts': ['fitbit_to_influxdb_server=fitbit_to_influxdb.command_line.server:main',
                              'download_fitbit_data=fitbit_to_influxdb.command_line.download_fitbit_data_cli:main',
                              'authorize_oath2=fitbit_to_influxdb.command_line.authorize_oath2:main',
                              'write_to_influxdb=fitbit_to_influxdb.command_line.write_to_influxdb_cli:main'],
      },
      zip_safe=False)
