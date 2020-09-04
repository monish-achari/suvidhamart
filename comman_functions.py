import datetime as dt
def add_data_to_table(db,token,data,table,key_variable,created_var,modified_var):
	"""
	this method add the data to table with adding 
	creation key,date of modified and created fields
	"""
	now_time = str(dt.datetime.now())
	val_key = db.child(table).push(data,token).get('name')
	data.update({key_variable:val_key})
	data.update({created_var:now_time})
	data.update({modified_var:now_time})
	table_obj = db.child(table).child(val_key)
	table_obj.update(data,token)
	return True,val_key

def return_foreign_key_val(data,column,comp_val,return_column_name):
	for i in data.keys():
		try: 
			if str(data.get(i,{}).get(column)) == str(comp_val):
				return str(data.get(i,{}).get(return_column_name))
		except:
			return 0
	return 0

def wallet_return_foreign_key_val(data,column,comp_val,return_column_name):
	try:
		result_val = data.get(comp_val,{})
		balance = [i for i in data.get(comp_val).values()][0].get(return_column_name)                                                        
		return balance
	except:
		return 0