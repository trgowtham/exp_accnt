#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def process_file(ts_file):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(ts_file, sep='\t')

    # Define subcategories of interest
    subcategories = ["Education", "Food", "Grocery", "Health", "Lifestyle", "Misc", "Shopping", "Travel", "Utility"]

    df['Subcategory'] = df['Category'].where(df['Category'].isin(subcategories), 'Misc')

    # Group by subcategory and sum amounts
    subcategory_data = df.groupby('Subcategory')['Amount'].sum()

    # Define category mapping
    def map_category(account):
        if account == 'self-card':
            return 'Self Card'
        elif account == 'self-cash':
            return 'Self Cash'
        elif 'cash' in account:
            return 'Not Self Cash'
        elif 'card' in account:
            return 'Not Self Card'
        return 'Other'

    df['Mapped Category'] = df['Account'].apply(map_category)

    # Group by mapped category and sum amounts
    category_data = df.groupby('Mapped Category')['Amount'].sum()

    # Get top 10 expenses
    top_expenses = df[['Note', 'Amount']].sort_values(by='Amount', ascending=False).head(10)

    # Total expenses
    total_expense = df['Amount'].sum()

    # Function to display amounts along with percentages
    def func(pct, all_vals):
        absolute = int(round(pct/100.*sum(all_vals)))
        return "{:.1f}%\n({})".format(pct, absolute)

    # Plot the pie charts
    fig, axes = plt.subplots(1, 3, figsize=(18, 8), gridspec_kw={'width_ratios': [2, 2, 1]})
    fig.suptitle(f'Expense Report: {ts_file}', fontsize=16, fontweight='bold')

    # Pie chart for Subcategories (without labels, amounts)
    colors = plt.cm.Paired.colors
    axes[0].pie(subcategory_data, colors=colors, startangle=140)
    axes[0].set_title('Expense Distribution by Subcategory')

    # Legend for Subcategory chart (sorted by amount)
    sorted_subcategories = subcategory_data.sort_values(ascending=False)
    legend_labels = [f"{sub}: {amt} ({amt/sum(subcategory_data)*100:.1f}%)" for sub, amt in sorted_subcategories.items()]
    axes[0].legend(legend_labels, loc='center left', bbox_to_anchor=(-0.4, 0.5), fontsize=10)

    # Pie chart for Categories
    axes[1].pie(category_data, labels=category_data.index, autopct=lambda pct: func(pct, category_data), startangle=140)
    axes[1].set_title('Expense Distribution by Account Category')

    # Display top 10 expenses as a table
    axes[2].axis('off')
    table_data = [[note, amt] for note, amt in zip(top_expenses['Note'], top_expenses['Amount'])]
    table = axes[2].table(cellText=table_data, colLabels=["Note", "Amount"], loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    axes[2].set_title("Top 10 Expenses")

    # Add total expenses at the bottom
    fig.text(0.5, 0.02, f'Total Expenses: {total_expense} INR', ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Save image with same name as input file but with .jpeg extension
    filename = os.path.basename(ts_file)
    output_filename = "jpeg/" + os.path.splitext(filename)[0] + ".jpeg"
    plt.savefig(output_filename, format="jpeg")
    plt.close()

# Get file names from command line arguments
if len(sys.argv) < 2:
    print("Usage: plot_pie.py <tsv_filename1> <tsv_filename2> ...")
    sys.exit(1)

for file in sys.argv[1:]:
    process_file(file)

