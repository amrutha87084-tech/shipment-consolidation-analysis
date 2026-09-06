from pathlib import Path
import re

# -------------------------------------------------
# 1. Locate the dataset file
# -------------------------------------------------

file_path = Path(__file__).resolve().parent.parent / "data" / "inst_g2_1.txt"

if not file_path.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{file_path}"
    )

# -------------------------------------------------
# 2. Read the dataset
# -------------------------------------------------

text = file_path.read_text(encoding="utf-8")

# -------------------------------------------------
# 3. Extract a single value
# -------------------------------------------------

def get_scalar(name):
    pattern = rf"{name}\s*=\s*([^;]+);"
    match = re.search(pattern, text)

    if not match:
        raise ValueError(f"{name} was not found in the dataset.")

    return match.group(1).strip()

# -------------------------------------------------
# 4. Extract basic dataset information
# -------------------------------------------------

nb_new_orders = int(get_scalar("NbNewOrders"))
nb_ongoing_orders = int(get_scalar("NbOngoingOrders"))
nb_months = int(get_scalar("NbMonths"))
nb_regions = int(get_scalar("NbRegions"))
nb_trucks = int(get_scalar("NbTrucks"))
truck_capacity = float(get_scalar("TruckCapa"))

# -------------------------------------------------
# 5. Display the information
# -------------------------------------------------

print("\nDATASET INFORMATION")
print("-----------------------------")
print("New orders      :", nb_new_orders)
print("Ongoing orders  :", nb_ongoing_orders)
print("Planning months :", nb_months)
print("Regions         :", nb_regions)
print("Trucks          :", nb_trucks)
print("Truck capacity  :", truck_capacity)
# -------------------------------------------------
# 6. Extract order volumes
# -------------------------------------------------

def get_array(name):
    pattern = rf"{name}\s*=\s*\[([^\]]+)\]\s*;"
    match = re.search(pattern, text)

    if not match:
        raise ValueError(f"{name} was not found in the dataset.")

    values = match.group(1).split()
    return [float(value) for value in values]


new_order_volume = get_array("NewOrderVolume")
ongoing_order_volume = get_array("OngOrderVolume")

print("\nORDER VOLUMES")
print("-----------------------------")
print("New order volumes    :", new_order_volume)
print("Ongoing order volumes:", ongoing_order_volume)

print("\nNumber of new-order values    :", len(new_order_volume))
print("Number of ongoing-order values:", len(ongoing_order_volume))
# -------------------------------------------------
# 7. Extract delivery information
# -------------------------------------------------

# -------------------------------------------------
# 7. Extract delivery information
# -------------------------------------------------

delivery_period = get_array("DeliveryPOord")
new_order_due_date = get_array("NewOrderduedate")

print("\nDELIVERY INFORMATION")
print("-----------------------------")

print("Delivery periods :", delivery_period)
print("Due dates        :", new_order_due_date)

print("\nNumber of delivery-period values :", len(delivery_period))
print("Number of due-date values       :", len(new_order_due_date))
# -------------------------------------------------
# 8. Create a table for new orders
# -------------------------------------------------

import pandas as pd

# -------------------------------------------------
# 8. Create table for NEW orders
# -------------------------------------------------

import pandas as pd

new_orders_df = pd.DataFrame({
    "Order_ID": range(1, len(new_order_volume) + 1),
    "Order_Volume": new_order_volume,
    "Due_Date": new_order_due_date
})

print("\nNEW ORDERS TABLE")
print("-----------------------------")
print(new_orders_df)

print("\nTotal new-order volume:",
      new_orders_df["Order_Volume"].sum())

print("Average new-order volume:",
      new_orders_df["Order_Volume"].mean())

print("Number of new orders:",
      len(new_orders_df))

print("\nNEW ORDERS TABLE")
print("-----------------------------")
print(new_orders_df)

print("\nTotal order volume:",
      new_orders_df["Order_Volume"].sum())

print("Average order volume:",
      new_orders_df["Order_Volume"].mean())
# -------------------------------------------------
# 9. Basic Exploratory Data Analysis (EDA)
# -------------------------------------------------

