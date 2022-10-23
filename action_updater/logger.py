__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import inspect
import logging as _logging
import os
import platform
import random
import sys
import threading

import rich.console
import rich.table


class Table:
    """
    Format a list of dicts into a table
    """

    def __init__(self, items):
        self.data = items
        self.max_widths = {}
        self.ensure_complete()

    def available_width(self, columns):
        """
        Calculate available width based on fields we cannot truncate (urls)
        """
        # We will determine column width based on terminal size
        try:
            width = os.get_terminal_size().columns
        except OSError:
            width = 120

        # Calculate column width
        column_width = int(width / len(columns))
        updated = width

        for _, needed in self.max_widths.items():
            updated = updated - needed

        # We don't have enough space
        if updated < 0:
            logger.warning("Terminal is too small to correctly render!")
            return column_width

        # Otherwise, recalculate column width taking into account truncation
        # We use the updated smaller width, and break it up between columns
        # that don't have a max width
        return int(updated / (len(columns) - len(self.max_widths)))

    def ensure_complete(self):
        """
        If any data missing fields, ensure they are included
        """
        fields = set()
        for entry in self.data:
            [fields.add(x) for x in entry.keys()]

        # Ensure fields are present
        for entry in self.data:
            for field in fields:

                if field not in entry:
                    entry[field] = ""

    @property
    def color(self):
        """
        Return a random color
        """
        return "color(" + str(random.choice(range(255))) + ")"

    def table_columns(self):
        """
        Shared function to return consistent table columns
        """
        if not self.data:
            return []
        return list(self.data[0].keys())

    def table_rows(self, columns, limit=25):
        """
        Shared function to yield rows as a list
        """
        # All keys are lowercase
        column_width = self.available_width(columns)

        for i, row in enumerate(self.data):

            # have we gone over the limit?
            if limit and i > limit:
                return

            parsed = []
            for column in columns:
                content = row[column]
                if (
                    content
                    and len(content) > column_width
                    and column not in self.endpoint.truncate_list
                ):
                    content = content[:column_width] + "..."
                parsed.append(content)
            yield parsed

    def show(self, limit=25, title=None):
        """
        Pretty print a table of content
        """
        table = rich.table.Table(title=title)

        # Always skip these columns
        seen_colors = []

        # Get column titles
        columns = self.table_columns()
        for column in columns:
            color = None
            while not color or color in seen_colors:
                color = self.color
            table.add_column(column.capitalize(), style=color)

        # Add rows
        for row in self.table_rows(columns, limit=limit):
            table.add_row(*row)

        # And print!
        console = rich.console.Console()
        console.print(table, justify="left")


class LogColors:
    PURPLE = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def underline(msg):
    """
    Return an underlined message
    """
    return f"{LogColors.UNDERLINE}{msg}{LogColors.ENDC}"


def add_prefix(msg, char=">>"):
    """
    Add an "OKBLUE" prefix to a message
    """
    return f"{LogColors.OKBLUE}{char}{LogColors.ENDC} {msg}"


class ColorizingStreamHandler(_logging.StreamHandler):

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    RESET_SEQ = LogColors.ENDC
    COLOR_SEQ = "\033[%dm"
    BOLD_SEQ = "\033[1m"

    colors = {
        "WARNING": YELLOW,
        "INFO": GREEN,
        "DEBUG": BLUE,
        "CRITICAL": RED,
        "ERROR": RED,
    }

    def __init__(self, nocolor=False, stream=sys.stderr, use_threads=False):
        super().__init__(stream=stream)
        self._output_lock = threading.Lock()
        self.nocolor = nocolor or not self.can_color_tty()

    def can_color_tty(self):
        if "TERM" in os.environ and os.environ["TERM"] == "dumb":
            return False
        return self.is_tty and not platform.system() == "Windows"

    @property
    def is_tty(self):
        isatty = getattr(self.stream, "isatty", None)
        return isatty and isatty()

    def emit(self, record):
        with self._output_lock:
            try:
                self.format(record)  # add the message to the record
                self.stream.write(self.decorate(record))
                self.stream.write(getattr(self, "terminator", "\n"))
                self.flush()
            except BrokenPipeError as e:
                raise e
            except (KeyboardInterrupt, SystemExit):
                # ignore any exceptions in these cases as any relevant messages have been printed before
                pass
            except Exception:
                self.handleError(record)

    def decorate(self, record):
        message = record.message
        message = [message]
        if not self.nocolor and record.levelname in self.colors:
            message.insert(0, self.COLOR_SEQ % (30 + self.colors[record.levelname]))
            message.append(self.RESET_SEQ)
        return "".join(message)


