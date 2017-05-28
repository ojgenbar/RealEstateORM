# -*- coding: UTF-8 -*-

from ORMBase import session

# session.execute('DELETE FROM price_history;')
# session.execute('DELETE FROM flat;')
# session.execute('''SELECT   "public"."district"."name",
#          "public"."address"."ru_address",
#          "public"."flat"."link",
#          "public"."flat"."qrooms",
#          "public"."flat"."ad_type",
#          "public"."flat"."bn_id",
#          "public"."price_history"."price",
#          "public"."price_history"."price_sqm",
#          "public"."price_history"."observe_date"
# FROM     "flat"
# INNER JOIN "address"  ON "flat"."address_id" = "address"."id"
# INNER JOIN "price_history"  ON "price_history"."flat_id" = "flat"."id"
# INNER JOIN "district"  ON "address"."district_id" = "district"."id"
# WHERE "public"."flat"."link" = 'http://www.bn.ru/detail/flats/1194738.html';''')

session.execute('''
                DELETE FROM "public"."price_history" AS PH
                WHERE PH."observe_date" = '2017-02-09'::date''')

# session.commit()
