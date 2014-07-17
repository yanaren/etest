#!/bin/sh
pkg_install='python2.7 setup.py install'
export PYTHONPATH=`pwd`
cd src/lib

InstallPython()
{
    echo "Installing python2.7"
    tar -zxvf Python-2.7.tgz
    cd Python-2.7 && sh ./configure && make
    sudo make install && cd $cwd
    sudo rm -rf Python-2.7
    cd ..
}

pyv=`which python 2>&1| awk -F: '{print $1}' | awk -F'/' '{print $NF}'`
if [ "$pyv" = "python" ]
then
    python --version 2> tmp
    pyv=`cat tmp`
    if [ "$pyv" = "Python 2.7" ]
    then
        echo "python2.7 have been installed"
    else
        InstallPython
    fi
    rm -rf tmp
else
    echo 'InstallPython'
    InstallPython
fi

InstallSetupTool()
{
    tar -zvxf setuptools-2.0.1.tar.gz
    cd setuptools-2.0.1
    sudo python setup.py install
    cd ..
}

InstallPip()
{
    tar -zvxf pip-1.3.1.tar.gz 
    cd pip-1.3.1 
    sudo python setup.py
    sudo python setup.py install
}

InstallPytest()
{
    tar -zvxf pytest-2.5.1.tar.gz
    cd pytest-2.5.1
    sudo python setup.py install
    cd ..
}
InstallPytestConfig()
{
    tar -zvxf pytest-configloader-0.1.tar.gz
    cd pytest-configloader-0.1 
    sudo python setup.py install
    cd ..
}


pytv=`which py.test 2>&1| awk -F: '{print $1}' | awk -F'/' '{print $NF}'`
if [ "$pytv" = "py.test" ]
then
        echo "py.test have been installed"
else
    echo 'install'
    InstallSetupTool
    InstallPip
    InstallPytest
    InstallPytestConfig
fi



