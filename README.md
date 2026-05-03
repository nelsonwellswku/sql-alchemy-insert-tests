# sql-alchemy-insert-tests

A benchmarking project that compares SQLAlchemy bulk insert strategies across **SQL Server** and **PostgreSQL**, measuring the real-world performance differences between common insertion patterns and explaining *why* they behave the way they do.

## Purpose

When inserting large volumes of rows with SQLAlchemy, the choice of method matters far more than most developers expect. This project makes that concrete by timing four different strategies at 50,000 rows each against both database engines and documenting the root causes behind surprising results (NULL-value fragmentation, silent `fast_executemany` bypass, round-trip overhead, etc.).

See [`docs/bulk-insert-performance-analysis.md`](docs/bulk-insert-performance-analysis.md) for the full analysis.

## Insert Strategies Compared

| # | Strategy | Description |
|---|----------|-------------|
| 1 | `Session.add_all()` | Standard ORM unit-of-work; tracks every object |
| 2 | `Session.execute(insert(Model), rows)` | SQLAlchemy 2.0 ORM bulk insert (`insertmanyvalues`) |
| 3 | ORM bulk insert + engine flags | `fast_executemany` (MSSQL/pyodbc) · `use_insertmanyvalues` (MSSQL/pymssql) · `executemany_mode=values_plus_batch` (psycopg2) · pipeline mode (psycopg3) |
| 4 | `Session.execute(text("INSERT …"), rows)` | Raw SQL; bypasses ORM entirely, hits `cursor.executemany()` directly |

Each strategy is tested against four driver/engine combinations:

- **`tests/mssql/`** — SQL Server 2022 via `pyodbc` + ODBC Driver 18
- **`tests/mssql_pymssql/`** — SQL Server 2022 via `pymssql`
- **`tests/postgres/`** — PostgreSQL 16 via `psycopg2`
- **`tests/psycopg3/`** — PostgreSQL 16 via `psycopg3`

## Project Structure

```
sql-bulk/
├── models.py               # SQLAlchemy ORM model (dbo.AppUser)
├── main.py                 # Quick smoke-test: insert + retrieve one row
├── mssql/                  # MSSQL engine factory (pyodbc)
├── mssql_pymssql/          # MSSQL engine factory (pymssql)
├── postgres/               # PostgreSQL engine factory (psycopg2)
├── psycopg3/               # PostgreSQL engine factory (psycopg3)
├── tests/
│   ├── mssql/              # Bulk insert benchmarks — SQL Server (pyodbc)
│   ├── mssql_pymssql/      # Bulk insert benchmarks — SQL Server (pymssql)
│   ├── postgres/           # Bulk insert benchmarks — PostgreSQL (psycopg2)
│   └── psycopg3/           # Bulk insert benchmarks — PostgreSQL (psycopg3)
├── docs/
│   └── bulk-insert-performance-analysis.md   # Detailed findings
├── docker-compose.yml      # Spins up SQL Server 2022 + PostgreSQL 16
├── init.sql                # Creates dbo.AppUser on SQL Server
├── init_pg.sql             # Creates dbo.AppUser on PostgreSQL
└── .env.example            # Environment variable template
```

## Prerequisites

- **Python 3.13+** and **[uv](https://docs.astral.sh/uv/)**
- **Docker** (for the database containers)
- **ODBC Driver 18 for SQL Server** — [install guide](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server) *(required only for the `mssql/` pyodbc suite)*

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd sql-bulk

# 2. Copy and edit the environment file
cp .env.example .env
# Edit .env if you need non-default passwords or hostnames

# 3. Start the databases
docker compose up -d

# 4. Install Python dependencies
uv sync
```

The Docker containers automatically run `init.sql` / `init_pg.sql` on first start to create the `dbo.AppUser` table.

## Running the Benchmarks

Run all suites:

```bash
uv run pytest -s
```

Run a specific suite:

```bash
uv run pytest tests/mssql         -s   # SQL Server via pyodbc
uv run pytest tests/mssql_pymssql -s   # SQL Server via pymssql
uv run pytest tests/postgres      -s   # PostgreSQL via psycopg2
uv run pytest tests/psycopg3      -s   # PostgreSQL via psycopg3
```

The `-s` flag lets timing output printed by each test appear in the terminal.

Each test suite inserts **50,000 rows** and reports elapsed time per strategy.

## Key Findings

1. **Raw SQL is fastest** — `session.execute(text("INSERT …"), rows)` bypasses the ORM and `OUTPUT INSERTED`, hitting `cursor.executemany()` directly with no overhead.
2. **`fast_executemany` has zero effect on ORM inserts with IDENTITY columns** — SQLAlchemy routes those through `insertmanyvalues` (which calls `cursor.execute()`), so `cursor.executemany()` is never invoked.
3. **NULL values fragment ORM bulk batches** — rows with different combinations of `None` columns are split into separate INSERT batches, significantly increasing round-trips.

Full root-cause analysis and fix recommendations: [`docs/bulk-insert-performance-analysis.md`](docs/bulk-insert-performance-analysis.md).
