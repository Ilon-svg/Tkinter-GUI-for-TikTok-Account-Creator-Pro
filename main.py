#!/usr/bin/env python3
"""
TikTok Account Creator Pro v3.0
Entry Point - CLI / GUI / API

Author: Maria Bosser
Telegram: @mariabosser
Channel: @Sectools1
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core import AccountManager, ColoredLogger


def main():
    parser = argparse.ArgumentParser(
        description="TikTok Account Creator Pro v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --gui                    # Launch GUI
  python main.py --api --port 8000        # Start API server
  python main.py --count 10 --region US  # CLI batch mode
        """
    )
    
    parser.add_argument("--gui", action="store_true", help="Launch GUI mode")
    parser.add_argument("--api", action="store_true", help="Start API server")
    parser.add_argument("--port", type=int, default=8000, help="API port")
    parser.add_argument("--count", type=int, default=1, help="Number of accounts")
    parser.add_argument("--region", default="US", help="Account region")
    parser.add_argument("--config", default="config.json", help="Config file")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.version:
        from src import __version__, __author__, __contact__
        print(f"TikTok Account Creator Pro v{__version__}")
        print(f"Author: {__author__}")
        print(f"Contact: {__contact__}")
        return
    
    logger = ColoredLogger("main")
    logger.info("=" * 60)
    logger.info("TikTok Account Creator Pro v3.0")
    logger.info("=" * 60)
    
    if args.gui:
        logger.info("Launching GUI...")
        from src.gui.app import launch_gui
        launch_gui()
    
    elif args.api:
        logger.info(f"Starting API server on port {args.port}...")
        import uvicorn
        from src.api import create_app
        app = create_app(args.config)
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    
    else:
        logger.info("CLI Mode")
        manager = AccountManager(config=args.config)
        results = manager.run_batch(
            count=args.count,
            region=args.region
        )
        logger.success(f"Complete: {len([r for r in results if r.status == 'success'])} accounts created")


if __name__ == "__main__":
    main()
