#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import time
import shutil
import urllib2
import subprocess
import zipfile

import yaml

class Deploy(object):
    def __init__(self):
        self._bundle = None
        self._bundle_dir = os.path.join(os.path.expanduser('~'),
                                        ".deploy")
        self._extract_dir = os.path.join(self._bundle_dir, str(time.time()))
        if not os.path.isdir(self._extract_dir):
            os.makedirs(self._extract_dir)
        self._workdir = None

    def deploy(self, bundle):
        self.download_bundle(bundle)
        try:
            with zipfile.ZipFile(self._bundle, "r") as zf:
                appspec = yaml.load(zf.read("appspec.yml"))
        except:
            raise Exception("Not found file appspec.yml in bundle.")

            
        self._workdir = appspec.get("workdir") or ""

        self._exec_hooks("ApplicationStop", appspec.get("hooks").get("ApplicationStop"))
        self._exec_hooks("BeforeInstall", appspec.get("hooks").get("BeforeInstall"))
        self.install(appspec.get("files"))
        self._exec_hooks("AfterInstall", appspec.get("hooks").get("AfterInstall"))
        self._exec_hooks("ApplicationStart", appspec.get("hooks").get("ApplicationStart"))
        self._exec_hooks("ValidateService", appspec.get("hooks").get("ValidateService"))

    def _exec_hooks(self, name, hooks):
        if hooks is None:
            return
        try:
            for hook in hooks:
                self._run_cmd(hook["location"])
        except Exception as err:
            raise Exception("run " + name + " hooks error: " + repr(err))

    def _run_cmd(self, cmd):
        cmd = "cd " + self._workdir + " && " + cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        rc = process.poll()
        if rc != 0:
            raise Exception("run cmd error: "+str(rc)+"\n"+stdout+"\n"+stderr)
        return rc

    def download_bundle(self, bundle):
        if bundle.startswith("http://"):
            f = urllib2.urlopen(bundle) 
            self._bundle = os.path.join(self._bundle_dir, os.path.basename(bundle))
            with open(self._bundle, "wb") as zf:     
                zf.write(f.read())
        else:
            self._bundle = bundle

    def extract(self):
        with zipfile.ZipFile(self._bundle, "r") as zf:
            for f in zf.namelist():
                zf.extract(f, self._extract_dir)

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
