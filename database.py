from sqlalchemy import create_engine  # pyright: ignore[reportMissingImports]

from sqlalchemy.orm import declarative_base, sessionmaker  # pyright: ignore[reportMissingImports]

# PASTE YOUR NEON STRING HERE:
DATABASE_URL = "postgresql://neondb_owner:npg_I0ZaFPrde7Xc@ep-shy-glitter-aedwq013-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()