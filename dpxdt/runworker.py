#!/usr/bin/env python
# Copyright 2013 Brett Slatkin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Runs a dpxdt queue worker.

Example usage:

PYTHONPATH=./lib:$PYTHONPATH \
./dpxdt/runworker.py \
    --phantomjs_binary=path/to/phantomjs-1.8.1-macosx/bin/phantomjs \
    --phantomjs_script=path/to/client/capture.js \
    --pdiff_binary=path/to/pdiff/perceptualdiff \
    --pdiff_queue_url=http://localhost:5000/api/work_queue/run-pdiff \
    --capture_queue_url=http://localhost:5000/api/work_queue/run-capture
"""

import logging
import sys
import threading

# Local Libraries
import gflags
FLAGS = gflags.FLAGS

# Local modules
from client import capture_worker
from client import pdiff_worker
from client import queue_workers
from client import workers


def run_workers():
    coordinator = workers.GetCoordinator()
    capture_worker.register(coordinator)
    pdiff_worker.register(coordinator)
    queue_workers.register(coordinator)
    coordinator.start()
    logging.info('Workers started')
    while True:
        item = coordinator.output_queue.get()
        item.check_result()


def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)

    if FLAGS.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    run_workers()


if __name__ == '__main__':
    main(sys.argv)
