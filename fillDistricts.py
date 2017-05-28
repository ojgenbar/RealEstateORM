# -*- coding: UTF-8 -*-

# ОСТАВЬ!!!!

from ORMBase import District
from ORMBase import session

dis = list()
dis.append(District(name=u'Адмиралтейский район'))
dis.append(District(name=u'Василеостровский район'))
dis.append(District(name=u'Выборгский район'))
dis.append(District(name=u'Калининский район'))
dis.append(District(name=u'Кировский район'))
dis.append(District(name=u'Колпинский район'))
dis.append(District(name=u'Красногвардейский район'))
dis.append(District(name=u'Красносельский район'))
dis.append(District(name=u'Кронштадтский район'))
dis.append(District(name=u'Курортный район'))
dis.append(District(name=u'Московский район'))
dis.append(District(name=u'Невский район'))
dis.append(District(name=u'Петроградский район'))
dis.append(District(name=u'Петродворцовый район'))
dis.append(District(name=u'Приморский район'))
dis.append(District(name=u'Пушкинский район'))
dis.append(District(name=u'Фрунзенский район'))
dis.append(District(name=u'Центральный район'))
dis.append(District(name=u'Область'))

session.add_all(dis)

session.commit()
