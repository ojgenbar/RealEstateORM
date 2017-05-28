from ORMBase import session
import datetime


def create(obsdate):
    y = str(obsdate.year).zfill(4)
    d = str(obsdate.day).zfill(2)
    m = str(obsdate.month).zfill(2)
    s1 = ''.join([y, m, d])
    s2 = '-'.join([y, m, d])
    session.execute('''
            BEGIN;

        -- CREATE VIEW "all%s" -----------------------------------
        CREATE OR REPLACE VIEW "public"."all%s" AS  SELECT flat.qrooms AS "Rooms",
            district.name AS "District",
            address.ru_address,
            address.en_address,
            flat.floor,
            address.floors,
            address.building_type,
            flat.area,
            flat.living_area,
            flat.kitchen_area,
            flat.bathroom,
            price_history.price,
            price_history.price_sqm,
            flat.abilities,
            flat.agency,
            flat.tel,
            flat.description,
            flat.bn_id,
            flat.ad_type,
            flat.link,
            flat.id,
            address.geom
           FROM (((address
             JOIN district ON ((address.district_id = district.id)))
             JOIN flat ON ((flat.address_id = address.id)))
             JOIN price_history ON ((price_history.flat_id = flat.id)))
          WHERE (price_history.observe_date = '%s'::date);;
        -- -------------------------------------------------------------

        COMMIT;
        ''' % (s1, s1, s2))
    session.commit()


if __name__ == "__main__":
    create(datetime.date(2017, 2, 9))
