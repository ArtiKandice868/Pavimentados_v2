from pavimentados2.processing import processors, workflows, sources
from pavimentados2.analyzers import calculators, gps_sources
from pavimentados2.downloader import Downloader
import os
import sys

dl = Downloader()
download_models = dl.download