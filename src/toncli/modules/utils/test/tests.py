# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import json
import os
import tempfile
from typing import List

from toncli.modules.utils.fift.fift import Fift, FiftParser
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.system.conf import getcwd, project_root
from toncli.modules.utils.system.project_conf import ProjectConf
from colorama import Fore, Style
from jinja2 import FileSystemLoader, select_autoescape, Environment

from toncli.modules.utils.test.commands import build_test

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


class TestsRunner:
    def __init__(self):
        self.project_config = ProjectConf(getcwd())

    def run(self, contracts: List[str], tests: List[str], verbose: int, output_results: bool = False,
            run_tests_old_way: bool = False, silent: bool = False):
        logger.info(f"🌈 Start tests")
        if contracts is not None and len(contracts) > 0:
            real_contracts = []

            for item in contracts:
                for config in self.project_config.contracts:
                    if config.name == item:
                        real_contracts.append(config)
        else:
            real_contracts = list(
                filter(lambda p: len(p.func_tests_files_locations) > 0, self.project_config.contracts))

        if not len(real_contracts):
            logger.error(f"😥 No contracts [{contracts}] are founded in project.yaml")

        to_save_location = os.path.abspath(f"{getcwd()}/build")

        # Build code
        build_test(getcwd(), contracts=real_contracts, cwd=getcwd(), compile_tests_with_contract=not run_tests_old_way)

        location = to_save_location.replace(getcwd(), '')
        logger.info(f"🥌 Build {gr}successfully{rs}, check out {gr}.{location}{rs}")

        total_to_save = []
        output_path = os.path.abspath(f"{getcwd()}/tests_output.json")

        if output_results and os.path.exists(output_path):
            os.remove(output_path)

        exit_codes = []
        for contract in real_contracts:
            # Add info to Jinja template

            render_kwargs = {
                'code_path': contract.to_save_location,
                'test_path': contract.to_save_tests_location,
                'output_results': int(output_results),
                'output_path': output_path,
                'contract_data': contract.data,
                'verbose': verbose,
                'silent': int(silent)
            }

            if tests is not None and len(tests) > 0:
                parser = FiftParser(contract.to_save_tests_location)
                tests_found = parser.lookup_tests(tests)
                if len(tests_found) > 0:
                    render_kwargs['tests'] = tests_found
                else:
                    # Skip contract if tests specified and not found
                    logger.error(f"😥 No tests found for:{rd}{contract.name}{rs}")
                    continue

            # Load template of transaction_debug
            loader = FileSystemLoader(f"{project_root}/modules/fift")

            env = Environment(
                loader=loader,
                autoescape=select_autoescape()
            )

            template_name = "run_test_old.fif.template" if run_tests_old_way else "run_test.fif.template"
            template = env.get_template(template_name)

            rendered = template.render(**render_kwargs)
            temp_location: str = tempfile.mkstemp(suffix='.fif')[1]
            with open(temp_location, 'w', encoding='utf-8') as f:
                f.write(rendered)

            # Run generated by jinja fift script
            fift = Fift('run', args=[temp_location])  # prev_block])
            output = fift.run_script(True)
            output_text = output.stdout.read()
            c = output.communicate()[0]
            exit_code = output.returncode

            print(output_text)
            exit_codes.append(exit_code)

            cur = -2

            if output_results:
                runvm_output = output_text.split('\n')

                for item in runvm_output:
                    if "[vm.cpp:558]" in item:
                        cur += 1
                        if cur % 3 != 0:
                            continue

                        to_save = {}
                        sitem = item.split()

                        for i in sitem:
                            if 'max' in i:
                                to_save['max'] = i.replace(',', '').replace('max=', '')
                            elif 'limit' in i:
                                to_save['limit'] = i.replace(',', '').replace('limit=', '')
                            elif 'used' in i:
                                to_save['used'] = i.replace(',', '').replace('used=', '')

                        total_to_save.append(to_save)

        if output_results:
            with open(output_path) as f:
                test_output = f.read().split('\n')[1:]
                assert len(test_output) == len(total_to_save), "Tests output and parsed vm states must be same length"

            output = []

            for item, vm_output in zip(test_output, total_to_save):
                sitem = item.split()

                assert int(sitem[2]) == int(vm_output['used']), "Gas used in vm and in output must be the same"

                output.append({
                    'name': sitem[0].replace('"', ''),
                    'exit_code': int(sitem[1]),
                    'gas_used': int(sitem[2]),
                    'gas_limit_vm': int(vm_output['limit']),
                    'gas_max_vm': int(vm_output['max']),
                })

            with open(output_path, 'w') as f:
                json.dump({'tests': output}, f, indent=4, sort_keys=True)

        if len(exit_codes):
            exit(max(exit_codes))
