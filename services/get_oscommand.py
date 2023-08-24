from dotenv import load_dotenv
from os import popen,getenv

##Load the .env file
load_dotenv()

def cmdline(command):
    process = popen(command)
    return process.read()

##Get current branch
GITBRANCH = cmdline('git rev-parse --abbrev-ref HEAD')
IFBRANCH = getenv("GIT_BRANCH")
GITBRANCH = str(GITBRANCH)
IFBRANCH = str(IFBRANCH)
print(f"IF branch is:{IFBRANCH}")
print(f"Git branch is:{GITBRANCH}")