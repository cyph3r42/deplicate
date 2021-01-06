# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..init import compilecards
from .common import fsdecode
from .posix import has_hidden_attribute as _has_hidden_attribute
from .posix import has_archive_attribute, is_archived, blksize


WILDCARDS = (
    '*.DS_Store', '.AppleDouble', '.LSOverride', 'Icon', '._*',
    '.DocumentRevisions-V100', '.fseventsd', '.Spotlight-V100',
    '.TemporaryItems', '.Trashes', '.VolumeIcon.icns',
    '.com.apple.timemachine.donotpresent', '.AppleDB', '.AppleDesktop',
    'Network Trash Folder', 'Temporary Items', '.apdisk')

_wildcards_match = compilecards(WILDCARDS).match


def has_hidden_attribute(filename):
    try:
        import Foundation

        ufilename = fsdecode(filename)
        url = Foundation.NSURL.fileURLWithPath_(ufilename)
        res = url.getResourceValue_forKey_error_(
            None, Foundation.NSURLIsHiddenKey, None
        )
        flag = res[1]

    except ImportError:
        flag = _has_hidden_attribute(filename)

    return flag


def is_hidden(filename):
    return filename.startswith('.') or has_hidden_attribute(filename)


def is_system(filename):
    return bool(_wildcards_match(filename))
