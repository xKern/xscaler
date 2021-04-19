from distutils.core import setup
setup(
      name='xscaler',         # How you named your package folder (MyLib)
      packages=['xscaler'],   # Chose the same as "name"
      version='0.1',
      license='MIT',
      description=('A simple python utility based on ffmpeg '
                   'and opencv for in house use'),
      author='Haider Ali',                   # Type in your name
      author_email='me@haiderali.dev',      # Type in your E-Mail
      url='https://github.com/xKern/xscale',
      download_url='https://github.com/xKern/xscaler/archive/refs/tags/0.1.tar.gz',
      keywords=['XKERN', 'XSCALER', 'PYTHON', 'FFMPEG', 'OPENCV'],
      # I explain this later on
      install_requires=['ffmpeg-python', 'opencv-python', 'logzero'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
        ],
)
