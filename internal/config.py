import os
import sys
import argparse
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("MODEL_NAME")

        self.verbose = False
        self.prompt = ''
        self._parse_args()

    def _parse_args(self):
        parser = argparse.ArgumentParser(
            prog = 'Coding Agent',
            description = """
                CodeGrind is an intelligent coding agent designed to help you improve your programming\n
                skills through hands-on challenges, automatic testing, and real-time feedback.\n
                Run custom exercises, track progress, and level up your problem-solving abilities.\n"""
            ,
            epilog = """Example usage:\n
                \tpython3 main.py "user prompt"\n\n
                For more information, visit the documentation or use the --help flag with subcommands.\n
                """
        )
        parser.add_argument('user_prompt', nargs='?', help="Message to the agent (positional)")
        parser.add_argument('-p', '--prompt', help="Message to the agent (optional flag)")
        parser.add_argument('--iterations', help="Number of max iterations allowed by agent (optional flag)", default=20)
        parser.add_argument('--prod', help="Run the agent in development mode (optional flag)", default=False)
        parser.add_argument('-v', '--verbose', help="turns verbose mode on to help debugging (optional flag)", action='store_true', default=False)
        args = parser.parse_args()

        # Enforce: exactly one of the two must be provided
        if bool(args.user_prompt) and bool(args.prompt):  # both or neither
            parser.error("You must provide either a positional prompt OR use -p/--prompt.")

        self.prompt = args.prompt or args.user_prompt
        self.verbose = args.verbose or not args.prod
        self.iterations = args.iterations