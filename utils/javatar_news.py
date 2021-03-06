import sublime
from .javatar_actions import add_action
from .javatar_usage import send_usages, get_usage_data
from .javatar_utils import start_clock, stop_clock


# YY.MM.DD.HH.MM
VERSION = "14.11.12.23.14b"
UPDATEFOR = "all"
NEWSID = 18

NEWS_TEMPLATE = '''\
Just install Javatar? Checkout JavatarDoc for Javatar information and guides. Link is located in README file.

A small update but got a new improvement on class creation. Be sure to checkout JavaDoc!
These are updates and fixes for Javatar {VERSION}...
- Build notification via SubNotify (more details in JavatarDoc)
- Fix package/class creation did not show any details
- Fix Javatar Shell cause Sublime Text crash on output encoding error
- Javatar Shell will now scroll to bottom
- Class creation improvements (See JavaDoc for more information)
- Remove abstract class snippets since a new class creation improvement can do more!

You can report/suggest any issue on Javatar repository. Link is already located in README file.
'''


def get_version():
    return VERSION


def show_news(title, prefix=""):
    news = NEWS_TEMPLATE.format(VERSION=get_version())

    view = sublime.active_window().new_file()
    view.set_name(title)
    view.run_command("javatar_util", {"util_type": "add", "text": prefix + news})
    view.set_read_only(True)
    view.set_scratch(True)


def check_news():
    add_action("javatar.util.news", "Check news")
    from .javatar_utils import get_settings, set_settings, is_stable
    if get_settings("message_id") < NEWSID:
        if get_settings("message_id") != -1:
            stop_clock(notify=False)
            if is_stable() and (UPDATEFOR == "stable" or UPDATEFOR == "all"):
                show_news("Javatar: Package has been updated!")
                add_action(
                    "javatar.util.news", "Show stable news"
                )
            elif not is_stable() and (UPDATEFOR == "dev" or UPDATEFOR == "all"):
                show_news("Javatar [Dev]: Package has been updated!")
                add_action("javatar.util.news", "Show dev news")
            start_clock()
            send_usages(get_usage_data())
            set_settings("message_id", NEWSID)
        elif get_settings("javatar_gp") & 0x1 == 0:
            send_usages(get_usage_data(), True)
