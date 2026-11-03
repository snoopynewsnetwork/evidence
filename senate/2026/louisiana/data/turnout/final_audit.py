"""Read-only final audit prints stdout; never redirect into an owned file after seal."""
import sys
sys.dont_write_bytecode=True
from repair_readonly import main
if __name__=='__main__':main()
