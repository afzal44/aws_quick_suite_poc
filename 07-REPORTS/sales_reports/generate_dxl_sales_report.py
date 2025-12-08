"""
DXL Annual Sales Report Generator
Generates a comprehensive PDF sales report for AWS Quick Suite analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (11, 8.5)  # Letter size

class DXLSalesReportGenerator:
    def __init__(self, data_path="poc_data_generators"):
        self.data_path = data_path
        self.report_year = 2024

    def load_data(self):
        """Load all necessary data files"""
        print("Loading data files...")

        # Load transaction data
        self.transactions = pd.read_csv(f"{self.data_path}/transaction_header.csv", encoding='utf-8-sig')
        self.transaction_details = pd.read_csv(f"{self.data_path}/transaction_detail.csv", encoding='utf-8-sig')

        # Load order data
        self.orders = pd.read_csv(f"{self.data_path}/orderheader.csv", encoding='utf-8-sig')
        self.orderlines = pd.read_csv(f"{self.data_path}/orderline.csv", encoding='utf-8-sig')

        # Load customer and store data
        self.customers = pd.read_csv(f"{self.data_path}/customer.csv", encoding='utf-8-sig')
        self.stores = pd.read_csv(f"{self.data_path}/store.csv", encoding='utf-8-sig')

        print(f"[OK] Loaded {len(self.transactions):,} transactions")
        print(f"[OK] Loaded {len(self.orders):,} orders")
        print(f"[OK] Loaded {len(self.customers):,} customers")
        print(f"[OK] Loaded {len(self.stores):,} stores")

    def prepare_data(self):
        """Prepare and clean data for analysis"""
        print("\nPreparing data for analysis...")

        # Parse dates in transactions
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'], format='%d-%m-%Y %H:%M', errors='coerce')
        self.transactions['year'] = self.transactions['transaction_date'].dt.year
        self.transactions['month'] = self.transactions['transaction_date'].dt.month
        self.transactions['quarter'] = self.transactions['transaction_date'].dt.quarter

        # Parse dates in orders
        self.orders['createdtimestamp'] = pd.to_datetime(self.orders['createdtimestamp'])
        self.orders['year'] = self.orders['createdtimestamp'].dt.year
        self.orders['month'] = self.orders['createdtimestamp'].dt.month
        self.orders['quarter'] = self.orders['createdtimestamp'].dt.quarter

        # Filter for report year (2024)
        self.transactions_2024 = self.transactions[self.transactions['year'] == self.report_year].copy()
        self.orders_2024 = self.orders[self.orders['year'] == self.report_year].copy()

        # Merge transaction details
        self.trans_detailed = pd.merge(
            self.transactions_2024,
            self.transaction_details,
            on='transaction_id',
            how='left'
        )

        # Merge order details
        self.orders_detailed = pd.merge(
            self.orders_2024,
            self.orderlines,
            on='orderid',
            how='left'
        )

        print(f"[OK] Filtered {len(self.transactions_2024):,} transactions for {self.report_year}")
        print(f"[OK] Filtered {len(self.orders_2024):,} orders for {self.report_year}")

    def calculate_metrics(self):
        """Calculate key business metrics"""
        print("\nCalculating business metrics...")

        self.metrics = {
            # Revenue Metrics
            'total_revenue': self.transactions_2024['total_net_retail'].sum(),
            'total_transactions': len(self.transactions_2024),
            'avg_transaction_value': self.transactions_2024['total_net_retail'].mean(),

            # Order Metrics
            'total_orders': len(self.orders_2024),
            'total_order_value': self.orders_detailed['orderlinetotal'].sum(),
            'avg_order_value': self.orders_detailed.groupby('orderid')['orderlinetotal'].sum().mean(),

            # Customer Metrics
            'unique_customers': self.transactions_2024['customer_id'].nunique(),
            'active_stores': self.transactions_2024['store_no'].nunique(),

            # Product Metrics
            'total_items_sold': self.trans_detailed['quantity'].sum(),
            'avg_items_per_transaction': self.trans_detailed.groupby('transaction_id')['quantity'].sum().mean(),

            # Profit Metrics
            'total_cost': self.trans_detailed['cost'].sum(),
            'total_markdown': self.trans_detailed['markdown_amount'].sum(),
            'gross_margin': None,  # Will calculate
        }

        # Calculate gross margin
        revenue = self.trans_detailed['net_retail'].sum()
        cost = self.trans_detailed['cost'].sum()
        self.metrics['gross_margin'] = ((revenue - cost) / revenue * 100) if revenue > 0 else 0

        print("[OK] Metrics calculated successfully")

    def generate_pdf(self, output_file="DXL_Sales_Report_2024.pdf"):
        """Generate comprehensive PDF report"""
        print(f"\nGenerating PDF report: {output_file}")

        with PdfPages(output_file) as pdf:
            # Page 1: Cover Page
            self._create_cover_page(pdf)

            # Page 2: Executive Summary
            self._create_executive_summary(pdf)

            # Page 3: Revenue Analysis
            self._create_revenue_analysis(pdf)

            # Page 4: Sales Channel Performance
            self._create_channel_analysis(pdf)

            # Page 5: Customer Analytics
            self._create_customer_analysis(pdf)

            # Page 6: Product Performance
            self._create_product_analysis(pdf)

            # Page 7: Store Performance
            self._create_store_analysis(pdf)

            # Page 8: Payment & Fulfillment Analysis
            self._create_payment_fulfillment_analysis(pdf)

            # Page 9: Trends & Seasonality
            self._create_trends_analysis(pdf)

            # Page 10: Recommendations for 2025
            self._create_recommendations(pdf)

        print(f"[OK] PDF report generated: {output_file}")

    def _create_cover_page(self, pdf):
        """Create cover page"""
        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Company branding
        ax.text(0.5, 0.85, 'DXL', ha='center', va='center', fontsize=72, fontweight='bold', color='#003366')
        ax.text(0.5, 0.75, 'Destination XL Group', ha='center', va='center', fontsize=28, color='#666666')

        # Report title
        ax.text(0.5, 0.55, 'Annual Sales Report', ha='center', va='center', fontsize=42, fontweight='bold')
        ax.text(0.5, 0.47, f'Fiscal Year {self.report_year}', ha='center', va='center', fontsize=32, color='#333333')

        # Subtitle
        ax.text(0.5, 0.35, 'Comprehensive Sales Analysis & Strategic Insights', ha='center', va='center',
                fontsize=18, style='italic', color='#666666')

        # Footer
        ax.text(0.5, 0.15, f'Generated: {datetime.now().strftime("%B %d, %Y")}',
                ha='center', va='center', fontsize=14, color='#999999')
        ax.text(0.5, 0.1, 'Prepared for AWS Quick Suite AI Analysis',
                ha='center', va='center', fontsize=12, color='#999999')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_executive_summary(self, pdf):
        """Create executive summary page"""
        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.95, 'Executive Summary', ha='center', va='top', fontsize=28, fontweight='bold')
        ax.text(0.5, 0.90, f'DXL Sales Performance - {self.report_year}', ha='center', va='top', fontsize=16, color='#666666')

        # Key metrics in boxes
        metrics_data = [
            ('Total Revenue', f"${self.metrics['total_revenue']:,.0f}", '#2E7D32'),
            ('Total Transactions', f"{self.metrics['total_transactions']:,}", '#1565C0'),
            ('Avg Transaction', f"${self.metrics['avg_transaction_value']:,.2f}", '#F57C00'),
            ('Total Orders', f"{self.metrics['total_orders']:,}", '#6A1B9A'),
            ('Active Customers', f"{self.metrics['unique_customers']:,}", '#C62828'),
            ('Gross Margin', f"{self.metrics['gross_margin']:.1f}%", '#00838F'),
        ]

        y_start = 0.75
        col_width = 0.3
        row_height = 0.15

        for idx, (label, value, color) in enumerate(metrics_data):
            row = idx // 2
            col = idx % 2
            x = 0.2 + col * 0.45
            y = y_start - row * row_height

            # Box
            box = plt.Rectangle((x - col_width/2, y - 0.06), col_width, 0.1,
                                facecolor=color, alpha=0.1, edgecolor=color, linewidth=2)
            ax.add_patch(box)

            # Text
            ax.text(x, y + 0.02, label, ha='center', va='center', fontsize=12, color='#333333', fontweight='bold')
            ax.text(x, y - 0.02, value, ha='center', va='center', fontsize=18, color=color, fontweight='bold')

        # Strategic highlights
        y_highlights = 0.25
        ax.text(0.05, y_highlights, 'Key Highlights:', fontsize=14, fontweight='bold', va='top')

        highlights = [
            f"• Processed {self.metrics['total_transactions']:,} transactions across {self.metrics['active_stores']} store locations",
            f"• Served {self.metrics['unique_customers']:,} unique customers with personalized big & tall apparel",
            f"• Average transaction value: ${self.metrics['avg_transaction_value']:,.2f}",
            f"• Total items sold: {self.metrics['total_items_sold']:,.0f} units",
            f"• Gross margin maintained at {self.metrics['gross_margin']:.1f}%",
            f"• Multi-channel operations: In-Store, E-Commerce, Mobile, and Call Center"
        ]

        y_pos = y_highlights - 0.03
        for highlight in highlights:
            ax.text(0.05, y_pos, highlight, fontsize=11, va='top', color='#333333')
            y_pos -= 0.03

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_revenue_analysis(self, pdf):
        """Create revenue analysis visualizations"""
        fig = plt.figure(figsize=(11, 8.5))

        # Title
        fig.suptitle('Revenue Analysis - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Monthly revenue trend
        ax1 = plt.subplot(2, 2, 1)
        monthly_revenue = self.transactions_2024.groupby('month')['total_net_retail'].sum()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax1.plot(monthly_revenue.index, monthly_revenue.values, marker='o', linewidth=2, color='#1565C0', markersize=8)
        ax1.set_xlabel('Month', fontsize=10)
        ax1.set_ylabel('Revenue ($)', fontsize=10)
        ax1.set_title('Monthly Revenue Trend', fontsize=12, fontweight='bold')
        ax1.set_xticks(range(1, 13))
        ax1.set_xticklabels(months, rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

        # Quarterly revenue
        ax2 = plt.subplot(2, 2, 2)
        quarterly_revenue = self.transactions_2024.groupby('quarter')['total_net_retail'].sum()
        colors = ['#2E7D32', '#1565C0', '#F57C00', '#C62828']
        bars = ax2.bar(quarterly_revenue.index, quarterly_revenue.values, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Quarter', fontsize=10)
        ax2.set_ylabel('Revenue ($)', fontsize=10)
        ax2.set_title('Quarterly Revenue Distribution', fontsize=12, fontweight='bold')
        ax2.set_xticks([1, 2, 3, 4])
        ax2.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height/1000:.0f}K',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Revenue by tender type
        ax3 = plt.subplot(2, 2, 3)
        tender_revenue = self.transactions_2024.groupby('tender_type')['total_net_retail'].sum().sort_values(ascending=True)
        ax3.barh(tender_revenue.index, tender_revenue.values, color='#00838F', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Revenue ($)', fontsize=10)
        ax3.set_title('Revenue by Payment Method', fontsize=12, fontweight='bold')
        ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax3.grid(True, alpha=0.3, axis='x')

        # Transaction count by month
        ax4 = plt.subplot(2, 2, 4)
        monthly_transactions = self.transactions_2024.groupby('month').size()
        ax4.bar(monthly_transactions.index, monthly_transactions.values, color='#6A1B9A', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Month', fontsize=10)
        ax4.set_ylabel('Transaction Count', fontsize=10)
        ax4.set_title('Monthly Transaction Volume', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(1, 13))
        ax4.set_xticklabels(months, rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_channel_analysis(self, pdf):
        """Create sales channel analysis"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Sales Channel Performance - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Orders by channel
        ax1 = plt.subplot(2, 2, 1)
        channel_orders = self.orders_2024.groupby('order_source').size().sort_values(ascending=False)
        ax1.bar(range(len(channel_orders)), channel_orders.values, color='#1565C0', alpha=0.7, edgecolor='black')
        ax1.set_xticks(range(len(channel_orders)))
        ax1.set_xticklabels(channel_orders.index, rotation=45, ha='right')
        ax1.set_ylabel('Number of Orders', fontsize=10)
        ax1.set_title('Orders by Channel', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')

        # Orders by device type
        ax2 = plt.subplot(2, 2, 2)
        device_orders = self.orders_2024.groupby('device_type').size()
        colors_device = ['#2E7D32', '#F57C00', '#C62828', '#6A1B9A']
        wedges, texts, autotexts = ax2.pie(device_orders.values, labels=device_orders.index, autopct='%1.1f%%',
                                           colors=colors_device, startangle=90)
        ax2.set_title('Orders by Device Type', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Customer type distribution
        ax3 = plt.subplot(2, 2, 3)
        customer_type = self.orders_2024.groupby('customer_type').size()
        colors_cust = ['#00838F', '#D32F2F', '#7B1FA2', '#F57F17']
        ax3.bar(range(len(customer_type)), customer_type.values, color=colors_cust, alpha=0.7, edgecolor='black')
        ax3.set_xticks(range(len(customer_type)))
        ax3.set_xticklabels(customer_type.index, rotation=45, ha='right')
        ax3.set_ylabel('Number of Orders', fontsize=10)
        ax3.set_title('Orders by Customer Type', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')

        # Shipping method preference
        ax4 = plt.subplot(2, 2, 4)
        shipping = self.orders_2024.groupby('shipping_method').size().sort_values(ascending=True)
        ax4.barh(shipping.index, shipping.values, color='#F57C00', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Number of Orders', fontsize=10)
        ax4.set_title('Shipping Method Preference', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_customer_analysis(self, pdf):
        """Create customer analytics page"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Customer Analytics - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Customer segmentation
        ax1 = plt.subplot(2, 2, 1)
        segmentation = self.customers['segmentation_value_a'].value_counts()
        colors_seg = ['#FFD700', '#C0C0C0', '#CD7F32', '#4169E1']
        wedges, texts, autotexts = ax1.pie(segmentation.values, labels=segmentation.index, autopct='%1.1f%%',
                                           colors=colors_seg, startangle=90)
        ax1.set_title('Customer Tier Distribution', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Customer status
        ax2 = plt.subplot(2, 2, 2)
        activity_status = self.customers['segmentation_value_c'].value_counts()
        ax2.bar(range(len(activity_status)), activity_status.values,
               color=['#2E7D32', '#F57C00', '#C62828'], alpha=0.7, edgecolor='black')
        ax2.set_xticks(range(len(activity_status)))
        ax2.set_xticklabels(activity_status.index, rotation=45, ha='right')
        ax2.set_ylabel('Number of Customers', fontsize=10)
        ax2.set_title('Customer Activity Status', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        # Gender distribution
        ax3 = plt.subplot(2, 2, 3)
        gender = self.customers['gender'].value_counts()
        ax3.bar(gender.index, gender.values, color=['#1565C0', '#C2185B'], alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Gender', fontsize=10)
        ax3.set_ylabel('Number of Customers', fontsize=10)
        ax3.set_title('Customer Gender Distribution', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')

        # Marital status
        ax4 = plt.subplot(2, 2, 4)
        marital = self.customers['marital_status'].value_counts()
        ax4.bar(range(len(marital)), marital.values, color='#6A1B9A', alpha=0.7, edgecolor='black')
        ax4.set_xticks(range(len(marital)))
        ax4.set_xticklabels(marital.index)
        ax4.set_ylabel('Number of Customers', fontsize=10)
        ax4.set_title('Marital Status Distribution', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_product_analysis(self, pdf):
        """Create product performance analysis"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Product Performance Analysis - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Top 10 sizes by quantity
        ax1 = plt.subplot(2, 2, 1)
        top_sizes = self.trans_detailed.groupby('size_description')['quantity'].sum().sort_values(ascending=False).head(10)
        ax1.barh(range(len(top_sizes)), top_sizes.values, color='#00838F', alpha=0.7, edgecolor='black')
        ax1.set_yticks(range(len(top_sizes)))
        ax1.set_yticklabels(top_sizes.index)
        ax1.set_xlabel('Quantity Sold', fontsize=10)
        ax1.set_title('Top 10 Sizes by Volume', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.invert_yaxis()

        # Markdown analysis
        ax2 = plt.subplot(2, 2, 2)
        markdown_dist = self.trans_detailed.groupby('markdown_percent')['quantity'].sum().sort_index()
        ax2.bar(markdown_dist.index, markdown_dist.values, color='#D32F2F', alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Markdown %', fontsize=10)
        ax2.set_ylabel('Quantity Sold', fontsize=10)
        ax2.set_title('Sales by Markdown Percentage', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        # Promotion flag impact
        ax3 = plt.subplot(2, 2, 3)
        promo_sales = self.trans_detailed.groupby('promotion_flag')['net_retail'].sum()
        labels = ['Non-Promotional', 'Promotional']
        colors_promo = ['#1565C0', '#F57C00']
        wedges, texts, autotexts = ax3.pie(promo_sales.values, labels=labels, autopct='%1.1f%%',
                                           colors=colors_promo, startangle=90)
        ax3.set_title('Sales: Promotional vs Non-Promotional', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Average selling price by markdown
        ax4 = plt.subplot(2, 2, 4)
        avg_price_markdown = self.trans_detailed.groupby('markdown_percent')['net_retail'].mean()
        ax4.plot(avg_price_markdown.index, avg_price_markdown.values, marker='o',
                linewidth=2, color='#2E7D32', markersize=8)
        ax4.set_xlabel('Markdown %', fontsize=10)
        ax4.set_ylabel('Average Price ($)', fontsize=10)
        ax4.set_title('Average Selling Price by Markdown', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_store_analysis(self, pdf):
        """Create store performance analysis"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Store Performance Analysis - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Top 10 stores by revenue
        ax1 = plt.subplot(2, 2, 1)
        store_revenue = self.transactions_2024.groupby('store_no')['total_net_retail'].sum().sort_values(ascending=False).head(10)
        ax1.barh(range(len(store_revenue)), store_revenue.values, color='#1565C0', alpha=0.7, edgecolor='black')
        ax1.set_yticks(range(len(store_revenue)))
        ax1.set_yticklabels([f"Store {s}" for s in store_revenue.index])
        ax1.set_xlabel('Revenue ($)', fontsize=10)
        ax1.set_title('Top 10 Stores by Revenue', fontsize=12, fontweight='bold')
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.invert_yaxis()

        # Top 10 stores by transaction count
        ax2 = plt.subplot(2, 2, 2)
        store_transactions = self.transactions_2024.groupby('store_no').size().sort_values(ascending=False).head(10)
        ax2.bar(range(len(store_transactions)), store_transactions.values, color='#F57C00', alpha=0.7, edgecolor='black')
        ax2.set_xticks(range(len(store_transactions)))
        ax2.set_xticklabels([f"S{s}" for s in store_transactions.index], rotation=45, ha='right')
        ax2.set_ylabel('Number of Transactions', fontsize=10)
        ax2.set_title('Top 10 Stores by Transaction Volume', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        # Average transaction value by store (top 10)
        ax3 = plt.subplot(2, 2, 3)
        avg_store_value = self.transactions_2024.groupby('store_no')['total_net_retail'].mean().sort_values(ascending=False).head(10)
        ax3.barh(range(len(avg_store_value)), avg_store_value.values, color='#2E7D32', alpha=0.7, edgecolor='black')
        ax3.set_yticks(range(len(avg_store_value)))
        ax3.set_yticklabels([f"Store {s}" for s in avg_store_value.index])
        ax3.set_xlabel('Average Transaction ($)', fontsize=10)
        ax3.set_title('Top 10 Stores by Avg Transaction Value', fontsize=12, fontweight='bold')
        ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.0f}'))
        ax3.grid(True, alpha=0.3, axis='x')
        ax3.invert_yaxis()

        # Store channel distribution
        ax4 = plt.subplot(2, 2, 4)
        if 'sales_channel_code' in self.transactions_2024.columns:
            # Use actual channel data if available
            channel_dist = self.transactions_2024['sales_channel_code'].value_counts()
        else:
            # Fallback: distinguish between web stores and physical stores
            web_stores = [1, 2]  # REPP CATALOG and REPP E-COMMERCE
            store_types = ['Web' if s in web_stores else 'Store' for s in self.transactions_2024['store_no']]
            channel_dist = pd.Series(store_types).value_counts()

        colors_channel = ['#6A1B9A', '#00838F']
        ax4.bar(range(len(channel_dist)), channel_dist.values, color=colors_channel, alpha=0.7, edgecolor='black')
        ax4.set_xticks(range(len(channel_dist)))
        ax4.set_xticklabels(channel_dist.index)
        ax4.set_ylabel('Number of Transactions', fontsize=10)
        ax4.set_title('Channel Distribution', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_payment_fulfillment_analysis(self, pdf):
        """Create payment and fulfillment analysis"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Payment & Fulfillment Analysis - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Payment method preference
        ax1 = plt.subplot(2, 2, 1)
        payment_methods = self.orders_2024.groupby('payment_method').size().sort_values(ascending=False)
        ax1.bar(range(len(payment_methods)), payment_methods.values,
               color=['#1565C0', '#F57C00', '#2E7D32', '#C62828', '#6A1B9A'], alpha=0.7, edgecolor='black')
        ax1.set_xticks(range(len(payment_methods)))
        ax1.set_xticklabels(payment_methods.index, rotation=45, ha='right')
        ax1.set_ylabel('Number of Orders', fontsize=10)
        ax1.set_title('Payment Method Distribution', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')

        # Fulfillment status
        ax2 = plt.subplot(2, 2, 2)
        fulfillment = self.orders_2024.groupby('fulfillmentstatus').size()
        colors_fulfill = ['#2E7D32', '#F57C00', '#C62828', '#1565C0', '#6A1B9A']
        wedges, texts, autotexts = ax2.pie(fulfillment.values, labels=fulfillment.index, autopct='%1.1f%%',
                                           colors=colors_fulfill, startangle=90)
        ax2.set_title('Order Fulfillment Status', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Cancellation rate by source
        ax3 = plt.subplot(2, 2, 3)
        cancel_by_source = self.orders_2024.groupby('order_source')['iscancelled'].apply(
            lambda x: (x == True).sum() / len(x) * 100
        ).sort_values(ascending=True)
        ax3.barh(cancel_by_source.index, cancel_by_source.values, color='#D32F2F', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Cancellation Rate (%)', fontsize=10)
        ax3.set_title('Cancellation Rate by Order Source', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')

        # UTM campaign performance
        ax4 = plt.subplot(2, 2, 4)
        campaign_orders = self.orders_2024.groupby('utmcampaign').size().sort_values(ascending=False).head(8)
        ax4.bar(range(len(campaign_orders)), campaign_orders.values, color='#00838F', alpha=0.7, edgecolor='black')
        ax4.set_xticks(range(len(campaign_orders)))
        ax4.set_xticklabels(campaign_orders.index, rotation=45, ha='right')
        ax4.set_ylabel('Number of Orders', fontsize=10)
        ax4.set_title('Top Marketing Campaigns', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_trends_analysis(self, pdf):
        """Create trends and seasonality analysis"""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Trends & Seasonality Analysis - 2024', fontsize=20, fontweight='bold', y=0.98)

        # Daily transaction trend (sample)
        ax1 = plt.subplot(2, 2, 1)
        daily_trans = self.transactions_2024.groupby(self.transactions_2024['transaction_date'].dt.date).size()
        if len(daily_trans) > 90:
            daily_trans = daily_trans.iloc[-90:]  # Last 90 days
        ax1.plot(range(len(daily_trans)), daily_trans.values, linewidth=1.5, color='#1565C0', alpha=0.7)
        ax1.fill_between(range(len(daily_trans)), daily_trans.values, alpha=0.3, color='#1565C0')
        ax1.set_xlabel('Days', fontsize=10)
        ax1.set_ylabel('Transaction Count', fontsize=10)
        ax1.set_title('Daily Transaction Trend (Last 90 Days)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Monthly growth rate
        ax2 = plt.subplot(2, 2, 2)
        monthly_rev = self.transactions_2024.groupby('month')['total_net_retail'].sum()
        growth_rate = monthly_rev.pct_change() * 100
        colors_growth = ['#2E7D32' if x > 0 else '#C62828' for x in growth_rate.values]
        ax2.bar(growth_rate.index, growth_rate.values, color=colors_growth, alpha=0.7, edgecolor='black')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Month', fontsize=10)
        ax2.set_ylabel('Growth Rate (%)', fontsize=10)
        ax2.set_title('Month-over-Month Revenue Growth', fontsize=12, fontweight='bold')
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax2.set_xticks(range(1, 13))
        ax2.set_xticklabels(months, rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')

        # Revenue vs Cost trend
        ax3 = plt.subplot(2, 2, 3)
        monthly_rev_cost = self.trans_detailed.groupby(
            self.trans_detailed['transaction_date'].dt.month
        ).agg({'net_retail': 'sum', 'cost': 'sum'})
        ax3.plot(monthly_rev_cost.index, monthly_rev_cost['net_retail'].values,
                marker='o', linewidth=2, label='Revenue', color='#2E7D32', markersize=6)
        ax3.plot(monthly_rev_cost.index, monthly_rev_cost['cost'].values,
                marker='s', linewidth=2, label='Cost', color='#C62828', markersize=6)
        ax3.set_xlabel('Month', fontsize=10)
        ax3.set_ylabel('Amount ($)', fontsize=10)
        ax3.set_title('Revenue vs Cost Trend', fontsize=12, fontweight='bold')
        ax3.legend(loc='best')
        ax3.set_xticks(range(1, 13))
        ax3.set_xticklabels(months, rotation=45)
        ax3.grid(True, alpha=0.3)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

        # Quarterly performance comparison
        ax4 = plt.subplot(2, 2, 4)
        quarterly_metrics = self.transactions_2024.groupby('quarter').agg({
            'total_net_retail': 'sum',
            'transaction_id': 'count'
        })
        x = np.arange(len(quarterly_metrics))
        width = 0.35
        ax4_twin = ax4.twinx()

        bars1 = ax4.bar(x - width/2, quarterly_metrics['total_net_retail'].values, width,
                       label='Revenue', color='#1565C0', alpha=0.7, edgecolor='black')
        bars2 = ax4_twin.bar(x + width/2, quarterly_metrics['transaction_id'].values, width,
                            label='Transactions', color='#F57C00', alpha=0.7, edgecolor='black')

        ax4.set_xlabel('Quarter', fontsize=10)
        ax4.set_ylabel('Revenue ($)', fontsize=10, color='#1565C0')
        ax4_twin.set_ylabel('Transaction Count', fontsize=10, color='#F57C00')
        ax4.set_title('Quarterly Performance Metrics', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
        ax4.tick_params(axis='y', labelcolor='#1565C0')
        ax4_twin.tick_params(axis='y', labelcolor='#F57C00')
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_recommendations(self, pdf):
        """Create recommendations page for 2025"""
        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.95, 'Strategic Recommendations for 2025', ha='center', va='top',
               fontsize=24, fontweight='bold')
        ax.text(0.5, 0.90, 'Data-Driven Insights for Growth', ha='center', va='top',
               fontsize=14, color='#666666', style='italic')

        # Recommendations sections
        y_pos = 0.82

        sections = [
            {
                'title': '1. Customer Experience Optimization',
                'points': [
                    '• Focus on VIP and Loyalty customer segments - they represent high-value opportunities',
                    '• Enhance mobile shopping experience - significant portion of orders via mobile devices',
                    '• Implement personalized recommendations based on FitMap body measurement data',
                    '• Reduce order cancellation rates through improved inventory visibility'
                ]
            },
            {
                'title': '2. Inventory & Merchandising Strategy',
                'points': [
                    '• Optimize stock levels for top-selling sizes to reduce stockouts',
                    '• Implement dynamic pricing strategies for slow-moving inventory',
                    '• Analyze markdown patterns to improve initial pricing accuracy',
                    '• Leverage seasonal trends identified in Q4 for better planning'
                ]
            },
            {
                'title': '3. Marketing & Campaign Optimization',
                'points': [
                    '• Double down on high-performing campaigns (summer_promo, cyber_monday)',
                    '• Increase investment in channels with highest conversion rates',
                    '• Develop targeted campaigns for dormant customers to reactivate',
                    '• Utilize A/B testing for promotional offers and discounts'
                ]
            },
            {
                'title': '4. Operational Efficiency',
                'points': [
                    '• Streamline fulfillment processes to reduce pending/cancelled orders',
                    '• Optimize shipping methods based on customer preferences and margins',
                    '• Implement AI-powered demand forecasting to reduce overstock',
                    '• Enhance cross-channel inventory management for better availability'
                ]
            },
            {
                'title': '5. Technology & Innovation',
                'points': [
                    '• Deploy AWS Quick Suite for real-time analytics and autonomous decision-making',
                    '• Integrate FitMap data into all customer touchpoints for personalization',
                    '• Implement conversational AI for customer service automation',
                    '• Build predictive models for customer lifetime value optimization'
                ]
            }
        ]

        for section in sections:
            # Section title
            ax.text(0.05, y_pos, section['title'], fontsize=12, fontweight='bold', color='#003366', va='top')
            y_pos -= 0.025

            # Points
            for point in section['points']:
                ax.text(0.08, y_pos, point, fontsize=9, va='top', color='#333333')
                y_pos -= 0.022

            y_pos -= 0.015  # Extra space between sections

        # Footer
        ax.text(0.5, 0.05, 'This report is optimized for AWS Quick Suite Quick Research analysis',
               ha='center', va='center', fontsize=10, color='#666666', style='italic')
        ax.text(0.5, 0.02, 'Use Quick Research to ask: "What are the key growth opportunities for DXL in 2025?"',
               ha='center', va='center', fontsize=9, color='#999999')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def run(self, output_file="DXL_Sales_Report_2024.pdf"):
        """Run the complete report generation process"""
        print("\n" + "="*60)
        print("DXL ANNUAL SALES REPORT GENERATOR")
        print("="*60)

        self.load_data()
        self.prepare_data()
        self.calculate_metrics()
        self.generate_pdf(output_file)

        print("\n" + "="*60)
        print("REPORT GENERATION COMPLETE!")
        print("="*60)
        print(f"\nOutput file: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")
        print("\nNext Steps:")
        print("1. Upload this PDF to AWS Quick Suite")
        print("2. Use Quick Research to analyze sales insights")
        print("3. Ask: 'What are the key trends and recommendations for 2025?'")
        print("\n" + "="*60)

if __name__ == "__main__":
    import os

    # Create report generator
    generator = DXLSalesReportGenerator()

    # Run the report
    generator.run("DXL_Sales_Report_2024.pdf")
