DEFAULT_SQL_PATH = "sqlite:///gates.sqlite"
DEFAULT_GRANTS_TABLE_DESCRP = (
   "This table has fields: GRANT ID, GRANTEE, PURPOSE, DIVISION, DATE COMMITTED, DURATION (MONTHS), AMOUNT COMMITTED, GRANTEE WEBSITE,GRANTEE CITY, GRANTEE STATE, GRANTEE COUNTRY, REGION SERVED,TOPIC for grants from the Gates Foundation."
   "The purpose and topic contain names of diseases such as Malaria, AIDS, Tuberculosis, Cholera, Guinea Worm, COVID, Polio, and HIV. The date is in the format year-month."
   "The DATE COMMITTED has format YYYY-MM."
)

DEFAULT_LC_TOOL_DESCRP = "Useful for when you want to answer queries about grants funded by the Gates Foundation."

DEFAULT_INGEST_DOCUMENT = (
    "There was 1 grants funded by the Gates Foundation in 1994.",
    'Grant INV-016370 went toward to develop shelf-stable, locally-sourced, microbiome-directed, ready-to-use therapeutic foods (MD-RUTFs) for malnourished children.  This grant was awarded $3.4m'
)
