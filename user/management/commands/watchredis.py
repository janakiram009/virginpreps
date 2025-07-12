import os
import socket
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Checks if Redis on port 6380 is running. Starts it if not."

    def handle(self, *args, **kwargs):
        port = 6380
        redis_bin = os.path.expanduser("/usr/bin/redis-server")

        # Try to connect to the port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(1)
            s.connect(("127.0.0.1", port))
            self.stdout.write("✅ Redis is already running on port 6380.")
            return
        except (ConnectionRefusedError, socket.timeout):
            self.stdout.write("⚠️ Redis is NOT running on port 6380. Attempting to start it...")
        finally:
            s.close()

        # Start Redis
        if not os.path.exists(redis_bin):
            self.stderr.write("❌ Redis binary not found at /user/bin/redis-server")
            return

        subprocess.Popen([redis_bin, "--port", str(port), "--bind", "127.0.0.1"])
        self.stdout.write("🚀 Redis started.")
