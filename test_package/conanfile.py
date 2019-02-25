#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        mpiexec = os.path.join(os.environ['MPI_BIN'], 'mpiexec')
        with open('hostfile', 'w') as f:
            f.write('localhost slots=2\n')
        command = '%s --oversubscribe -np 2 --hostfile hostfile %s' % (mpiexec, os.path.join("bin", "test_package"))
        with tools.environment_append({'TMPDIR': '/tmp'}):
            self.run(command, run_environment=True)
