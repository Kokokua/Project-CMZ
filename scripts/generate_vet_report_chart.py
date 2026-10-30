import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def generate_vet_dashboard(csv_path, output_png_path):
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            r['duration_sec'] = float(r['duration_sec'])
            rows.append(r)
            
    total_sec = sum(r['duration_sec'] for r in rows)
    
    # Aggregations
    behavior_totals = defaultdict(float)
    macro_totals = defaultdict(float)
    for r in rows:
        behavior_totals[r['behavior']] += r['duration_sec']
        macro_totals[r['macro_state']] += r['duration_sec']
        
    # Set style
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    fig = plt.figure(figsize=(16, 10), facecolor='#0f172a')
    
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0], hspace=0.35, wspace=0.25)
    
    # 1. Macro State Donut Chart
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#0f172a')
    
    colors_macro = {'INACTIVE': '#38bdf8', 'ACTIVE': '#f59e0b'}
    labels = [f"{k}\n({v/3600:.1f} hrs / {v/total_sec*100:.1f}%)" for k, v in macro_totals.items()]
    wedges, texts, autotexts = ax1.pie(
        list(macro_totals.values()),
        labels=labels,
        colors=[colors_macro.get(k, '#94a3b8') for k in macro_totals.keys()],
        autopct='%1.1f%%',
        pctdistance=0.75,
        startangle=140,
        textprops={'color': '#f8fafc', 'fontsize': 11, 'weight': 'bold'},
        wedgeprops=dict(width=0.45, edgecolor='#1e293b', linewidth=2)
    )
    for at in autotexts:
        at.set_color('#ffffff')
        at.set_fontsize(12)
        at.set_weight('bold')
    ax1.set_title("24-Hour Macro Activity Budget\n(Active vs Inactive)", color='#38bdf8', fontsize=14, weight='bold', pad=15)
    
    # 2. Detailed Ethogram Behaviors Bar Chart
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1e293b')
    ax2.tick_params(colors='#94a3b8', labelsize=10)
    for spine in ax2.spines.values():
        spine.set_color('#334155')
        
    sorted_beh = sorted(behavior_totals.items(), key=lambda x: x[1], reverse=True)
    beh_names = [k.replace('_', ' ').title() for k, v in sorted_beh]
    beh_hrs = [v / 3600.0 for k, v in sorted_beh]
    y_pos = np.arange(len(beh_names))
    
    colors_beh = ['#38bdf8', '#f59e0b', '#10b981', '#818cf8', '#ec4899', '#f43f5e']
    bars = ax2.barh(y_pos, beh_hrs, color=colors_beh[:len(beh_names)], edgecolor='#0f172a', height=0.55)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(beh_names, color='#f8fafc', fontsize=11, weight='bold')
    ax2.set_xlabel("Total Time (Hours)", color='#94a3b8', fontsize=11)
    ax2.set_title("Behavior Breakdown (Chiang Mai Zoo Ethogram)", color='#10b981', fontsize=14, weight='bold', pad=15)
    
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 0.15, bar.get_y() + bar.get_height()/2.0, f"{w:.2f} h",
                 va='center', color='#f8fafc', fontsize=10, weight='bold')
    ax2.set_xlim(0, max(beh_hrs) * 1.25)
    ax2.grid(axis='x', color='#334155', linestyle='--', alpha=0.7)
    
    # 3. 24-Hour Chronogram Timeline (Bottom Span)
    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_facecolor('#1e293b')
    ax3.tick_params(colors='#94a3b8', labelsize=10)
    for spine in ax3.spines.values():
        spine.set_color('#334155')
        
    hours = np.arange(24)
    active_hourly = np.zeros(24)
    inactive_hourly = np.zeros(24)
    
    for r in rows:
        st_parts = [int(x) for x in r['start_time'].split(':')]
        dur_m = r['duration_sec'] / 60.0
        st_h = min(23, st_parts[0])
        
        # distribute across hours
        rem_m = dur_m
        curr_h = st_h
        while rem_m > 0 and curr_h < 24:
            available = 60.0
            alloc = min(rem_m, available)
            if r['macro_state'] == 'ACTIVE':
                active_hourly[curr_h] += alloc
            else:
                inactive_hourly[curr_h] += alloc
            rem_m -= alloc
            curr_h += 1
            
    # Normalize hourly totals to 60 mins max
    for h in range(24):
        tot = active_hourly[h] + inactive_hourly[h]
        if tot > 60:
            active_hourly[h] = (active_hourly[h] / tot) * 60
            inactive_hourly[h] = (inactive_hourly[h] / tot) * 60
        elif tot == 0:
            inactive_hourly[h] = 60 # default sleeping if quiet
            
    p1 = ax3.bar(hours, inactive_hourly, label='Inactive (Sleeping / Resting)', color='#38bdf8', edgecolor='#0f172a', width=0.75)
    p2 = ax3.bar(hours, active_hourly, bottom=inactive_hourly, label='Active (Locomotion / Eating / Drinking)', color='#f59e0b', edgecolor='#0f172a', width=0.75)
    
    ax3.set_xticks(hours)
    ax3.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45, color='#94a3b8')
    ax3.set_ylabel("Minutes / Hour", color='#94a3b8', fontsize=11)
    ax3.set_title("24-Hour Behavioral Chronogram (April 05, 2026: 00:00 - 24:00)", color='#f59e0b', fontsize=14, weight='bold', pad=15)
    ax3.legend(loc='upper right', facecolor='#0f172a', edgecolor='#334155', labelcolor='#f8fafc', fontsize=11)
    ax3.set_ylim(0, 68)
    ax3.grid(axis='y', color='#334155', linestyle='--', alpha=0.7)
    
    fig.suptitle("Large Indian Civet (Viverra zibetha) — Automated Daily Behavior Report\nChiang Mai Zoo × Chiang Mai University (Phase 2 Submission)",
                 fontsize=16, color='#f8fafc', weight='bold', y=0.98)
    
    plt.savefig(output_png_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Vet report dashboard successfully saved to: {output_png_path}")

if __name__ == "__main__":
    test_csv = r"D:\CMU\4th\1 st\image processing\project cmz\finish\daily_behavior_log.csv"
    test_png = r"D:\CMU\4th\1 st\image processing\project cmz\finish\vet_activity_report.png"
    generate_vet_dashboard(test_csv, test_png)
