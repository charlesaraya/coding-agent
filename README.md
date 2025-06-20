# Coding Buddy — A CLI Coding AI Agent

**CodeBuddy** is a Python-based command-line tool that accepts natural language coding tasks and attempts to solve them autonomously by chaining together a set of predefined capabilities.

## What It Does

1. Interprets the task and chooses from a toolkit of functions:
   - Scan files in a directory
   - Read a file's contents
   - Overwrite a file with new content
   - Run a Python script and analyze the output
2. Chains these tools together, attempting to resolve the issue.
3. Repeats the cycle until it:
   - solves the problem
   - or fails

## Features

- Interactive or programmatic CLI interface
- Modular task-solving strategy using tool chaining
- Basic introspection and feedback loop
- Can mutate code and test results in real-time

## Example Usage

```bash
$ python agent.py "my script throws a TypeError on line 23 😭"
