
# See:
#     Matt Parker: How to mathematically calculate a fall through the Earth
#     https://www.youtube.com/watch?v=s94Gojs3Ags
#     code at: https://www.dropbox.com/s/vbwymdxjz47bsrs/Earth_fall.py?dl=0

# Comment:
# To better align the output, I would change the print line to:
# print 'Inc of {0:>14.5f} m gave a time of {1:>7.2f} s and max speed of {2:>7.2f} m/s - execution time: {3:>10.5f}'\
#       .format(inc, t * 2, v, end_time - start_time)
#
# To get the execution time, add:
# import time
#
# # first line on first while
# start_time = time.time()
# # right before print call
# end_time = time.time()


def fall(cap:float=1.0):

    import math
    import time

    r_earth = 6371000
    m_earth = 5.972 * 10**24
    g = 6.674 * 10**-11

    rho = m_earth/((4.0/3) * math.pi * r_earth**3)

    inc = r_earth/4.0

    while inc >= cap:
        start_time = time.time()

        x = r_earth
        a = g * rho * (4/3.0) * math.pi * x
        t = 0.0
        v = 0.0

        while x > 0:
            u = v
            v = (u**2 + 2 * a * inc)**0.5
            t = t + (v-u)/a
            x = x - inc
            a = g * rho * (4/3.0) * math.pi * x

        end_time = time.time()
        print(F"Inc of {inc:>14.5f} m gave a time of {t*2:>7.3f} s and max speed of {v:>7.3f} m/s "
              F"| exe time = {end_time-start_time:>17.13f} sec")

        if inc/2.0 < 1000:  # I wanted to double the number of increments until they are 1km~ish each
            if inc > 1000:
                inc = 1000
            else:           # Then I want to go down 1km, 100m, 10m etc
                inc = inc/10.0
        else:
            inc = inc/2.0

    return 'DONE'


if __name__ == '__main__':
    fall(0.1)
    exit()