print("\nBASIC EDA")
print("-----------------------------")

print("\nSummary statistics:")
print(new_orders_df.describe())

print("\nMinimum order volume:",
      new_orders_df["Order_Volume"].min())

print("Maximum order volume:",
      new_orders_df["Order_Volume"].max())

print("Average order volume:",
      new_orders_df["Order_Volume"].mean())

print("Total order volume:",
      new_orders_df["Order_Volume"].sum())
# -------------------------------------------------
# 10. Visualize order volumes
# -------------------------------------------------

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

plt.bar(
    new_orders_df["Order_ID"],
    new_orders_df["Order_Volume"]
)

plt.xlabel("Order ID")
plt.ylabel("Order Volume")
plt.title("Order Volume Distribution")

plt.tight_layout()
plt.show()
# -------------------------------------------------
# 11. Analyze truck capacity
# -------------------------------------------------

truck_capacity = 25000

total_volume = new_orders_df["Order_Volume"].sum()

minimum_trucks = int(
    (total_volume + truck_capacity - 1) // truck_capacity
)

new_orders_df["Volume_Percentage_of_Truck"] = (
    new_orders_df["Order_Volume"] / truck_capacity * 100
)

print("\nTRUCK CAPACITY ANALYSIS")
print("-----------------------------")

print("Truck capacity:", truck_capacity)
print("Total new-order volume:", total_volume)
print("Minimum theoretical trucks required:",
      minimum_trucks)

print("\nOrder volume as % of truck capacity:")
print(
    new_orders_df[
        ["Order_ID", "Order_Volume",
         "Volume_Percentage_of_Truck"]
    ]
)
# -------------------------------------------------
# 12. Identify possible order pairs
# -------------------------------------------------

possible_pairs = []

for i in range(len(new_orders_df)):
    for j in range(i + 1, len(new_orders_df)):

        order_1 = new_orders_df.iloc[i]
        order_2 = new_orders_df.iloc[j]

        combined_volume = (
            order_1["Order_Volume"] +
            order_2["Order_Volume"]
        )

        if combined_volume <= truck_capacity:
            possible_pairs.append({
                "Order_1": int(order_1["Order_ID"]),
                "Order_2": int(order_2["Order_ID"]),
                "Combined_Volume": combined_volume,
                "Remaining_Capacity":
                    truck_capacity - combined_volume
            })

pairs_df = pd.DataFrame(possible_pairs)

print("\nPOTENTIAL CONSOLIDATION PAIRS")
print("-----------------------------")
print("Number of feasible pairs:", len(pairs_df))

print("\nFirst 20 feasible pairs:")
print(pairs_df.head(20))
# -------------------------------------------------
# 13. Apply delivery-date compatibility
# -------------------------------------------------

date_compatible_pairs = []

max_due_date_difference = 1

for i in range(len(new_orders_df)):
    for j in range(i + 1, len(new_orders_df)):

        order_1 = new_orders_df.iloc[i]
        order_2 = new_orders_df.iloc[j]

        combined_volume = (
            order_1["Order_Volume"] +
            order_2["Order_Volume"]
        )

        due_date_difference = abs(
            order_1["Due_Date"] -
            order_2["Due_Date"]
        )

        if (
            combined_volume <= truck_capacity
            and due_date_difference <= max_due_date_difference
        ):
            date_compatible_pairs.append({
                "Order_1": int(order_1["Order_ID"]),
                "Order_2": int(order_2["Order_ID"]),
                "Combined_Volume": combined_volume,
                "Due_Date_1": order_1["Due_Date"],
                "Due_Date_2": order_2["Due_Date"],
                "Due_Date_Difference": due_date_difference,
                "Remaining_Capacity":
                    truck_capacity - combined_volume
            })

compatible_pairs_df = pd.DataFrame(date_compatible_pairs)

print("\nDATE-COMPATIBLE CONSOLIDATION PAIRS")
print("-----------------------------")
print(
    "Number of compatible pairs:",
    len(compatible_pairs_df)
)

print("\nFirst 20 compatible pairs:")
print(compatible_pairs_df.head(20))
# -------------------------------------------------
# 14. Calculate consolidation opportunity rate
# -------------------------------------------------

