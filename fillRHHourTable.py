from random import randint
model = """+-----------------------------------------+
| Dia: :day
| Horários: :h1 | :h2 | :h3 | :h4"""

for i in range(31):
    h1 = 8
    h2 = 12
    h3 = 13
    h4 = 18

    t1, t2, t3, t4 = '', '', '', ''
    minute = randint(-10,10)
    surprise = randint(0,2)
    if minute < 0:
        if surprise == 0:
            h1 -= 1  # 7h
            h2 -= 1  # 11h
            m1 = 60 + minute
            m2 = 60 + minute
            m3 = 30
            m4 = '00'
            t1 = '0'+str(h1)+':'+str(abs(m1))
            t2 = str(h2)+':'+str(abs(m2))
            t3 = str(h3)+':'+str(abs(m3))
            t4 = str(h4)+':'+str(m4)
        elif surprise == 1:
            h3 -= 1  # 12
            h4 -= 1  # 17
            m1 = '00'
            m2 = '00'
            m3 = 30 + minute
            m4 = 60 + minute
            t1 = '0'+str(h1)+':'+str(m1)
            t2 = str(h2)+':'+str(m2)
            t3 = str(h3)+':'+str(abs(m3))
            if len(str(m4)) >= 2:
                t4 = str(h4)+':'+str(abs(m4))
            else:
                t4 = str(h4)+':0'+str(abs(m4))
        elif surprise == 2:
            h1 -= 1  # 7
            m1 = 60 + minute
            m2 = '00'
            m3 = 30
            m4 = 0 + abs(minute)
            t1 = '0'+str(h1)+':'+str(abs(m1))
            t2 = str(h2)+':'+str(m2)
            t3 = str(h3)+':'+str(abs(m3))
            if len(str(m4)) >= 2:
                t4 = str(h4)+':'+str(abs(m4))
            else:
                t4 = str(h4)+':0'+str(abs(m4))

    elif minute > 0:
        if surprise == 0:
            m1 = 0 + minute
            m2 = 0 + minute
            m3 = 30
            m4 = '00'
            if len(str(m1)) >= 2:
                t1 = str(h1)+':'+str(abs(m1))
            else:
                t1 = str(h1)+':0'+str(abs(m1))
            if len(str(m2)) >= 2:
                t2 = str(h2)+':'+str(abs(m2))
            else:
                t2 = str(h2)+':0'+str(abs(m2))
            t3 = str(h3)+':'+str(abs(m3))
            t4 = str(h4)+':'+str(m4)
        elif surprise == 1:
            m1 = '00'
            m2 = '00'
            m3 = 30 + minute
            m4 = 0 + minute
            t1 = '0'+str(h1)+':'+str(m1)
            t2 = str(h2)+':'+str(m2)
            t3 = str(h3)+':'+str(abs(m3))
            if len(str(m4)) >= 2:
                t4 = str(h4)+':'+str(abs(m4))
            else:
                t4 = str(h4)+':0'+str(abs(m4))
        elif surprise == 2:
            h4 -= 1  # 17h
            m1 = 0 + minute
            m2 = '00'
            m3 = 30
            m4 = 60 - abs(minute)

            if len(str(m1)) >= 2:
                t1 = '0'+str(h1)+':'+str(abs(m1))
            else:
                t1 = '0'+str(h1)+':0'+str(abs(m1))
            t2 = str(h2)+':'+str(m2)
            t3 = str(h3)+':'+str(abs(m3))
            if len(str(m4)) >= 2:
                t4 = str(h4)+':'+str(abs(m4))
            else:
                t4 = str(h4)+':0'+str(abs(m4))
    else:
        m1 = '00'
        m2 = '00'
        m3 = '30'
        m4 = '00'
        t1 = '0'+str(h1)+':'+str(m1)
        t2 = str(h2)+':'+str(m2)
        t3 = str(h3)+':'+str(m3)
        t4 = str(h4)+':'+str(m4)
    print(model.replace(':h1', t1).replace(':h2', t2).replace(':h3', t3).replace(':h4', t4).replace(':day', str(i+1)))

