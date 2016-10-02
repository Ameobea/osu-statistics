from datetime import datetime, timedelta
from pprint import pprint
import MySQLdb

# Steps through time periods one week at a time, returning the min+max amounts of PP necessary
# to have a rank within a certain range.
def pp_rank_ranges(start_date, end_date, upper_range, lower_range):
    db = MySQLdb.connect(host="ameobea.me", user="osu_stats_local2", passwd="99889", db="osutrack")

    time_diff = timedelta(7)
    cur_date = start_date
    # start_date, end_date, min_pp, max_pp
    results = []

    while cur_date < end_date:
        # [(timestamp, osu_id, pp_raw, pp_rank), (...), ...]
        res = pp_rank_fetch(db, cur_date, cur_date + time_diff, upper_range, lower_range)

        if len(res) > 0:
            min = res[0][2]
        else:
            min = 0
        max = 0
        for p in res:
            if p[2] < min:
                min = p[2]
            if p[2] > max:
                max = p[2]

        results.append([cur_date, cur_date + time_diff, min, max])

        cur_date += time_diff

    db.close()
    return results

# Fetch a timerange and return the result
def pp_rank_fetch(db, start_date, end_date, upper_range, lower_range):
    query = ("SELECT `timestamp`,`osu_id`,`pp_raw`,`pp_rank` FROM `osustd` WHERE `pp_rank` < {}"
      " AND `pp_rank` > {} AND `timestamp` > '{}' AND `timestamp` < '{}'"
      " ORDER BY `pp_rank`")
    query = query.format(upper_range, lower_range, str(start_date), str(end_date))

    cur = db.cursor()
    cur.execute(query)

    res = cur.fetchall()
    pprint(res)
    return res

############################################

start_date = datetime(2014, 5, 26, 0, 0)
end_date = datetime.now();

# upper and lower rank to select
upper_range = 100
lower_range = 0

while upper_range < 100200:
    results = pp_rank_ranges(start_date, end_date, upper_range, lower_range)

    # write results to file in the form of a CSV
    with open("res_{}-{}.csv".format(lower_range, upper_range), "w") as f:
        for b in results:
            line = "{}, {}, {}, {}\n"
            line = line.format(str(b[0]), str(b[1]), b[2], b[3])
            f.write(line)

    upper_range += 1000
    lower_range += 1000
