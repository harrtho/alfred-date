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

"""formats.py [options] <action> [<format>]

Usage:
    formats.py (-h | --help)
    formats.py show
    formats.py new <format>
    formats.py delete <format>
    formats.py add <format>
    formats.py reset

Options:
    -h, --help  Show this help message.
"""

import sys
from datetime import date

from workflow import ICON_ERROR, ICON_INFO, ICON_WARNING, Workflow

log = None


def main(wf):
    import common
    from docopt import docopt
    common.log = log

    log.debug('-' * 40)

    common.set_locale()

    args = docopt(__doc__, argv=wf.args)
    log.debug('args : {}'.format(args))
    fmt = args.get('<format>')

    date_formats = wf.settings.get('date_formats', [])

    # add a new format
    if args.get('new'):
        if fmt in common.get_formats():
            wf.add_item("'{}' already exists".format(fmt),
                        'Try something else',
                        valid=False,
                        icon=ICON_WARNING)
        elif not common.format_valid(fmt):
            wf.add_item("'{}' is not a valid date format".format(fmt),
                        "Use 'datehelp' for formatting help",
                        valid=False,
                        icon=ICON_ERROR)
        else:
            value = unicode(common.date_with_format(date.today(), fmt),
                            'utf-8')
            wf.add_item("Save '{}' to custom formats".format(fmt),
                        'e.g. {}'.format(value),
                        valid=True,
                        arg=fmt,
                        icon='icon.png')

        wf.send_feedback()

    # show existing custom formats
    elif args.get('show'):

        if not date_formats:  # warn of no formats
            wf.add_item('You have no custom formats',
                        "Use 'dtadd' to add a custom format",
                        valid=False,
                        icon=ICON_INFO)

        else:  # list custom formats
            for f in date_formats:
                value = unicode(common.date_with_format(date.today(), f),
                                'utf-8')
                wf.add_item(f,
                            'e.g. {}'.format(value),
                            valid=True,
                            arg=f,
                            icon='icon.png')

        wf.send_feedback()

    # add new format
    elif args.get('add'):

        if fmt not in date_formats:
            date_formats.append(fmt)
            wf.settings['date_formats'] = date_formats
            print("'{}' saved".format(fmt))
        else:
            print("'{}' already exists".format(fmt))

    # delete existing format
    elif args.get('delete'):

        if fmt not in date_formats:
            print("'{}' does not exist".format(fmt))
        else:
            date_formats.remove(fmt)
            wf.settings['date_formats'] = date_formats
            print("'{}' deleted".format(fmt))

    # delete custom formats and restore defaults
    elif args.get('reset'):

        wf.settings['date_formats'] = common.get_default_formats()
        log.debug('Formats restored to defaults')
        log.debug(wf.settings['date_formats'])

    log.debug('finished.')


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
