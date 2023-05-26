# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import os

env = os.environ.get('APP_ENV', 'develop')

if env == 'development':
    from .development import *
elif env == 'production':
    from .production import *
else:
    from .testing import *
