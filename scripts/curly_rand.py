import os
import random
import re

from modules import scripts, script_callbacks, shared

re_combinations = re.compile(r"\{([^{}]*)}")

class Script(scripts.Script):
    def title(self):
        return "Curly rand"
    
    def _replace_curly_blackets(self, match):
        if match is None or len(match.groups()) == 0:
            return ""

        combinations_str = match.groups()[0]
        variants = combinations_str.split("|")

        return self.gen.choice(variants)

    def run(self, p):
        if not p.all_prompts:
            original_prompt = p.prompt

            self.gen = random.Random()

            p.prompt = re_combinations.sub(lambda x: self._replace_curly_blackets(x), p.prompt)

            if original_prompt != p.prompt:
                p.extra_generation_params["Wildcard prompt"] = original_prompt
        else:
            original_prompt = p.all_prompts[0]

            for i in range(len(p.all_prompts)):
                self.gen = random.Random()
                self.gen.seed(p.all_seeds[0 if shared.opts.wildcards_same_seed else i])

                prompt = p.all_prompts[i]
                prompt = re_combinations.sub(lambda x: self._replace_curly_blackets(x), prompt)
                p.all_prompts[i] = prompt

            if original_prompt != p.all_prompts[0]:
                p.extra_generation_params["Wildcard prompt"] = original_prompt
