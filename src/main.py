from subprocess import run as subprocess_run, PIPE as subprocess_PIPE
from datetime import datetime
from threading import Thread
from argparse import ArgumentParser
from PIL import ImageGrab
import os
import keyboard
import re


class BaseOS:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def capture(self, output_file: str) -> None:
        screenshot = ImageGrab.grab()
        screenshot.save(output_file)

    def capture_thread(self, output_file: str) -> Thread:
        thread = Thread(target=self.capture, args=(output_file,))
        thread.start()
        return thread

    def after_script_execution(self) -> None:
        pass


class HyprlandLinuxOS(BaseOS):
    def __init__(self, output_dir):
        super().__init__(output_dir)

    @staticmethod
    def execute_command(command: str) -> str:
        result = subprocess_run(
            command,
            shell=True,
            stdout=subprocess_PIPE,
            stderr=subprocess_PIPE,
            text=True,
        )
        if result.returncode != 0:
            return result.stderr
        else:
            return result.stdout

    def get_active_window_geometry(self) -> str:
        command = "hyprctl activewindow | grep -E '([0-9]+),([0-9]+)' | awk '{printf \"%s %s\", $2, $3}' | sed 's/,/x/2'"
        return self.execute_command(command)

    # Takes about 0.37 seconds to run
    def capture(self, output_file: str) -> None:
        geometry = self.get_active_window_geometry()
        self.execute_command(f'grim -g "{geometry.strip()}" {output_file}')

    def after_script_execution(self) -> None:
        username = self.output_dir.split("/")[2]
        group = self.execute_command(f"id -gn {username}").strip()
        self.execute_command(f"sudo chown -R {username}:{group} {self.output_dir}")


def configure_os():
    if os.environ.get("XDG_SESSION_TYPE") == "wayland":
        return HyprlandLinuxOS
    else:
        return BaseOS


configured_os = configure_os()


class OptiNotes(configured_os):
    def __init__(self, output_dir: str, mappings: dict, threading: bool = False) -> None:
        super().__init__(output_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir
        self.mappings = mappings
        self.threading = threading
        self.date_format = "%Y-%m-%d_%H:%M:%S.%f"
        self.last_thread = None
        self.queue = []

    @staticmethod
    def pprint(msg: str, color: str = "white", **kwargs) -> None:
        colors = {"white": "\033[0m", "red": "\033[31m", "green": "\033[32m"}
        print(f"{colors[color]}{msg}{colors['white']}", **kwargs)

    def _handle_queue(self) -> None:
        res = []
        for i in self.queue:
            if i != "D" or len(res) == 0:
                res.append(i)
            else:
                res.pop()
        self.queue = res

    def _handle_user_input(self, e) -> None:
        if e.event_type == keyboard.KEY_DOWN and e.name in self.mappings.keys():
            self.queue.append(self.mappings[e.name])
            self._handle_queue()

    def _generate_name(self, filetype: str = "png") -> str:
        return datetime.now().strftime(self.date_format) + f".{filetype}"

    def _get_most_recent_file(self) -> str:
        files = os.listdir(self.output_dir)
        if len(files) == 0:
            return None
        files = [
            i
            for i in files
            if re.match(r"^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.\d{6}\S+$", i)
        ]
        files.sort(
            key=lambda x: datetime.strptime(
                ".".join(x.split(".")[:-1])[:-4], self.date_format
            )
        )
        return files[-1]

    def _main_loop(self) -> None:
        while True:
            if len(self.queue) == 0:
                continue
            command = self.queue.pop(0)
            if command == "C":
                name = self._generate_name()
                capture_method = self.capture_thread if self.threading else self.capture
                self.last_thread = self.capture_thread(rf"{self.output_dir}/{name}")
                capture_method(rf"{self.output_dir}/{name}")
                self.pprint(f"Captured {name}", color="green")
            elif command == "D":
                if self.last_thread is not None:
                    self.last_thread.join()
                to_delete = self._get_most_recent_file()
                if to_delete is None:
                    self.pprint("Directory is empty. Nothing to delete.", color="red")
                    continue
                os.remove(rf"{self.output_dir}/{to_delete}")
                self.pprint(f"Deleted {to_delete}", color="red")

    def _keyboard_thread(self) -> None:
        try:
            keyboard.wait()
        except:
            pass
        finally:
            keyboard.unhook_all()

    def run(self) -> None:
        keyboard.hook(self._handle_user_input)
        Thread(target=self._keyboard_thread, daemon=True).start()
        try:
            self._main_loop()
        except KeyboardInterrupt:
            self.after_script_execution()
            self.pprint(f'Interrupted by keyboard action. Exiting...', color='green')


if __name__ == "__main__":
    parser = ArgumentParser(description="PyNote")
    parser.add_argument("output", nargs="?", type=str, help="Output directory")
    parser.add_argument(
        "-kc", "--key-capture", type=str, help="Key to capture", default="f2"
    )
    parser.add_argument(
        "-kd", "--key-delete", type=str, help="Key to delete", default="f4"
    )
    parser.add_argument(
        "-t", "--threading", action='store_true', help="Enable threading"
    )
    args = parser.parse_args()
    mappings = {args.key_capture: "C", args.key_delete: "D"}
    OptiNotes(args.output, mappings, threading=args.threading).run()
