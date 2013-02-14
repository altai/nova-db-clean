#!/usr/bin/env python

import sys

from datetime import timedelta
from datetime import datetime

from nova import flags
from nova import log as logging
from nova import utils

from nova.openstack.common import cfg

from nova.db.sqlalchemy import models
from nova.db.sqlalchemy.session import get_session

my_opts = [
    cfg.IntOpt('db_purge_days',
               default=6,
               help=_('How many days keep data in the database')),
    ]

if __name__ == '__main__':

    FLAGS = flags.FLAGS
    FLAGS.register_opts(my_opts)

    utils.default_flagfile()
    flags.FLAGS(sys.argv)
    logging.setup()

    db_purge_day = datetime.now() - timedelta(FLAGS.db_purge_days)
    db_deadline = db_purge_day.strftime('%Y-%m-%d %H:%M:%S')

    session = get_session()
    with session.begin():
        print "=" * 44
        print "Startting from %s (%s days)" % (db_deadline,FLAGS.db_purge_days)
        print "=" * 44
        result = session.query(models.Instance).\
                filter_by(deleted=True).\
                filter(models.Instance.deleted_at < db_deadline).\
                delete()
        print "Deleted %s instances." % result

        result = session.query(models.SecurityGroupInstanceAssociation).\
                filter_by(deleted=True).\
                filter(models.SecurityGroupInstanceAssociation.deleted_at < db_deadline).\
                delete()
        print "Deleted %s security groups." % result

        result = session.query(models.InstanceMetadata).\
                filter_by(deleted=True).\
                filter(models.InstanceMetadata.deleted_at < db_deadline).\
                delete()
        print "Deleted %s instances metadata." % result

        result = session.query(models.BlockDeviceMapping).\
                filter_by(deleted=True).\
                filter(models.BlockDeviceMapping.deleted_at < db_deadline).\
                delete()
        print "Deleted %s block device mappings." % result
        print "=" * 44

