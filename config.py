dep_reg_1 = ['yveline', 'essonne', 'seine-saint-denis', 'val-de-marne']
dep_reg_2 = ['cher', 'yonne']
dep_reg_3 = ['cher', 'yonne', 'aude']
dep_reg_4 = ['cher', 'yonne', 'oise']
dep_reg_5 = ['cher', 'yonne', 'moselle']


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


#name_to_reg_id = { list_dep:id_reg for (id_reg, list_dep) in reg_id_to_name.items()}
