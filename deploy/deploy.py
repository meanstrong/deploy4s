#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import urllib2
import subprocess
import zipfile
import logging

import yaml

class Deploy(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)

        self._bundle = None
        self._bundle_dir = os.path.join(os.path.expanduser('~'), ".deploy")
        if not os.path.isdir(self._bundle_dir):
            os.makedirs(self._bundle_dir)
        self._workdir = "."

    def deploy(self, bundle):
        self.logger.info("DownloadBundle...")
        self.download_bundle(bundle)
        try:
            with zipfile.ZipFile(self._bundle, "r") as zf:
                appspec = yaml.load(zf.read("appspec.yml"))
        except:
            raise Exception("Not found file appspec.yml in bundle.")

        workdir = appspec.get("workdir")
        if workdir is not None:
            self._workdir = workdir
        if not os.path.isdir(self._workdir):
            os.makedirs(self._workdir)

        self.logger.info("RUN ApplicationStop...")
        self._exec_hooks(appspec.get("hooks").get("ApplicationStop"))

        self.logger.info("RUN BeforeInstall...")
        self._exec_hooks(appspec.get("hooks").get("BeforeInstall"))

        self.logger.info("RUN Install...")
        self.install(appspec.get("files"))

        self.logger.info("RUN AfterInstall...")
        self._exec_hooks(appspec.get("hooks").get("AfterInstall"))

        self.logger.info("RUN ApplicationStart...")
        self._exec_hooks(appspec.get("hooks").get("ApplicationStart"))

        self.logger.info("RUN ValidateService...")
        self._exec_hooks(appspec.get("hooks").get("ValidateService"))

        self.logger.info("Deploy OK.")

    def _exec_hooks(self, hooks):
        if hooks is None:
            return
        try:
            for hook in hooks:
                self._run_cmd(hook["location"])
        except Exception as err:
            raise Exception("run cmd error: " + repr(err))

    def _run_cmd(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=self._workdir)
        while p.poll() is None:
            line = p.stdout.readline()
            self.logger.info(line.strip())
        rc = p.returncode
        if rc != 0:
            self.logger.warn("rc: " + str(rc))
            self.logger.warn("stderr: " + p.stderr.read())
            raise Exception("run cmd error.")
        return rc

    def download_bundle(self, bundle):
        if bundle.startswith("http://"):
            f = urllib2.urlopen(bundle) 
            self._bundle = os.path.join(self._bundle_dir, os.path.basename(bundle))
            with open(self._bundle, "wb") as zf:     
                zf.write(f.read())
        else:
            self._bundle = bundle

    def install(self, files):
        if files is None:
            return
        zf = zipfile.ZipFile(self._bundle, "r")
        for entry in files:
            source = entry["source"]
            destination = entry["destination"]
            if source == "/":
                zf.extractall(self._workdir)
            else:
                zf.extract(source, self._workdir)
                if os.path.isdir(os.path.join(self._workdir, source)):
                    for f in zf.namelist():
                        if f.startswith(source):
                            zf.extract(f, self._workdir)
        zf.close()
