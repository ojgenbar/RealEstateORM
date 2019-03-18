# -*- coding: UTF-8 -*-
from ORMBase import Flat, Address, PriceHistory
from sqlalchemy.orm.exc import NoResultFound


"""
Old shit. It should be rewritten in not so retard way
"""


def get_district_number(district):
    district = district
    DISTR_DICT = {
         u'Адмиралтейский район': 1,
         u'Василеостровский район': 2,
         u'Выборгский район': 3,
         u'Калининский район': 4,
         u'Кировский район': 5,
         u'Колпинский район': 6,
         u'Красногвардейский район': 7,
         u'Красносельский район': 8,
         u'Кронштадтский район': 9,
         u'Курортный район': 10,
         u'Московский район': 11,
         u'Невский район': 12,
         u'Петроградский район': 13,
         u'Петродворцовый район': 14,
         u'Приморский район': 15,
         u'Пушкинский район': 16,
         u'Фрунзенский район': 17,
         u'Центральный район': 18,
         u'Область': 19}

    res = DISTR_DICT.get(district, 19)

    return res


def upload_day(session, properties_lst, current_date):

    for row in properties_lst:
        qrooms = row[0]
        distID = get_district_number(row[1])
        ruAddr = row[2]
        enAddr = row[5]
        x, y = row[4], row[3]
        buiType = row[7]

        lst1 = row[6].replace(u'\\', u'/').split(u'/')
        if len(lst1) == 2:
            try:
                floor = int(lst1[0])
            except ValueError:
                floor = None
            try:
                floors = int(lst1[1])
            except ValueError:
                floors = None
        else:
            floor = None
            floors = None

        area = row[8]
        k_area = row[10]
        l_area = row[9]
        bath = row[11]
        price = row[13]
        abil = row[15]
        agen = row[16]
        tel = row[17]
        descr = row[18]
        bn_id = row[19]
        bn_type = row[20]
        link = row[21]

        sup = PriceHistory(observe_date=current_date, price=price)
        if bn_type == 3:
            q = session.query(Flat.id, Flat.address_id).filter(Flat.bn_id == bn_id,
                                                               Flat.ad_type == 3).one_or_none()
        else:
            q = session.query(Flat.id, Flat.address_id).filter(Flat.bn_id == bn_id,
                                                               Flat.ad_type != 3).one_or_none()
        if q:
            fl_id, addrID = q
            sup.flat = Flat(
                id=fl_id,
                qrooms=qrooms,
                floor=floor,
                kitchen_area=k_area,
                living_area=l_area,
                bathroom=bath,
                abilities=abil,
                agency=agen,
                tel=tel,
                description=descr,
                area=area,
                bn_id=bn_id,
                ad_type=bn_type,
                link=link)

            oldFloors, oldBuiType = session.query(Address.floors,
                                                  Address.building_type).filter(Address.id == addrID).one()
            if floors < oldFloors:
                floors = oldFloors
            if not buiType:
                buiType = oldBuiType
            sup.flat.address = Address(
                id=addrID,
                floors=floors,
                building_type=buiType)
        else:
            sup.flat = Flat(
                qrooms=qrooms,
                floor=floor,
                kitchen_area=k_area,
                living_area=l_area,
                bathroom=bath,
                abilities=abil,
                agency=agen,
                tel=tel,
                description=descr,
                area=area,
                bn_id=bn_id,
                ad_type=bn_type,
                link=link)
            try:
                addrID, oldFloors, oldBuiType = session.query(Address.id,
                    Address.floors, Address.building_type).filter(Address.en_address == enAddr).one()
                if floors < oldFloors:
                    floors = oldFloors
                if not buiType:
                    buiType = oldBuiType
                sup.flat.address = Address(
                    id=addrID,
                    floors=floors,
                    building_type=buiType)
            except NoResultFound:
                sup.flat.address = Address(
                    geom='SRID=4326; POINT(%.7f %.7f)' % (x, y),
                    floors=floors,
                    ru_address=ruAddr,
                    en_address=enAddr,
                    district_id=distID,
                    building_type=buiType)
        sup._price_sqm = sup.price_sqm
        # sup._price_sqm = sup.price_sqm
        # print sup._price_sqm
        session.merge(sup)
    session.commit()
