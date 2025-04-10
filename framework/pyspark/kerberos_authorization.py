import os
import platform
from pyspark.sql import SparkSession


def kerberos_authorization():
    if platform.system().lower() == "windows":
        print(os.system("where kinit"))
        keytab_path = "D:/document/qzdsf/qzdsf_dev.keytab"
        cache_name = "D:/document/qzdsf/krb5cc_uid"
        os.system(f"kinit -kt {keytab_path} -c {cache_name} qzdsf_dev")
        os.environ["KRB5CCNAME"] = cache_name
        os.system("klist")
