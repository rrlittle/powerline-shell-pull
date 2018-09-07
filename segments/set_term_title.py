import os
import socket
from ..utils import BasicSegment, warn


class Segment(BasicSegment):
    def format(self, shell, content):
        wrappers = {
            'bash': '\\[\\e]0;%s\\a\\]',
            'zsh': '%{\033]0;%s\007%}'
        }
        default = '\033]0;%s\007'
        return wrappers.get(shell, default) % content

    def build_title(self, title):
        if type(title) in (str, unicode):
            return title
        elif type(title) is list:
            err = 'not implemented yet'
            warn(err)
            return err
        else:
            return 'powerline-shell set_term_title title invalid'

    def add_to_powerline(self):
        powerline = self.powerline
        term = os.getenv('TERM')
        if not (('xterm' in term) or ('rxvt' in term)):
            return
        cust_title = powerline.segment_conf('set_term_title', 'title')
        content = (self.build_title(cust_title) if cust_title else
                   '%s@%s: %s' % (os.getenv('USER'),
                                  socket.gethostname().split('.')[0],
                                  powerline.cwd.replace(
                                      os.path.expanduser('~'), '~')
                                  ))
        set_title = self.format(powerline.args.shell, content)
        powerline.append(set_title, None, None, None)
