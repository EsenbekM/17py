
def make_readable(s):
    return '{:02}:{:02}:{:02}'.format(s // 3600, s // 60 % 60, s % 60)


print(make_readable(0))  # "00:00:00"
print(make_readable(5))  # "00:00:05"
print(make_readable(60))  # "00:01:00"
print(make_readable(86399))  # "23:59:59"
print(make_readable(359999))  # "99:59:59"