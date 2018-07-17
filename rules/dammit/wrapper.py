"""Snakemake wrapper for Dammit"""

__author__ = "Tessa Pierce"
__copyright__ = "Copyright 2018, Tessa Pierce"
__email__ = "ntpierce@gmail.com"
__license__ = "MIT"

from os import path
from snakemake.shell import shell

# handle database params
db_dir = snakemake.params.get("database_dir")
db_dir = path.abspath(db_dir)
busco_dbs = snakemake.params.get("busco_dbs", "")
db_extra = snakemake.params.get("db_extra", "")
db_only = snakemake.params.get('db_install_only', False)

db_cmd = ' --database-dir ' + db_dir if db_dir is not None else ""
busco_cmd = ' --busco-group '.join(busco_dbs) if busco_dbs is not None else ""
log = snakemake.log_fmt_shell(stdout=True, stderr=True)

# handle annotate params
outdir = path.dirname(snakemake.output[0])
annot_extra = snakemake.params.get("annot_extra", "")

# install databases
shell("dammit databases {db_cmd} {busco_cmd} --install --n_threads {snakemake.threads} {db_extra} {log}")

if not db_only:
# run annotation
    shell("dammit annotate {snakemake.input} {db_cmd} --n_threads {snakemake.threads} --output-dir {outdir} {annot_extra} {log}")
