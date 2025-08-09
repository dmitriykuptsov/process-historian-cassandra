# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database 
SQLALCHEMY_DATABASE_URI = "mysql://ph:password@192.168.1.245/ph"

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 10

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "umLovFucsokustoosepquitViOvufPiv"

# Secret key for signing cookies
SECRET_KEY = "CashFeitjidarIbrInthepicCofIfDij"

# Token key
TOKEN_KEY = "cyedEcnoucJovnugs2OrGhiadkaibJejrercomguItInibWothiOnyodVevrytwu"

# Server noncep
SERVER_NONCE = "udOtJatnaweedlyhoicHubjabmywuShrakkanacDekveClukDas;shrardAnusAj"

# Validity of the token in days
JWT_VALIDITY_IN_DAYS = 30

# Cassandra configuration
CASSANDRA_NODES = ["192.168.1.245"]
CASSANDRA_KEYSPACE = "ph"
