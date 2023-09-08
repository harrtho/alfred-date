#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2023 Thomas Harr <xDevThomas@gmail.com>
# Copyright (c) 2014 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-12
#

"""
"""

import locale
import sys
from datetime import date

from workflow import ICON_ERROR, Workflow

# GitHub repo for self-updating
UPDATE_SETTINGS = {'github_slug': 'harrtho/alfred-date'}

# GitHub Issues
HELP_URL = 'https://github.com/harrtho/alfred-date/issues'

# Icon shown if a newer version is available
ICON_UPDATE = 'update-available.png'

log = None


def main(wf):
    import common
    common.log = log

    log.debug('-' * 40)

    common.set_locale()

    lc, encoding = locale.getlocale()
    log.debug('args : {}'.format(wf.args))
    log.debug('locale : {}  encoding : {}'.format(lc, encoding))

    # Notify user if update is available
    # ------------------------------------------------------------------
    if wf.update_available:
        wf.add_item('Workflow Update is Available',
                    '↩ or ⇥ to install',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=ICON_UPDATE)

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    log.debug('query : {}'.format(query))

    if not query or query in ('0', 'now', 'today'):
        dt = date.today()
    else:
        dt = common.parse_query(query)

    if not dt:  # Didn't understand query
        wf.add_item("Couldn't understand '{}'".format(query),
                    "Use 'datehelp' for help on formatting",
                    valid=False, icon=ICON_ERROR)
        wf.send_feedback()
        return 0
    log.debug('date : {0.year}-{0.month}-{0.day}'.format(dt))
    # get date formats
    for i, fmt in enumerate(common.get_formats()):
        value = common.date_with_format(dt, fmt)
        wf.add_item(value,
                    'Copy to clipboard',
                    arg=value,
                    valid=True,
                    uid='date-{:02d}'.format(i),
                    icon='icon.png')
    wf.send_feedback()
    log.debug('finished.')


if __name__ == '__main__':
    wf = Workflow(update_settings=UPDATE_SETTINGS,
                  help_url=HELP_URL)
    log = wf.logger
    sys.exit(wf.run(main))