total_possible_pairs = len(new_orders_df) * (
    len(new_orders_df) - 1
) // 2

compatible_pairs = len(compatible_pairs_df)

consolidation_opportunity_rate = (
    compatible_pairs / total_possible_pairs
) * 100

print("\nCONSOLIDATION OPPORTUNITY KPI")
print("-----------------------------")
print("Total possible order pairs:",
      total_possible_pairs)

print("Capacity-feasible pairs:",
      len(pairs_df))

print("Date-compatible pairs:",
      compatible_pairs)

print("Consolidation opportunity rate:",
      round(consolidation_opportunity_rate, 2), "%")
# -------------------------------------------------
# 15. Create potential consolidation groups
# -------------------------------------------------

from itertools import combinations

consolidation_groups = []

# Maximum number of orders in one group
max_group_size = 3

for group_size in range(2, max_group_size + 1):

    for combination in combinations(
        new_orders_df.index,
        group_size
    ):

        group = new_orders_df.loc[list(combination)]

        total_volume = group["Order_Volume"].sum()

        due_date_range = (
            group["Due_Date"].max()
            - group["Due_Date"].min()
        )

        if (
            total_volume <= truck_capacity
            and due_date_range <= max_due_date_difference
        ):

            consolidation_groups.append({
                "Orders": list(group["Order_ID"]),
                "Number_of_Orders": group_size,
                "Total_Volume": total_volume,
                "Due_Date_Range": due_date_range,
                "Remaining_Capacity":
                    truck_capacity - total_volume
            })

groups_df = pd.DataFrame(consolidation_groups)

print("\nPOTENTIAL CONSOLIDATION GROUPS")
print("-----------------------------")

print(
    "Total potential groups:",
    len(groups_df)
)

print("\nFirst 20 groups:")
print(groups_df.head(20))
# -------------------------------------------------
# 16. Select non-overlapping consolidation groups
# -------------------------------------------------

selected_groups = []
used_orders = set()

# Prefer groups with 3 orders first
groups_sorted = groups_df.sort_values(
    by=["Number_of_Orders", "Total_Volume"],
    ascending=[False, True]
)

for _, group in groups_sorted.iterrows():

    group_orders = set(group["Orders"])

    # Select the group only if none of its orders
    # have already been selected
    if used_orders.isdisjoint(group_orders):

        selected_groups.append(group)
        used_orders.update(group_orders)

selected_groups_df = pd.DataFrame(selected_groups)

print("\nSELECTED NON-OVERLAPPING GROUPS")
print("-----------------------------")

print(
    "Number of selected groups:",
    len(selected_groups_df)
)

print(
    "Number of orders included:",
    len(used_orders)
)

print("\nSelected groups:")
print(selected_groups_df)
# -------------------------------------------------
# 17. Calculate consolidation coverage
# -------------------------------------------------

total_new_orders = len(new_orders_df)

orders_consolidated = len(used_orders)

consolidation_coverage = (
    orders_consolidated / total_new_orders
) * 100

print("\nCONSOLIDATION COVERAGE KPI")
print("-----------------------------")

print("Total new orders:",
      total_new_orders)

print("Orders included in consolidation:",
      orders_consolidated)

print("Orders not included:",
      total_new_orders - orders_consolidated)

print("Consolidation coverage:",
      round(consolidation_coverage, 2), "%")
# -------------------------------------------------
# 18. Calculate consolidation group utilization
# -------------------------------------------------

selected_groups_df["Capacity_Utilization"] = (
    selected_groups_df["Total_Volume"]
    / truck_capacity
) * 100

print("\nCONSOLIDATION GROUP UTILIZATION")
print("-----------------------------")

print(
    selected_groups_df[
        [
            "Orders",
            "Number_of_Orders",
            "Total_Volume",
            "Remaining_Capacity",
            "Capacity_Utilization"
        ]
    ]
)

print("\nAverage group capacity utilization:",
      round(
          selected_groups_df["Capacity_Utilization"].mean(), 2
      ),
      "%")
# -------------------------------------------------
# 19. Analyze due-date distribution
# -------------------------------------------------

