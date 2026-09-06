# shipment-consolidation-analysis
Data science project for identifying potential shipment consolidation opportunities using order volume, delivery deadlines, and truck capacity.

# Shipment Consolidation Analysis

## Project Overview

This project focuses on identifying potential shipment consolidation opportunities to reduce underutilized delivery trips and improve transportation efficiency.

The analysis uses shipment order volume, delivery deadlines, and truck capacity to identify orders that can potentially be consolidated into the same transportation movement.

## Problem Statement

How can shipment data be analyzed to identify consolidation opportunities among compatible shipments, thereby improving vehicle utilization and logistics efficiency?

## Objectives

- Analyze shipment patterns using Exploratory Data Analysis (EDA).
- Identify orders that can potentially be consolidated.
- Evaluate truck capacity utilization.
- Support better logistics resource allocation.
- Provide a foundation for future optimization.

## Dataset

The project uses a public shipment consolidation dataset containing information about new orders, ongoing orders, order volumes, due dates, truck capacity, transportation costs, and other logistics parameters.

## Methods Used

- Data Loading and Processing
- Exploratory Data Analysis (EDA)
- Rule-based Consolidation Screening
- Capacity Utilization Analysis
- Python and Pandas

## Key Results

- 25 new orders were analyzed.
- 300 capacity-feasible order pairs were identified.
- 142 pairs satisfied both capacity and delivery-date conditions.
- Consolidation opportunity rate: **47.33%**
- 10 non-overlapping consolidation groups were selected.
- 24 out of 25 orders were covered.
- Average theoretical truck-capacity utilization: **68.53%**

## Project Structure

```text
shipment-consolidation-analysis/
├── README.md
├── src/
│   └── load_data.py
└── results/
    └── final_consolidation_summary.csv
