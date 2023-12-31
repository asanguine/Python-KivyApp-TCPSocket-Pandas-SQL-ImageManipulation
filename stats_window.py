from model import create_connection, retrieve_user_id, get_study_data, get_aggregated_study_data
import matplotlib.pyplot as plt
from kivy.uix.modalview import ModalView
import pandas as pd
from datetime import datetime, timedelta

class StatsWindow(ModalView):
    # study_data_list = get_study_data(conn, user_id)
    # for row in study_data_list:
    #     print(f"Date: {row[0]}, Duration: {row[1]} minutes")

    # for date, total_duration in aggregated_study_data:
    #     print(f"Date: {date}, Total Duration: {total_duration} minutes")

    def get_current_week(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week


    def create_barplot(self):
        conn = create_connection()
        user_id = retrieve_user_id(conn)
        study_data = get_aggregated_study_data(conn, user_id)

        start_of_week, end_of_week = self.get_current_week()
        date_range = pd.date_range(start_of_week, end_of_week)

        df = pd.DataFrame({'Date': date_range, 'Duration': 0})

        for date, duration in study_data:
            date = pd.to_datetime(date).date()
            if date in df['Date'].dt.date.values:
                df.loc[df['Date'].dt.date == date, 'Duration'] = duration

        x_positions = range(len(df['Date']))
        
        plt.bar(x_positions, df['Duration'], color='purple')
        plt.xlabel('Date')
        plt.ylabel('Total Duration (minutes)')
        plt.title('Study Sessions - Current Week')
        plt.xticks(x_positions, df['Date'].dt.strftime('%Y-%m-%d'), rotation=90, ha='right')
        plt.tight_layout()
        plt.savefig('study_sessions_plot.png')


    def update_stats_image(self):
        stats_image = self.ids.stats_image
        stats_image.source = 'study_sessions_plot.png'
        stats_image.reload()