class Logger:
    def __init__(self):
        self.logger = _logging.getLogger(__name__)
        self.log_handler = [self.text_handler]
        self.stream_handler = None
        self.printshellcmds = False
        self.quiet = False
        self.logfile = None
        self.last_msg_was_job_info = False
        self.logfile_handler = None

    def cleanup(self):
        if self.logfile_handler is not None:
            self.logger.removeHandler(self.logfile_handler)
            self.logfile_handler.close()
        self.log_handler = [self.text_handler]

    def handler(self, msg):
        for handler in self.log_handler:
            handler(msg)

    def set_stream_handler(self, stream_handler):
        if self.stream_handler is not None:
            self.logger.removeHandler(self.stream_handler)
        self.stream_handler = stream_handler
        self.logger.addHandler(stream_handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def location(self, msg):
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        self.debug("{}: {info.filename}, {info.function}, {info.lineno}".format(msg, info=info))

    def yellow(self, msg):
        self.handler(dict(level="info", msg=msg))

    def info(self, msg):
        self.handler(dict(level="info", msg=msg))

    def warning(self, msg):
        self.handler(dict(level="warning", msg=msg))

    def debug(self, msg):
        self.handler(dict(level="debug", msg=msg))

    def error(self, msg):
        self.handler(dict(level="error", msg=msg))

    def exit(self, msg, return_code=1):
        self.handler(dict(level="error", msg=msg))
        sys.exit(return_code)

    def progress(self, done=None, total=None):
        self.handler(dict(level="progress", done=done, total=total))

    def shellcmd(self, msg):
        if msg is not None:
            msg = dict(level="shellcmd", msg=msg)
            self.handler(msg)

    def text_handler(self, msg):
        """The default log handler prints the output to the console.
        Args:
            msg (dict):     the log message dictionary
        """
        level = msg["level"]
        if level == "info" and not self.quiet:
            self.logger.info(msg["msg"])
        if level == "warning":
            self.logger.warning(msg["msg"])
        elif level == "error":
            self.logger.error(msg["msg"])
        elif level == "debug":
            self.logger.debug(msg["msg"])
        elif level == "progress" and not self.quiet:
            done = msg["done"]
            total = msg["total"]
            p = done / total
            percent_fmt = ("{:.2%}" if p < 0.01 else "{:.0%}").format(p)
            self.logger.info("{} of {} steps ({}) done".format(done, total, percent_fmt))
        elif level == "shellcmd":
            if self.printshellcmds:
                self.logger.warning(msg["msg"])


logger = Logger()


def setup_logger(
    quiet=False,
    printshellcmds=False,
    nocolor=False,
    stdout=False,
    debug=False,
    use_threads=False,
    wms_monitor=None,
):
    # console output only if no custom logger was specified
    stream_handler = ColorizingStreamHandler(
        nocolor=nocolor,
        stream=sys.stdout if stdout else sys.stderr,
        use_threads=use_threads,
    )
    logger.set_stream_handler(stream_handler)
    logger.set_level(_logging.DEBUG if debug else _logging.INFO)
    logger.quiet = quiet
    logger.printshellcmds = printshellcmds
