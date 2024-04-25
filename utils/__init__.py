import logging

# Create a logger
logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
