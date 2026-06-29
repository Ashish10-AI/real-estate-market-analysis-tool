import os
import sys

# Add src directory to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import dashboard.app as dashboard_app

if __name__ == "__main__":
    dashboard_app.main()
