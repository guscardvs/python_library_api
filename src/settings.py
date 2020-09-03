import mongoengine as mongo
import os


mongo.connect(os.getenv("DATABASE", "Library"))

PROJECT_KEY = os.getenv(
    "PROJECT_KEY", '60a7b8de951700195f19de87a17759b1dd8317c8cba2b1283256bc016554274cc1298fb29cb979b60d91006bd22adcf606d71ff4b06f366465cc80b809159020')