due_date_counts = new_orders_df["Due_Date"].value_counts().sort_index()

print("\nDUE-DATE DISTRIBUTION")
print("-----------------------------")
print(due_date_counts)

print("\nNumber of orders by due date:")
for date, count in due_date_counts.items():
    print(f"Due date {int(date)}: {count} orders")
    # -------------------------------------------------
# 20. Visualize due-date distribution
# -------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    due_date_counts.index.astype(int),
    due_date_counts.values
)

plt.xlabel("Due Date")
plt.ylabel("Number of Orders")
plt.title("Distribution of New Orders by Due Date")

plt.xticks(due_date_counts.index.astype(int))

plt.tight_layout()
plt.show()
# -------------------------------------------------
# 21. Analyze order volume by due date
# -------------------------------------------------

volume_by_due_date = (
    new_orders_df
    .groupby("Due_Date")["Order_Volume"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

print("\nORDER VOLUME BY DUE DATE")
print("-----------------------------")
print(volume_by_due_date)
# -------------------------------------------------
# 22. Identify high-volume orders
# -------------------------------------------------

median_volume = new_orders_df["Order_Volume"].median()

new_orders_df["Volume_Category"] = new_orders_df[
    "Order_Volume"
].apply(
    lambda x: "High Volume"
    if x >= median_volume
    else "Lower Volume"
)

print("\nORDER VOLUME CATEGORIES")
print("-----------------------------")

print("Median order volume:",
      median_volume)

print("\nOrders by category:")
print(
    new_orders_df[
        ["Order_ID", "Order_Volume",
         "Due_Date", "Volume_Category"]
    ]
)

print("\nCategory counts:")
print(
    new_orders_df["Volume_Category"].value_counts()
)
# -------------------------------------------------
# 23. Rank consolidation groups
# -------------------------------------------------

selected_groups_df["Capacity_Utilization"] = (
    selected_groups_df["Total_Volume"]
    / truck_capacity
) * 100

selected_groups_df["Priority_Score"] = (
    selected_groups_df["Capacity_Utilization"]
    + (selected_groups_df["Number_of_Orders"] * 10)
)

ranked_groups_df = selected_groups_df.sort_values(
    by="Priority_Score",
    ascending=False
)

print("\nTOP CONSOLIDATION GROUPS")
print("-----------------------------")

print(
    ranked_groups_df[
        [
            "Orders",
            "Number_of_Orders",
            "Total_Volume",
            "Due_Date_Range",
            "Capacity_Utilization",
            "Priority_Score"
        ]
    ]
)
# -------------------------------------------------
# 24. Final consolidation summary
# -------------------------------------------------

final_summary = ranked_groups_df[
    [
        "Orders",
        "Number_of_Orders",
        "Total_Volume",
        "Remaining_Capacity",
        "Capacity_Utilization",
        "Due_Date_Range"
    ]
].copy()

final_summary = final_summary.reset_index(drop=True)

final_summary.index = final_summary.index + 1

print("\nFINAL CONSOLIDATION SUMMARY")
print("-----------------------------")
print(final_summary)

print("\nTotal selected groups:",
      len(final_summary))

print("Total orders covered:",
      final_summary["Number_of_Orders"].sum())

print("Average capacity utilization:",
      round(
          final_summary["Capacity_Utilization"].mean(), 2
      ), "%")
# -------------------------------------------------
# 25. Save final results
# -------------------------------------------------

output_path = Path(__file__).resolve().parent.parent / "results" / "final_consolidation_summary.csv"

final_summary.to_csv(output_path, index=False)

print("\nRESULT FILE SAVED")
print("-----------------------------")
print("Saved to:", output_path)
# -------------------------------------------------
# 26. Visualize consolidation group utilization
# -------------------------------------------------

plt.figure(figsize=(10, 5))

group_labels = [
    f"Group {i}"
    for i in range(1, len(final_summary) + 1)
]

plt.bar(
    group_labels,
    final_summary["Capacity_Utilization"]
)

plt.xlabel("Consolidation Group")
plt.ylabel("Capacity Utilization (%)")
plt.title("Truck Capacity Utilization by Consolidation Group")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()