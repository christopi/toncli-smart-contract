import os
import tempfile
from typing import List

from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.system.conf import getcwd, project_root
from toncli.modules.utils.system.project_conf import ProjectConf
from colorama import Fore, Style
from toncli.modules.utils.func.commands import build as fift_build
from jinja2 import FileSystemLoader, select_autoescape, Environment

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


class TestsRunner:
    def __init__(self):
        self.project_config = ProjectConf(getcwd())

    def run(self, contracts: List[str], verbose: int, output_results: bool = False):
        logger.info(f"🌈 Start tests")

        if contracts is not None and len(contracts) > 0:
            real_contracts = []

            for item in contracts:
                for config in self.project_config.contracts:
                    if config.name == item:
                        real_contracts.append(config)
        else:
            real_contracts = self.project_config.contracts

        if not len(real_contracts):
            logger.error(f"😥 No contracts [{contracts}] are founded in project.yaml")

        to_save_location = os.path.abspath(f"{getcwd()}/build")

        # Build code
        fift_build(getcwd(), contracts=real_contracts, cwd=getcwd(), use_tests_lib=True)

        location = to_save_location.replace(getcwd(), '')
        logger.info(f"🥌 Build {gr}successfully{rs}, check out {gr}.{location}{rs}")

        for contract in real_contracts:
            # Add info to Jinja template
            render_kwargs = {
                'code_path': contract.to_save_location,
                'test_path': contract.to_save_tests_location,
                'output_results': int(output_results),
                'output_path': os.path.abspath(f"{getcwd()}/tests_output"),
                'verbose': verbose
            }

            # Load template of transaction_debug
            loader = FileSystemLoader(f"{project_root}/modules/fift")

            env = Environment(
                loader=loader,
                autoescape=select_autoescape()
            )

            template = env.get_template("run_test.fif.template")

            rendered = template.render(**render_kwargs)
            temp_location: str = tempfile.mkstemp(suffix='.fif')[1]
            with open(temp_location, 'w', encoding='utf-8') as f:
                f.write(rendered)

            # Run generated by jinja fift script
            fift = Fift('run', args=[temp_location])  # prev_block])
            fift.run()
