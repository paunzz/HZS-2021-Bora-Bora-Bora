from datetime import datetime

from base import session
from models import Info

now = datetime.now().date()


def get_flags(events):
    flags = []

    for event in events:
        flags.append(['gray', ''])
        # if event is None:
        #     flags.append(['gray', ''])
        #     break
        # else:
        #     delta = (event - now).days
        # if delta is None:
        #     flags.append(['gray', ''])
        # elif delta < 0:
        #     flags.append(['#FF1744', 0])
        # elif delta < 10:
        #     flags.append(['#FF1744', delta])
        # elif delta < 31:
        #     flags.append(['#FFEA00', delta])
        # else:
        #     flags.append(['#66BB6A', delta])

    return flags
