DEFAULT_SQL_PATH = "sqlite:///gates.sqlite"
DEFAULT_GRANTS_TABLE_DESCRP = (
   "This table has fields: ID, grantee, purpose, division, date, duration, amount, website, city, state, country, region, and topic for grants from the Gates Foundation."
   "The purpose and topic contain names of diseases such as Malaria, AIDS, Tuberculosis, Cholera, Guinea Worm, COVID, Polio, and HIV. The date is in the format year-month."
   "The first 4 digits of the date are the year and the last 2 digits are the month."
)

DEFAULT_LC_TOOL_DESCRP = "Useful for when you want to answer queries about grants funded by the Gates Foundation."

DEFAULT_INGEST_DOCUMENT = (
    "There was 1 grants funded by the Gates Foundation in 1994.",
    'Grant INV-016370 went toward to develop shelf-stable, locally-sourced, microbiome-directed, ready-to-use therapeutic foods (MD-RUTFs) for malnourished children.  This grant was awarded $3.4m'
)
