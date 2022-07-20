

def row7_txn_month_config(txn_year):
    if txn_year == "2022":
        return [mon for mon in range(1, 8)]
    else:
        return [mon for mon in range(1, 13)]

    