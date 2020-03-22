import subprocess

class Py3status:
    """
    """

    # available configuration parameters
    cache_timeout = 600
    format = "UPD[\?not_zero : {dnf}]"

    def post_config_hook(self):
        if not self.py3.check_commands("dnf"):
            raise Exception(STRING_NOT_INSTALLED)

    def dnf_updates(self):
        dnf_updates = self._check_dnf_updates()

        color = self.py3.COLOR_DEGRADED
        if dnf_updates == 0:
            color = self.py3.COLOR_GOOD
        full_text = self.py3.safe_format(self.format, {"dnf": dnf_updates})
        return {
            "color": color,
            "cached_until": self.py3.time_in(self.cache_timeout),
            "full_text": full_text,
        }

    def _check_dnf_updates(self):
        """
        This method will use the 'checkupdates' command line utility
        to determine how many updates are waiting to be installed via
        'apt list --upgradeable'.
        """
        output = subprocess.check_output(["dnf", "check-update"])
        output = output.decode("utf-8").rstrip().split("\n")
        return len(output) - 1


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
