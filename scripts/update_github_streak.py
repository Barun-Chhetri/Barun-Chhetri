#!/usr/bin/env python3
"""
Dynamic GitHub Contribution & Streak Updater for Barun-Chhetri
Queries the GitHub GraphQL API directly, accurately aggregates all legitimate
contributions, calculates current streak, longest streak, and last contribution date,
and generates the pixel-perfect TokyoNight streak card SVG.
"""

import os
import sys
import json
import subprocess
from datetime import datetime, date

USERNAME = "Barun-Chhetri"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_SVG = os.path.join(REPO_ROOT, "assets", "github-streak-card.svg")

def fetch_contributions_graphql(username):
    """
    Fetch contribution calendar from GitHub GraphQL API across active account years.
    Uses gh CLI authentication if available, otherwise falls back to GITHUB_TOKEN env var.
    """
    # Barun-Chhetri account created July 21, 2024
    current_year = datetime.now().year
    years = list(range(2024, current_year + 1))
    
    daily_contributions = {}
    total_contributions = 0

    for yr in years:
        from_iso = f"{yr}-01-01T00:00:00Z"
        to_iso = f"{yr}-12-31T23:59:59Z"
        
        query = f"""
        query {{
          user(login: "{username}") {{
            contributionsCollection(from: "{from_iso}", to: "{to_iso}") {{
              contributionCalendar {{
                totalContributions
                weeks {{
                  contributionDays {{
                    date
                    contributionCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        try:
            cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            payload = json.loads(res.stdout)
            
            if "errors" in payload:
                print(f"[Warning] GraphQL error for year {yr}: {payload['errors']}", file=sys.stderr)
                continue
                
            cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            total_contributions += cal["totalContributions"]
            for week in cal["weeks"]:
                for day in week["contributionDays"]:
                    d_str = day["date"]
                    c_count = day["contributionCount"]
                    daily_contributions[d_str] = c_count
        except Exception as e:
            print(f"[Error] Failed to fetch GraphQL data for year {yr}: {e}", file=sys.stderr)
            raise e

    return total_contributions, daily_contributions

def compute_streak_metrics(total_contributions, daily_contributions):
    today_str = datetime.now().strftime("%Y-%m-%d")
    sorted_dates = sorted([d for d in daily_contributions.keys() if d <= today_str])
    
    last_contrib_date = None
    for d in sorted_dates:
        if daily_contributions[d] > 0:
            last_contrib_date = d

    longest_streak = 0
    temp_streak = 0
    streak_ranges = []
    cur_start = None
    prev_d = None

    for d in sorted_dates:
        count = daily_contributions[d]
        if count > 0:
            if temp_streak == 0:
                cur_start = d
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            if temp_streak > 0:
                streak_ranges.append((cur_start, prev_d, temp_streak))
            temp_streak = 0
        prev_d = d

    if temp_streak > 0:
        streak_ranges.append((cur_start, sorted_dates[-1], temp_streak))

    # Determine current active streak (active today or ended yesterday)
    yesterday_str = date.fromordinal(date.today().toordinal() - 1).strftime("%Y-%m-%d")
    current_streak = 0
    current_streak_range = ("", "")

    for start_d, end_d, length in streak_ranges:
        if end_d == today_str or end_d == yesterday_str:
            current_streak = length
            current_streak_range = (start_d, end_d)
            break

    # Format human-friendly ranges
    def format_short_date(iso_str):
        if not iso_str:
            return ""
        dt = datetime.strptime(iso_str, "%Y-%m-%d")
        return dt.strftime("%b %-d")

    def format_full_date(iso_str):
        if not iso_str:
            return ""
        dt = datetime.strptime(iso_str, "%Y-%m-%d")
        return dt.strftime("%b %-d, %Y")

    current_range_str = f"{format_short_date(current_streak_range[0])} - {format_short_date(current_streak_range[1])}" if current_streak > 0 else "No active streak"
    last_contrib_str = format_full_date(last_contrib_date) if last_contrib_date else "None"

    return {
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_contribution_date": last_contrib_str,
        "current_range_str": current_range_str,
        "account_range_str": "Jul 21, 2024 - Present"
    }

def generate_streak_svg(stats):
    total = stats["total_contributions"]
    curr = stats["current_streak"]
    longest = stats["longest_streak"]
    last_date = stats["last_contribution_date"]
    account_range = stats["account_range_str"]
    curr_range = stats["current_range_str"]

    svg_content = f"""<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'
     style='isolation: isolate' viewBox='0 0 495 195' width='495px' height='195px' direction='ltr'>
    <style>
        @keyframes currstreak {{
            0% {{ font-size: 3px; opacity: 0.2; }}
            80% {{ font-size: 34px; opacity: 1; }}
            100% {{ font-size: 28px; opacity: 1; }}
        }}
        @keyframes fadein {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif; }}
    </style>
    <defs>
        <clipPath id='outer_rectangle'>
            <rect width='495' height='195' rx='8'/>
        </clipPath>
        <mask id='mask_out_ring_behind_fire'>
            <rect width='495' height='195' fill='white'/>
            <ellipse id='mask-ellipse' cx='247.5' cy='32' rx='13' ry='18' fill='black'/>
        </mask>
    </defs>
    <g clip-path='url(#outer_rectangle)'>
        <!-- Background -->
        <g style='isolation: isolate'>
            <rect stroke='#000000' stroke-opacity='0' fill='#1A1B27' rx='8' x='0.5' y='0.5' width='494' height='194'/>
        </g>
        
        <!-- Column Dividers -->
        <g style='isolation: isolate'>
            <line x1='165' y1='28' x2='165' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#2F334D' stroke-linejoin='miter' stroke-linecap='square'/>
            <line x1='330' y1='28' x2='330' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#2F334D' stroke-linejoin='miter' stroke-linecap='square'/>
        </g>

        <!-- Column 1: Total Contributions -->
        <g style='isolation: isolate'>
            <g transform='translate(82.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#70A5FD' font-weight='700' font-size='28px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 0.6s'>
                    {total}
                </text>
            </g>
            <g transform='translate(82.5, 84)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#70A5FD' font-weight='400' font-size='14px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 0.7s'>
                    Total Contributions
                </text>
            </g>
            <g transform='translate(82.5, 114)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#38BDAE' font-weight='400' font-size='12px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 0.8s'>
                    {account_range}
                </text>
            </g>
        </g>

        <!-- Column 2: Current Streak -->
        <g style='isolation: isolate'>
            <!-- Ring around number -->
            <g mask='url(#mask_out_ring_behind_fire)'>
                <circle cx='247.5' cy='71' r='40' fill='none' stroke='#70A5FD' stroke-width='5' style='opacity: 0; animation: fadein 0.5s linear forwards 0.4s'></circle>
            </g>
            <!-- Fire icon -->
            <g transform='translate(247.5, 19.5)' stroke-opacity='0' style='opacity: 0; animation: fadein 0.5s linear forwards 0.6s'>
                <path d='M -12 -0.5 L 15 -0.5 L 15 23.5 L -12 23.5 L -12 -0.5 Z' fill='none'/>
                <path d='M 1.5 0.67 C 1.5 0.67 2.24 3.32 2.24 5.47 C 2.24 7.53 0.89 9.2 -1.17 9.2 C -3.23 9.2 -4.79 7.53 -4.79 5.47 L -4.76 5.11 C -6.78 7.51 -8 10.62 -8 13.99 C -8 18.41 -4.42 22 0 22 C 4.42 22 8 18.41 8 13.99 C 8 8.6 5.41 3.79 1.5 0.67 Z M -0.29 19 C -2.07 19 -3.51 17.6 -3.51 15.86 C -3.51 14.24 -2.46 13.1 -0.7 12.74 C 1.07 12.38 2.9 11.53 3.92 10.16 C 4.31 11.45 4.51 12.81 4.51 14.2 C 4.51 16.85 2.36 19 -0.29 19 Z' fill='#70A5FD' stroke-opacity='0'/>
            </g>

            <!-- Current Streak big number -->
            <g transform='translate(247.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#BF91F3' font-weight='700' font-size='28px' class='font-sans' style='animation: currstreak 0.6s linear forwards'>
                    {curr}
                </text>
            </g>

            <!-- Current Streak label -->
            <g transform='translate(247.5, 108)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#BF91F3' font-weight='700' font-size='14px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 0.9s'>
                    Current Streak
                </text>
            </g>

            <!-- Last Contribution Date & Range -->
            <g transform='translate(247.5, 145)'>
                <text x='0' y='21' stroke-width='0' text-anchor='middle' fill='#38BDAE' font-weight='400' font-size='11.5px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 0.9s'>
                    Last: {last_date}
                </text>
            </g>
        </g>

        <!-- Column 3: Longest Streak -->
        <g style='isolation: isolate'>
            <g transform='translate(412.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#70A5FD' font-weight='700' font-size='28px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 1.2s'>
                    {longest}
                </text>
            </g>
            <g transform='translate(412.5, 84)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#70A5FD' font-weight='400' font-size='14px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 1.3s'>
                    Longest Streak
                </text>
            </g>
            <g transform='translate(412.5, 114)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#38BDAE' font-weight='400' font-size='12px' class='font-sans' style='opacity: 0; animation: fadein 0.5s linear forwards 1.4s'>
                    {curr_range}
                </text>
            </g>
        </g>
    </g>
</svg>"""
    return svg_content

def main():
    print(f"Fetching GitHub contributions for @{USERNAME} via GraphQL API...")
    total, daily = fetch_contributions_graphql(USERNAME)
    stats = compute_streak_metrics(total, daily)
    
    print("\nVerified GitHub Statistics:")
    print(f"• Total Contributions:    {stats['total_contributions']}")
    print(f"• Current Streak:         {stats['current_streak']} days ({stats['current_range_str']})")
    print(f"• Longest Streak:         {stats['longest_streak']} days")
    print(f"• Last Contribution Date: {stats['last_contribution_date']}")
    
    os.makedirs(os.path.dirname(OUTPUT_SVG), exist_ok=True)
    svg_code = generate_streak_svg(stats)
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_code)
        
    print(f"\nGenerated streak card SVG at: {OUTPUT_SVG}")

if __name__ == "__main__":
    main()
