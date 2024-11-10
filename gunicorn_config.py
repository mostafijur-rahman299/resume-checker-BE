bind = "0.0.0.0:8000"
module = "resume_checker.wsgi:application"

workers = 4  # Adjust based on your server's resources
worker_connections = 1000
threads = 4

# certfile = "/etc/letsencrypt/live/resumechecker-be.mostafijur.xyz/fullchain.pem"
# keyfile = "/etc/letsencrypt/live/resumechecker-be.mostafijur.xyz/privkey.pem"
