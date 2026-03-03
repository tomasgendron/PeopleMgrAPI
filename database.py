from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from azure.identity import DefaultAzureCredential
import struct

server = "tomas-test-sqlserver.database.windows.net"
database = "tomas-test-sqldb"
driver = "SQL Server"
connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Authentication=ActiveDirectoryMsi"

credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

SQL_COPT_SS_ACCESS_TOKEN = 1256 

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={connection_string}",
    connect_args={"attrs_before": {SQL_COPT_SS_ACCESS_TOKEN: token_struct}},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
