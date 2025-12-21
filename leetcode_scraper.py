import requests

URL = "https://leetcode.com/graphql"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    }

def run_leetcode_query(query, variables):
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(URL, json=payload, headers=headers)
    data = response.json()

    if "data" not in data:
        return None

    return data["data"]



# YOUR QUERIES (REUSED)


query_userSessionProgress="""
    \n    query userSessionProgress($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n  }\n  matchedUser(username: $username) {\n    submitStats {\n      acSubmissionNum {\n        difficulty\n        count\n        submissions\n      }\n      totalSubmissionNum {\n        difficulty\n        count\n        submissions\n      }\n    }\n  }\n}\n
"""

query_recentAcSubmissions="""
    \n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n
"""

query_userContestRankingInfo="""
    \n    query userContestRankingInfo($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    totalParticipants\n    topPercentage\n    badge {\n      name\n    }\n  }\n  userContestRankingHistory(username: $username) {\n    attended\n    trendDirection\n    problemsSolved\n    totalProblems\n    finishTimeInSeconds\n    rating\n    ranking\n    contest {\n      title\n      startTime\n    }\n  }\n}\n
"""

query_skillStats="""
    \n    query skillStats($username: String!) {\n  matchedUser(username: $username) {\n    tagProblemCounts {\n      advanced {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n      intermediate {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n      fundamental {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n    }\n  }\n}\n
"""

query_userBadges="""
    \n    query userBadges($username: String!) {\n  matchedUser(username: $username) {\n    badges {\n      id\n      name\n      shortName\n      displayName\n      icon\n      hoverText\n      medal {\n        slug\n        config {\n          iconGif\n          iconGifBackground\n        }\n      }\n      creationDate\n      category\n    }\n    upcomingBadges {\n      name\n      icon\n      progress\n    }\n  }\n}\n
"""

query_userProfileCalendar="""
    \n    query userProfileCalendar($username: String!, $year: Int) {\n  matchedUser(username: $username) {\n    userCalendar(year: $year) {\n      activeYears\n      streak\n      totalActiveDays\n      dccBadges {\n        timestamp\n        badge {\n          name\n          icon\n        }\n      }\n      submissionCalendar\n    }\n  }\n}\n
"""




# DASHBOARD DATA BUILDER
def fetch_full_leetcode_overview():
    variables = {
        "username": "satyam15890",
        "limit": 10
    }

    session_data = run_leetcode_query(query_userSessionProgress, variables)
    recent_data = run_leetcode_query(query_recentAcSubmissions, variables)
    contest_data = run_leetcode_query(query_userContestRankingInfo, variables)
    skill_data = run_leetcode_query(query_skillStats, variables)
    badge_data = run_leetcode_query(query_userBadges, variables)
    calendar_data = run_leetcode_query(query_userProfileCalendar, variables)

    if not session_data or not recent_data or not contest_data:
        return None

    # PLATFORM TOTAL
    platform = {
        i["difficulty"]: i["count"]
        for i in session_data["allQuestionsCount"]
        if i["difficulty"] != "All"
    }

    #  SOLVED
    solved = {
        i["difficulty"]: i["count"]
        for i in session_data["matchedUser"]["submitStats"]["acSubmissionNum"]
        if i["difficulty"] != "All"
    }

    # ACCURACY
    accuracy = {}
    total_submissions = {}
    accepted = session_data["matchedUser"]["submitStats"]["acSubmissionNum"]
    total = session_data["matchedUser"]["submitStats"]["totalSubmissionNum"]

    for a, t in zip(accepted, total):
        if a["difficulty"] != "All" and t["submissions"] != 0:
            accuracy[a["difficulty"]] = round(
                (a["submissions"] / t["submissions"]) * 100, 2
            )
            total_submissions[a["difficulty"]] = t["submissions"]

    # RECENT
    recent = recent_data.get("recentAcSubmissionList", [])

    # ---------- CONTEST ----------
    contest = contest_data.get("userContestRanking", {})
    contest_history_raw = contest_data.get("userContestRankingHistory", [])
    contest_history = [c for c in contest_history_raw if c.get("attended")]

    # SKILLS EXTRACTION
    if skill_data and "matchedUser" in skill_data:
        skills = skill_data["matchedUser"].get("tagProblemCounts", {})
    else:
        skills = {
            "fundamental": [],
            "intermediate": [],
            "advanced": []
        }

    # BADGES EXTRACTION
    if badge_data and "matchedUser" in badge_data:
        badges = badge_data["matchedUser"].get("badges", [])
        upcoming_badges = badge_data["matchedUser"].get("upcomingBadges", [])
    else:
        badges = []
        upcoming_badges = []

    # PROFILE CALENDAR SAFE EXTRACTION
    if calendar_data and "matchedUser" in calendar_data:
        calendar = calendar_data["matchedUser"].get("userCalendar", {})
        active_years = calendar.get("activeYears", [])
        streak = calendar.get("streak", 0)
        total_active_days = calendar.get("totalActiveDays", 0)
        dcc_badges = calendar.get("dccBadges", [])
        submission_calendar = calendar.get("submissionCalendar", "{}")
    else:
        active_years = []
        streak = 0
        total_active_days = 0
        dcc_badges = []
        submission_calendar = "{}"


    return {
        "username": variables["username"],
        "platform": platform,
        "solved": solved,
        "accuracy": accuracy,
        "total_submissions": total_submissions,
        "recent": recent,
        "contest": contest,
        "contest_history": contest_history,
        "skills": skills,
        "badges": badges,
        "upcoming_badges": upcoming_badges,
        "active_years": active_years,
        "streak": streak,
        "total_active_days": total_active_days,
        "dcc_badges": dcc_badges,
        "submission_calendar": submission_calendar

    }



