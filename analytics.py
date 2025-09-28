import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine
import os
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import ColorScaleRule
import warnings
warnings.filterwarnings('ignore')

os.makedirs('charts', exist_ok=True)
os.makedirs('exports', exist_ok=True)

class SkyTrackAnalytics:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'airport_analytics',
            'user': 'postgres',
            'password': '0000'
        }
        
        connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        self.engine = create_engine(connection_string)
        
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        
        print("Database connection established successfully")
    
    def create_pie_chart(self):
        """График 1: Круговая диаграмма - распределение рейсов по авиакомпаниям"""
        print("\nCreating pie chart...")
        
        query = """
        SELECT 
            a.airline_name as airline,
            COUNT(f.flight_id) as flight_count
        FROM airline a 
        JOIN flights f ON a.airline_id = f.airline_id
        GROUP BY a.airline_name
        ORDER BY COUNT(f.flight_id) DESC
        LIMIT 8;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for pie chart")
                return
            
            plt.figure(figsize=(10, 8))
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFB366', '#B3B3FF']
            
            wedges, texts, autotexts = plt.pie(df['flight_count'], 
                                             labels=df['airline'], 
                                             autopct='%1.1f%%',
                                             colors=colors,
                                             startangle=90)
            
            plt.title('Flight Distribution by Airlines', fontsize=14, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig('charts/pie_chart_airlines.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_rows = len(df)
            total_flights = df['flight_count'].sum()
            print(f"Pie chart created: {total_rows} airlines, {total_flights} total flights")
            print(f"Shows: market share of airlines by number of flights")
            print(f"Saved to: charts/pie_chart_airlines.png")
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
    
    def create_bar_chart(self):
        """График 2: Столбчатая диаграмма - бронирования по платформам"""
        print("\nCreating bar chart...")
        
        query = """
        SELECT 
            b.booking_platform as platform,
            COUNT(b.booking_id) as booking_count,
            ROUND(AVG(b.price), 2) as avg_price
        FROM booking b
        GROUP BY b.booking_platform
        ORDER BY COUNT(b.booking_id) DESC
        LIMIT 10;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for bar chart")
                return
            
            plt.figure(figsize=(12, 6))
            bars = plt.bar(range(len(df)), df['booking_count'], 
                          color='skyblue', edgecolor='navy', linewidth=0.7)
            
            for i, (bar, count) in enumerate(zip(bars, df['booking_count'])):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom', fontweight='bold')
            
            plt.title('Top 10 Booking Platforms by Volume', fontsize=14, fontweight='bold')
            plt.xlabel('Booking Platform', fontsize=12)
            plt.ylabel('Number of Bookings', fontsize=12)
            plt.xticks(range(len(df)), [p[:15] + '...' if len(p) > 15 else p for p in df['platform']], rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('charts/bar_chart_platforms.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_rows = len(df)
            print(f"Bar chart created: {total_rows} platforms analyzed")
            print(f"Shows: most popular booking platforms")
            print(f"Saved to: charts/bar_chart_platforms.png")
            
        except Exception as e:
            print(f"Error creating bar chart: {e}")
    
    def create_horizontal_bar_chart(self):
        """График 3: Горизонтальная столбчатая диаграмма - загруженность аэропортов"""
        print("\nCreating horizontal bar chart...")
        
        query = """
        SELECT 
            ap.airport_name as airport,
            ap.city as city,
            COUNT(DISTINCT f.flight_id) as flight_count
        FROM airport ap
        LEFT JOIN flights f ON (ap.airport_id = f.departure_airport_id OR ap.airport_id = f.arrival_airport_id)
        GROUP BY ap.airport_name, ap.city
        HAVING COUNT(DISTINCT f.flight_id) > 0
        ORDER BY COUNT(DISTINCT f.flight_id) DESC
        LIMIT 15;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for horizontal bar chart")
                return
            
            plt.figure(figsize=(12, 8))
            
            labels = [f"{airport}\n({city})" for airport, city in zip(df['airport'], df['city'])]
            
            bars = plt.barh(range(len(df)), df['flight_count'], 
                           color='lightcoral', edgecolor='darkred', linewidth=0.7)
            
            for i, (bar, count) in enumerate(zip(bars, df['flight_count'])):
                plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                        str(count), va='center', fontweight='bold')
            
            plt.title('Top 15 Busiest Airports by Flight Volume', fontsize=14, fontweight='bold')
            plt.xlabel('Number of Flights', fontsize=12)
            plt.ylabel('Airport', fontsize=12)
            plt.yticks(range(len(df)), labels)
            plt.grid(axis='x', alpha=0.3)
            plt.gca().invert_yaxis()
            
            plt.tight_layout()
            plt.savefig('charts/horizontal_bar_airports.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_rows = len(df)
            top_airport = df.iloc[0]
            print(f"Horizontal bar chart created: {total_rows} airports analyzed")
            print(f"Shows: which airports serve as major transportation hubs")
            print(f"Busiest airport: {top_airport['airport']} with {top_airport['flight_count']} flights")
            print(f"Saved to: charts/horizontal_bar_airports.png")
            
        except Exception as e:
            print(f"Error creating horizontal bar chart: {e}")
    
    def create_line_chart(self):
        """График 4: Линейный график - рейсы по статусам"""
        print("\nCreating line chart...")
        
        query = """
        SELECT 
            f.status as flight_status,
            COUNT(f.flight_id) as flight_count
        FROM flights f
        GROUP BY f.status
        ORDER BY f.status;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for line chart")
                return
            
            plt.figure(figsize=(12, 6))
            
            plt.plot(df['flight_status'], df['flight_count'], 
                    marker='o', linewidth=3, markersize=8, 
                    color='green', markerfacecolor='lightgreen', 
                    markeredgecolor='darkgreen', markeredgewidth=2)
            
            for i, (status, count) in enumerate(zip(df['flight_status'], df['flight_count'])):
                plt.annotate(str(count), (i, count), 
                           textcoords="offset points", xytext=(0,10), ha='center',
                           fontweight='bold', fontsize=11)
            
            plt.title('Flight Count by Status', fontsize=14, fontweight='bold')
            plt.xlabel('Flight Status', fontsize=12)
            plt.ylabel('Number of Flights', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('charts/line_chart_flight_status.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_flights = df['flight_count'].sum()
            print(f"Line chart created: {len(df)} flight statuses analyzed")
            print(f"Shows: distribution of flights by operational status")
            print(f"Total flights: {total_flights}")
            print(f"Saved to: charts/line_chart_flight_status.png")
            
        except Exception as e:
            print(f"Error creating line chart: {e}")
    
    def create_histogram(self):
        """График 5: Гистограмма - распределение цен билетов"""
        print("\nCreating histogram...")
        
        query = """
        SELECT 
            b.price as ticket_price
        FROM booking b
        WHERE b.price > 0;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for histogram")
                return
            
            plt.figure(figsize=(12, 6))
            
            n, bins, patches = plt.hist(df['ticket_price'], bins=20, 
                                       color='orange', alpha=0.7, 
                                       edgecolor='darkorange', linewidth=1.2)
            
            for i, patch in enumerate(patches):
                patch.set_facecolor(plt.cm.viridis(i / len(patches)))
            
            plt.title('Distribution of Ticket Prices', fontsize=14, fontweight='bold')
            plt.xlabel('Ticket Price ($)', fontsize=12)
            plt.ylabel('Number of Bookings', fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            
            mean_price = df['ticket_price'].mean()
            median_price = df['ticket_price'].median()
            plt.axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_price:.0f}')
            plt.axvline(median_price, color='blue', linestyle='--', linewidth=2, label=f'Median: ${median_price:.0f}')
            plt.legend()
            
            plt.tight_layout()
            plt.savefig('charts/histogram_ticket_prices.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_bookings = len(df)
            print(f"Histogram created: {total_bookings} bookings analyzed")
            print(f"Shows: price distribution of airline tickets")
            print(f"Average price: ${mean_price:.2f}")
            print(f"Price range: ${df['ticket_price'].min():.2f}-${df['ticket_price'].max():.2f}")
            print(f"Saved to: charts/histogram_ticket_prices.png")
            
        except Exception as e:
            print(f"Error creating histogram: {e}")
    
    def create_scatter_plot(self):
        """График 6: Диаграмма рассеяния - связь между весом багажа и ценой билета"""
        print("\nCreating scatter plot...")
        
        query = """
        SELECT 
            bag.weight_in_kg as baggage_weight,
            b.price as ticket_price
        FROM baggage bag
        JOIN booking b ON bag.booking_id = b.booking_id
        WHERE bag.weight_in_kg > 0 AND b.price > 0
        LIMIT 200;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for scatter plot")
                return
            
            plt.figure(figsize=(12, 8))
            
            plt.scatter(df['baggage_weight'], df['ticket_price'], 
                       alpha=0.6, s=50, color='purple', edgecolors='indigo')
            
            plt.title('Relationship between Baggage Weight and Ticket Price', fontsize=14, fontweight='bold')
            plt.xlabel('Baggage Weight (kg)', fontsize=12)
            plt.ylabel('Ticket Price ($)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Добавление линии тренда
            z = np.polyfit(df['baggage_weight'], df['ticket_price'], 1)
            p = np.poly1d(z)
            plt.plot(df['baggage_weight'], p(df['baggage_weight']), "r--", alpha=0.8, linewidth=2)
            
            plt.tight_layout()
            plt.savefig('charts/scatter_plot_baggage_price.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            total_points = len(df)
            correlation = df['baggage_weight'].corr(df['ticket_price'])
            print(f"Scatter plot created: {total_points} data points analyzed")
            print(f"Shows: correlation between baggage weight and ticket price")
            print(f"Correlation coefficient: {correlation:.3f}")
            print(f"Saved to: charts/scatter_plot_baggage_price.png")
            
        except Exception as e:
            print(f"Error creating scatter plot: {e}")
    
    def create_interactive_timeline(self):
        """Интерактивный график Plotly"""
        print("\nCreating interactive timeline with Plotly...")
        
        query = """
        SELECT 
            a.airline_name as airline,
            f.status as flight_status,
            COUNT(f.flight_id) as flight_count
        FROM airline a
        JOIN flights f ON a.airline_id = f.airline_id
        GROUP BY a.airline_name, f.status
        ORDER BY COUNT(f.flight_id) DESC
        LIMIT 20;
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            
            if df.empty:
                print("No data available for interactive chart")
                return
            
            fig = px.bar(df, 
                        x="airline", 
                        y="flight_count",
                        color="flight_status",
                        title="Flight Count by Airline and Status",
                        labels={
                            "airline": "Airline",
                            "flight_count": "Number of Flights",
                            "flight_status": "Flight Status"
                        })
            
            fig.update_layout(
                width=1000,
                height=600,
                title_font_size=16,
                xaxis_tickangle=-45
            )
            
            fig.show()
            
            total_records = len(df)
            total_airlines = df['airline'].nunique()
            print(f"Interactive chart created successfully")
            print(f"Shows: flight distribution by airline and status")
            print(f"Records displayed: {total_records}")
            print(f"Airlines included: {total_airlines}")
            
        except Exception as e:
            print(f"Error creating interactive chart: {e}")
    
    def export_to_excel(self):
        """Экспорт данных в Excel"""
        print("\nExporting analytical data to Excel...")
        
        queries = {
            'Airlines_Performance': """
                SELECT 
                    a.airline_name as "Airline Name",
                    COUNT(f.flight_id) as "Total Flights"
                FROM airline a
                LEFT JOIN flights f ON a.airline_id = f.airline_id
                GROUP BY a.airline_name
                ORDER BY COUNT(f.flight_id) DESC;
            """,
            'Airport_Traffic': """
                SELECT 
                    ap.airport_name as "Airport Name",
                    ap.city as "City",
                    COUNT(DISTINCT f.flight_id) as "Flight Count"
                FROM airport ap
                LEFT JOIN flights f ON (ap.airport_id = f.departure_airport_id OR ap.airport_id = f.arrival_airport_id)
                GROUP BY ap.airport_name, ap.city
                ORDER BY COUNT(DISTINCT f.flight_id) DESC;
            """,
            'Booking_Summary': """
                SELECT 
                    booking_platform as "Platform",
                    COUNT(*) as "Bookings",
                    AVG(price) as "Avg Price"
                FROM booking
                GROUP BY booking_platform
                ORDER BY COUNT(*) DESC;
            """
        }
        
        try:
            filename = 'exports/skytrack_analytics_report.xlsx'
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                total_rows = 0
                
                for sheet_name, query in queries.items():
                    df = pd.read_sql_query(query, self.engine)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    total_rows += len(df)
            
            self._apply_excel_formatting(filename, list(queries.keys()))
            
            sheet_count = len(queries)
            print(f"Excel export completed: {filename}")
            print(f"Sheets created: {sheet_count}, total data rows: {total_rows}")
            print(f"Formatting applied: frozen headers, filters, gradients")
            
        except Exception as e:
            print(f"Error during Excel export: {e}")
    
    def _apply_excel_formatting(self, filename, sheet_names):
        """Применение форматирования к Excel"""
        try:
            workbook = load_workbook(filename)
            
            for sheet_name in sheet_names:
                ws = workbook[sheet_name]
                
                ws.freeze_panes = "B2"
                
                if ws.max_row > 1:
                    ws.auto_filter.ref = ws.dimensions
                
                for col_idx in range(2, ws.max_column + 1):
                    col_letter = ws.cell(row=1, column=col_idx).column_letter
                    
                    has_numeric_data = False
                    for row_idx in range(2, min(ws.max_row + 1, 10)):
                        cell_value = ws.cell(row=row_idx, column=col_idx).value
                        if isinstance(cell_value, (int, float)) and cell_value is not None:
                            has_numeric_data = True
                            break
                    
                    if has_numeric_data:
                        rule = ColorScaleRule(
                            start_type="min", start_color="FFAA0000",
                            mid_type="percentile", mid_value=50, mid_color="FFFFFF00",
                            end_type="max", end_color="FF00AA00"
                        )
                        range_string = f"{col_letter}2:{col_letter}{ws.max_row}"
                        ws.conditional_formatting.add(range_string, rule)
                
                header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
                for col_idx in range(1, ws.max_column + 1):
                    cell = ws.cell(row=1, column=col_idx)
                    cell.fill = header_fill
                    cell.font = cell.font.copy(color="FFFFFF", bold=True)
            
            workbook.save(filename)
            
        except Exception as e:
            print(f"Warning: Formatting error occurred: {e}")
    
    def run_all_analytics(self):
        """Выполнение полного цикла аналитики"""
        print("SKYTRACK SOLUTIONS - COMPREHENSIVE ANALYTICS SUITE")
        print("=" * 60)
        
        self.create_pie_chart()
        self.create_bar_chart()
        self.create_horizontal_bar_chart()
        self.create_line_chart()
        self.create_histogram()
        self.create_scatter_plot()
        
        self.create_interactive_timeline()
        
        self.export_to_excel()
        
        print("\n" + "=" * 60)
        print("ALL ANALYTICAL TASKS COMPLETED SUCCESSFULLY!")
        print("Generated files:")
        print("   Charts folder: 6 visualization files saved")
        print("   Exports folder: Excel report with formatted data")
        print("=" * 60)


if __name__ == "__main__":
    analytics = SkyTrackAnalytics()
    analytics.run_all_analytics()