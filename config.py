dep_reg_1 = ['yvelines', 'essonne', 'seine-saint-denis', 'val-de-marne', 'hauts-de-seine', 'seine-et-marne']
dep_reg_2 = ['seine-maritime', 'cher', 'finistere', 'morbihan', 'manche', 'calvados', 'mayenne', 'sarthe', 'vendee', 'orne', 'loire-atlantique', 'maine-et-loire']
dep_reg_3 = ['aube', "cote-d''or", 'pas-de-calais', 'marne', 'meuse', 'moselle', 'doubs', 'bas-rhin', 'nord', 'somme', 'yonne', 'meurthe-et-moselle', 'saone-et-loire']
dep_reg_4 = ['haute-corse', 'bouches-du-rhone', 'var', 'vaucluse', 'drome', 'ardeche', 'isere', 'gard', 'savoie', 'haute-savoie', 'pyrenees-orientales', 'alpes-maritimes']
dep_reg_5 = ['indre-et-loire', 'aude', 'charente', 'pyrenees-atlantiques', 'hautes-pyrenees', 'landes', 'gironde', 'dordogne', 'tarn', 'ariege', 'gers', 'aveyron', 'haute-garonne', 'charente-maritime', 'vienne', 'haute-vienne']


#list_departement_reg_1 = "('yveline', 'essonne', 'seine-saint-denis', 'val-de-marne')"
list_departement_reg_1 = "("
list_departement_reg_1 += "'" + dep_reg_1[0] + "'" 
for dep in dep_reg_1[1:] :
    list_departement_reg_1 += ", " + "'" + dep + "'"
list_departement_reg_1 += ")"



#list_departement_reg_2 = "('cher', 'yonne')"
list_departement_reg_2 = "("
list_departement_reg_2 += "'" + dep_reg_2[0] + "'" 
for dep in dep_reg_2[1:] :
    list_departement_reg_2 += ", " + "'" + dep + "'"
list_departement_reg_2 += ")"



#list_departement_reg_3 = "('cher', 'yonne', 'aude')"
list_departement_reg_3 = "("
list_departement_reg_3 += "'" + dep_reg_3[0] + "'" 
for dep in dep_reg_3[1:] :
    list_departement_reg_3 += ", " + "'" + dep + "'"
list_departement_reg_3 += ")"




#list_departement_reg_4 = "('cher', 'yonne', 'oise')"
list_departement_reg_4 = "("
list_departement_reg_4 += "'" + dep_reg_4[0] + "'" 
for dep in dep_reg_4[1:] :
    list_departement_reg_4 += ", " + "'" + dep + "'"
list_departement_reg_4 += ")"



#list_departement_reg_5 = "('cher', 'yonne', 'moselle')"
list_departement_reg_5 = "("
list_departement_reg_5 += "'" + dep_reg_5[0] + "'" 
for dep in dep_reg_5[1:] :
    list_departement_reg_5 += ", " + "'" + dep + "'"
list_departement_reg_5 += ")"


reg_id_to_name = {
    1 : list_departement_reg_1,
    2 : list_departement_reg_2,
    3 : list_departement_reg_3,
    4 : list_departement_reg_4,
    5 : list_departement_reg_5
}


int_to_name = {
    1 : 'janvier',
    2 : 'fevrier',
    3 : 'mars',
    4 : 'avril',
    5 : 'mai',
    6 : 'juin',
    7 : 'juillet',
    8 : 'aout',
    9 : 'septembre',
    10 : 'octobre',
    11 : 'novembre',
    12 : 'decembre'
}
