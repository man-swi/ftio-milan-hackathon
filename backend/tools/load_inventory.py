import csv

# -----------------------------------
# GLOBAL CACHE
# -----------------------------------

_inventory_cache = []


# -----------------------------------
# INITIALIZE INVENTORY
# -----------------------------------

def initialize_inventory():

    global _inventory_cache

    print("INITIALIZING INVENTORY CACHE...")

    file_path = (
        "backend/data/inventory_sample.csv"
    )

    inventory_data = []

    with open(
        file_path,
        mode="r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            inventory_data.append({

                "sku": row["sku"],

                "product_name":
                row["product_name"],

                "category":
                row["category"],

                "stock":
                int(row["stock"]),

                "unit_price":
                float(row["unit_price"]),

                "sales_velocity":
                row["sales_velocity"]
            })

    _inventory_cache = inventory_data

    print("INVENTORY CACHE READY")

    print(_inventory_cache[:2])


# -----------------------------------
# LOAD INVENTORY
# -----------------------------------

def load_inventory():

    global _inventory_cache

    if not _inventory_cache:

        initialize_inventory()

    return _inventory_cache