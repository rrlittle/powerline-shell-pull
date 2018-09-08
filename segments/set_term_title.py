import os
import socket
from ..utils import BasicSegment
from powerline_shell import Powerline, CustomImporter
import argparse


class Segment(BasicSegment):
    def format(self, shell, content):
        wrappers = {
            'bash': '\\[\\e]0;%s\\a\\]',
            'zsh': '%{\033]0;%s\007%}'
        }
        default = '\033]0;%s\007'
        return wrappers.get(shell, default) % content

    def build_title_segments(self, segment_names):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--shell', action='store', default='bash',
                                choices=['bash', 'tcsh', 'zsh', 'bare'])
        arg_parser.add_argument('prev_error', nargs='?', type=int, default=0,
                                help='Error code returned by the last command')
        args = arg_parser.parse_args()

        importer = CustomImporter()
        theme_mod = importer.import_(
            'powerline_shell.themes.', 'default', 'Theme')
        theme = getattr(theme_mod, 'Color')
        powerline = Powerline(args, {}, theme)
        segments = []
        for seg_name in segment_names:
            seg_mod = importer.import_(
                'powerline_shell.segments.', seg_name, 'Segment')
            segment = getattr(seg_mod, 'Segment')(powerline)
            segments.append(segment)
        for segment in segments:
            segment.add_to_powerline()
        output = '>'.join([s[0] for s in powerline.segments])
        print(output, powerline.segments)
        return output

    def build_title(self, title):
        if type(title) in (str, unicode):
            return title
        elif type(title) is list:
            return self.build_title_segments(title)
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
