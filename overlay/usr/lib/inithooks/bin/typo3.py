#!/usr/bin/python
"""Set Typo3 admin password

Option:
    --pass=     unless provided, will ask interactively

"""

import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Typo3 Password",
            "Enter new password for the Typo3 'admin' account.")

    hash = hashlib.md5(password).hexdigest()

    m = MySQL()
    for username in ('admin', 'simple_editor', 'advanced_editor', 'news_editor'):
        m.execute('UPDATE typo3.be_users SET password=\"%s\" WHERE username=\"%s\";' % (hash, username))

    config = "/var/www/typo3/typo3conf/LocalConfiguration.php"
    system("sed -i \"s|?>|\$TYPO3_CONF_VARS['BE']['installToolPassword'] = '%s';\\n// Updated by inithook\\n?>|\" %s" % (hash, config))

if __name__ == "__main__":
    main()
