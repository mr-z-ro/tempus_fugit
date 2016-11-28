# Copyright 2016 Google Inc.
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

""" appengine_config.py gets loaded when starting a new application instance """

import os.path

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
#vendor.add('lib')
# to avoid errors while running this in different environments i.e. production, development, staging e.t.c.
# reference the 'lib' folder using an absolute path
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)),'lib'))

##
## Enable ctypes on dev appserver so we get proper flask tracebacks. From http://jinja.pocoo.org/docs/dev/faq/#my-tracebacks-look-weird-what-s-happening
## and http://stackoverflow.com/questions/3086091/debug-jinja2-in-google-app-engine
PRODUCTION_MODE = not os.environ.get(
    'SERVER_SOFTWARE', 'Development').startswith('Development')
if not PRODUCTION_MODE:
    from google.appengine.tools.devappserver2.python import sandbox
    sandbox._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
    import os
    import sys
    if os.name == 'nt':
        os.name = None
        sys.platform = ''
