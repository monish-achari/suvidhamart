from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import pyrebase
from django.conf import settings
from comman_functions import *
import datetime as dt
import json
import uuid
"""
Error Handling Functions
"""

def handler404(request,va):
	return render(request, 'error/404.html')

def handler500(request):
	return render(request, 'error/404.html')


"""
<!-- The core Firebase JS SDK is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/7.14.4/firebase-app.js"></script>

<!-- TODO: Add SDKs for Firebase products that you want to use
     https://firebase.google.com/docs/web/setup#available-libraries -->
<script src="https://www.gstatic.com/firebasejs/7.14.4/firebase-analytics.js"></script>

<script>
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyAPTy6vrUp4PU7H205fZFkUEHs9LsoSDus",
    authDomain: "citric-proxy-241616.firebaseapp.com",
    databaseURL: "https://citric-proxy-241616.firebaseio.com",
    projectId: "citric-proxy-241616",
    storageBucket: "citric-proxy-241616.appspot.com",
    messagingSenderId: "1000975911785",
    appId: "1:1000975911785:web:a4a4007840f5501308cbf8",
    measurementId: "G-138FDLBEBE"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();
</script>
"""
#gs://citric-proxy-241616.appspot.com/
# Create your views here.

# config = {
#         "apiKey": "AIzaSyAPTy6vrUp4PU7H205fZFkUEHs9LsoSDus",
#         "authDomain": "citric-proxy-241616.firebaseapp.com",
#         "databaseURL": "https://citric-proxy-241616.firebaseio.com",
#         "storageBucket": "citric-proxy-241616.appspot.com",
#         "projectId": "citric-proxy-241616",
#         "messagingSenderId": "1000975911785",
#     	"appId": "1:1000975911785:web:a4a4007840f5501308cbf8",
#         # "serviceAccount": settings.BASE_DIR+'/credentials/zinc-interface-243315-1e90e041f0a6.json',
#     	"measurementId": "G-138FDLBEBE"
#     }

config = {
	"apiKey": "AIzaSyAJKvTG7YQevLeHsJzC9gYKXiVAD4bofsQ",
    "authDomain": "essentials-e7555.firebaseapp.com",
    "databaseURL": "https://essentials-e7555.firebaseio.com",
    "projectId": "essentials-e7555",
    "storageBucket": "essentials-e7555.appspot.com",
    "messagingSenderId": "407847376528",
    "appId": "1:407847376528:web:43925e60a64b68a6c0aa15",
    "measurementId": "G-1XPPMM586R"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def filter_function(dictval,campare_val):
	return_dict = {}
	for key in dictval.keys():
		for child_key in dictval[key].keys():
			product_lists = []
			# if dictval[str(key)][str(child_key)]['is_ORDER_DELIVER'] == campare_val:
			if dictval[str(key)][str(child_key)]['orderStatus'] in ['Order Placed','Out For Deliver','Delivered','Cancelled']:
				# for num,prod in enumerate(dictval[str(key)][str(child_key)]['products']):
					# product_lists.append({"product":dictval[str(key)][str(child_key)]['products'][num]['product_Name']})
				return_dict.update({str(child_key):{"key":key,"username":dictval[str(key)][str(child_key)]['userDetails']['s_NAME'],"products":len(dictval[str(key)][str(child_key)]['products']),"cancelled":dictval[str(key)][str(child_key)].get('Is_Order_Cancelled')}})
	return return_dict


from grofer.settings import BASE_DIR
import time
def write_csv(data):
	file = BASE_DIR+'/static/'+str(int(time.time()))+".txt"
	fil = open(file,'w+')
	fil.write(str(data))
	fil.close()
	return None

def test_url(request):
	token_id = request.session['uid']
	template_name = 'admin_panel/user_details.html'
	return render(request, template_name,locals())


def login_page(request):
	template_name = 'login/login.html'
	if request.method == "POST":
		email = request.POST.get('email')
		passwd = request.POST.get('passwd')
		try:
			user = auth.sign_in_with_email_and_password(email,passwd)
			session_id = user['idToken']
			request.session['uid'] = session_id
			message = "Login Succesfull"
			return redirect('dashboard')
		except:
			message = "Something went wrong!!!"
	return render(request, template_name,locals())

def logout_page(request):
	logout(request)
	return redirect('login')

def list_product(request):
	template_name = 'admin_panel/list_product.html'
	token_id = request.session['uid']
	all_products = dict(db.child("Product").get(token_id).val())
	return render(request, template_name,locals())

def dashboard_page(request):
	"""user listing"""
	template_name = 'admin_panel/dashboard.html'
	token_id = request.session['uid']
	all_agents = dict(db.child("Users").get(token_id).val())
	all_agents_list = []
	return render(request, template_name,locals())

def list_category(request):
	template_name = 'admin_panel/list_category.html'
	token_id = request.session['uid']
	all_categories = dict(db.child("ProductCategory").get(token_id).val())
	return render(request, template_name,locals())

def list_subcategory(request):
	template_name = 'admin_panel/list_subcategory.html'
	token_id = request.session['uid']
	all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
	return render(request, template_name,locals())

def list_offers(request):
	template_name = 'admin_panel/list_offers.html'
	token_id = request.session['uid']
	all_offers = dict(db.child('Offers').get(token_id).val())
	return render(request, template_name,locals())

def list_offers_second(request):
	template_name = 'admin_panel/list_offers2.html'
	token_id = request.session['uid']
	try:
		all_offers = dict(db.child('Offers2').get(token_id).val())
	except:
		all_offers = []
	return render(request, template_name,locals())

def create_user_page(request):
	template_name = 'admin_panel/user_create.html'
	token_id = request.session['uid']
	if request.method == 'POST':
		data = request.POST
		user_dict = {'userEmail': data.get('email',''), 'userId': data.get('mobile',0), 'userName': data.get('username','')}
		db.child('Users').push(user_dict,token_id)
		message = "Successfully added"
		return redirect('dashboard')
	return render(request,template_name)



def add_category(request):
	token_id= request.session['uid']
	all_categories = dict(db.child("ProductCategory").get(token_id).val())	
	template_name = 'admin_panel/add_category_new.html'
	if request.method=='POST':
		name = request.POST.get('name')
		offer = request.POST.get('offer')
		description =request.POST.get('description')
		url = request.POST.get('url')
		token_id= request.session['uid']
		category_dict = {
		"Cat_Name":name,
		'Offer':offer,
		'Cat_Details':description,
		'Cat_Image_Url':url,
		}
		add_data_to_table(db,token_id,category_dict,"ProductCategory","Cat_Id","Cat_Created_Date","Cat_Modified_Date")
		return redirect('categorylist')
	return render(request, template_name,locals())



def add_subcategory(request):	
	template_name = 'admin_panel/add_subcategory_new.html'
	token_id= request.session['uid']
	all_categories = dict(db.child("ProductCategory").get(token_id).val())
	if request.method=='POST':
		name = request.POST.get('name')
		offer = request.POST.get('offer')
		description =request.POST.get('description')
		category_id = request.POST.get('category_id')
		subcategory_dict = {
		"Sub_Cat_Name":name,
		'Sub_Cat_Details':description,
		'Cat_Id':category_id,
		'Offer':offer,
		"Sub_Cat_Image_Url":request.POST.get('url')
		}
		add_data_to_table(db,token_id,subcategory_dict,"ProductSubCategory","Sub_Cat_Id","Sub_Cat_Created_Date","Sub_Cat_Modified_Date")
		# db.child('ProductSubCategory').push(subcategory_dict,token_id)
		return redirect('subcategorylist')
	return render(request, template_name,locals())


def add_product(request):	
	template_name = 'admin_panel/add_product_new.html'
	token_id = request.session['uid']
	all_offers = dict(db.child("Offers").get(token_id).val())
	all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
	all_grandcategories = dict(db.child("ProductGrandCategory").get(token_id).val())
	if request.method=='POST':
		data = request.POST
		product_name = data.get('product_name')
		product_mrp = data.get('product_mrp')
		product_sp = data.get('product_sp')
		product_quatity_type = data.get('product_quatity_type')
		product_details = data.get('product_details')
		product_stock_quatity = data.get('product_stock_quatity')
		product_category_id = data.get('product_subcategory_id')
		product_grandcategory_id = data.get('product_grandcategory_id')
		product_image_url = [data.get('url'),data.get('url2'),data.get('url3'),data.get('url4')]
		product_out_of_stok = data.get('out_of_stock',"true")
		product_offer = data.get('product_offer') or ""
		sold_product = data.get('product_sold')
		token_id= request.session['uid']
		grand_cat_name = all_grandcategories.get(product_grandcategory_id)
		product_dict = {
			"DealsOftheday":data.get('dofd'),
			"RecommendedEssentials":data.get('recess'),
			"DailyEssentials":data.get('de'),
			"Product_Cat_Id":dict(db.child("ProductSubCategory").child(product_category_id).get(token_id).val()).get('Cat_Id',''),
			"Product_Name" : product_name,
			"Product_MRP" : product_mrp,
			"Product_SP" : product_sp,
			"Product_Image_Url" : product_image_url,
			"Product_Quantity_Type" :product_quatity_type,
			"Product_Details": product_details,
			"Product_Quantitiy":product_stock_quatity,
			"Product_Sub_Cat_Id": product_category_id,
			"Product_Grand_Cat_Id": product_grandcategory_id,
			"Product_Out_Of_Stock":product_out_of_stok,
			"Product_Offer_Id":product_offer,
			"No_Of_Product_Sold":sold_product,
			"keywords":data.get('keyword'),
			"TotalNumberOfOrdered":0,
			"DeliveryCharge":data.get('deliverycharge'),
			"MoreInfo":data.get('moreinfo'),
			"Product_Grand_Cat_Name":grand_cat_name.get('Grand_Cat_Name'),
			}
		add_data_to_table(db,token_id,product_dict,"Product","Product_Id","Product_Created_Date","Product_Modified_Date")
		# db.child('Product').push(product_dict,token_id)
		return redirect('productlist')
	return render(request, template_name,locals())

def add_offer(request):
	token_id = request.session['uid']
	template_name = 'admin_panel/add_offer.html'
	# all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
	all_products = dict(db.child("Product").get(token_id).val())
	if request.method=='POST':
		data = request.POST
		offer_dict = {
			"Offer_Details":data.get('offer_details'),
			"Offer_Expire_Date":data.get('expire_date'),
			"Offer_Name":data.get('name'),
			"Offer_Code":data.get('offer_code'),
			"Offers_Image_Url":data.get('url'),
			# "Sub_Cat_Id":data.get('subcategory')
			"Prodct_Id":data.getlist('subcategory')
		}
		bool_val,key_val = add_data_to_table(db,token_id,offer_dict,"Offers","Offer_ID","Offer_Created_Date","Offer_Modified_Date")
		"""
		offer id in product list 
		"""
		for p_id in data.getlist('subcategory'):
			product_obj = db.child('Product').child(p_id)
			product_dict = {
				"Product_Modified_Date":str(dt.datetime.now()),
				"Product_Offer_Id":key_val
				}
			product_obj.update(product_dict,token_id)
		"""
		end product offers 
		"""
			
		return redirect('offerslist')	
	return render(request, template_name,locals())


def add_offer_second(request):
	token_id = request.session['uid']
	template_name = 'admin_panel/add_offer2.html'
	# all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
	all_products = dict(db.child("Product").get(token_id).val())
	if request.method=='POST':
		data = request.POST
		offer_dict = {
			"WalletPercentageUsed":data.get('WalletPercentageUsed'),
			"TotalMRPForUsingwallet":data.get('TotalMRPForUsingwallet'),
			"MaximumwalletAmountForOrder":data.get('MaximumwalletAmountForOrder'),
			"Offer_Details":data.get('offer_details'),
			"Offer_Expire_Date":data.get('expire_date'),
			"Offer_Name":data.get('name'),
			"Offer_Code":data.get('offer_code'),
			"Offers_Image_Url":data.get('url'),
			# "Sub_Cat_Id":data.get('subcategory')
			"Prodct_Id":data.getlist('subcategory')
		}
		bool_val,key_val = add_data_to_table(db,token_id,offer_dict,"Offers2","Offer_ID","Offer_Created_Date","Offer_Modified_Date")
		"""
		offer id in product list 
		"""
		for p_id in data.getlist('subcategory'):
			product_obj = db.child('Product').child(p_id)
			product_dict = {
				"Product_Modified_Date":str(dt.datetime.now()),
				"Product_Offer2_Id":key_val
				}
			product_obj.update(product_dict,token_id)
		"""
		end product offers 
		"""
			
		return redirect('offerslist2')	
	return render(request, template_name,locals())


def update_obj_page(request,obj,uid):
	token_id = request.session['uid']
	if obj == 'user':	
		user_details = dict(db.child("Users").child(uid).get(token_id).val())
		template_name = 'admin_panel/user_update.html'
		if  request.method == 'POST':
			user_obj = db.child('Users').child(uid)
			data = request.POST
			user_data = {"userEmail":data.get('email'),"mobile":data.get('email'),"userName":data.get('username')}
			user_obj.update(user_data,token_id)
			return redirect('dashboard')
	
	elif obj == 'category':
		cat_details = dict(db.child("ProductCategory").child(uid).get(token_id).val())
		template_name = 'admin_panel/category_update.html'
		if  request.method == 'POST':
			cat_obj = db.child('ProductCategory').child(uid)
			name = request.POST.get('name')
			description =request.POST.get('description')
			url = request.POST.get('url') if request.POST.get('url') else cat_details.get('Cat_Image_Url')
			cat_data = {
				"Cat_Modified_Date":str(dt.datetime.now()),
				"Cat_Name":name,
				"Cat_Details":description,
				"Cat_Image_Url":url,
				"Offer":request.POST.get('offer_code'),
				}
			cat_obj.update(cat_data,token_id)
			return redirect('categorylist')

	elif obj == 'sub-category':
		all_categories = dict(db.child("ProductCategory").get(token_id).val())
		subcat_details = dict(db.child("ProductSubCategory").child(uid).get(token_id).val())
		template_name = 'admin_panel/subcategory_update.html'
		if  request.method == 'POST':
			subcat_obj = db.child('ProductSubCategory').child(uid)
			name = request.POST.get('name')
			offer = request.POST.get('offer')
			description =request.POST.get('description')
			category_id = request.POST.get('category_id')
			subcategory_dict = {
				"Sub_Cat_Modified_Date":str(dt.datetime.now()),
				"Sub_Cat_Name":name,
				"Sub_Cat_Details":description,
				"Cat_Id":category_id,
				'Offer':offer,
				"Sub_Cat_Image_Url":request.POST.get('url') if request.POST.get('url') else subcat_details.get('Sub_Cat_Image_Url')
			}
			subcat_obj.update(subcategory_dict,token_id)
			return redirect('subcategorylist')

	elif obj == 'grand-category':
		all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
		grandcat_details = dict(db.child("ProductGrandCategory").child(uid).get(token_id).val())
		template_name = 'admin_panel/grandcategoryedit.html'
		if  request.method == 'POST':
			grandcat_obj = db.child('ProductGrandCategory').child(uid)
			name = request.POST.get('name')
			offer = request.POST.get('offer')
			description =request.POST.get('description')
			category_id = request.POST.get('subcategory_id')
			grandcategory_dict = {
				"Sub_Cat_Modified_Date":str(dt.datetime.now()),
				"Grand_Cat_Name":name,
				"Grand_Cat_Details":description,
				"SubCat_Id":category_id,
				"Grand_Cat_Image_Url":request.POST.get('url') if request.POST.get('url') else  grandcat_details.get('Grand_Cat_Image_Url')
			}
			grandcat_obj.update(grandcategory_dict,token_id)
			return redirect('grandcategory')

	elif obj == 'prodcut':
		all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
		all_grandcategories = dict(db.child("ProductGrandCategory").get(token_id).val())
		product_details = dict(db.child("Product").child(uid).get(token_id).val())
		template_name = 'admin_panel/product_update.html'
		if  request.method == 'POST':
			product_obj = db.child('Product').child(uid)
			data = request.POST
			product_name = data.get('product_name')
			product_mrp = data.get('product_mrp')
			product_sp = data.get('product_sp')
			product_image_url = []
			if data.get('url',None):
				product_image_url.append(data.get('url'))
			if data.get('url2',None):
				product_image_url.append(data.get('url2'))
			if data.get('url3',None):
				product_image_url.append(data.get('url3'))
			if data.get('url4',None):
				product_image_url.append(data.get('url4'))
			product_quatity_type = data.get('product_quatity_type')
			product_details = data.get('product_details')
			product_stock_quatity = data.get('product_stock_quatity')
			product_category_id = data.get('product_subcategory_id')
			product_grandcategory_id = data.get('product_grandcategory_id')
			grand_cat_name = all_grandcategories.get(product_grandcategory_id)
			product_dict = {
				"DealsOftheday":data.get('dofd'),
				"RecommendedEssentials":data.get('recess'),
				"DailyEssentials":data.get('de'),
				"Product_Modified_Date":str(dt.datetime.now()),
				"Product_Name" : product_name,
				"Product_MRP" : product_mrp,
				"Product_SP" : product_sp,
				"Product_Out_Of_Stock":data.get('product_stock'),
				"Product_Quantity_Type" :product_quatity_type,
				"Product_Details": product_details,
				"Product_Quantitiy":product_stock_quatity,
				"Product_Sub_Cat_Id": product_category_id,
				"Product_Grand_Cat_Id": product_grandcategory_id,
				"keywords":data.get('keyword'),
				"DeliveryCharge":data.get('deliverycharge'),
				"MoreInfo":data.get('moreinfo'),
				"Product_Grand_Cat_Name":grand_cat_name.get('Grand_Cat_Name')
				}
			if product_image_url:
				product_dict.update({"Product_Image_Url" : product_image_url})
			product_obj.update(product_dict,token_id)
			return redirect('productlist')		

	elif obj == 'offers':
		all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
		offer_details = dict(db.child("Offers").child(uid).get(token_id).val())
		all_products = dict(db.child("Product").get(token_id).val())
		template_name = 'admin_panel/offer_update.html'
		if  request.method == 'POST':
			offer_obj = db.child('Offers').child(uid)
			data = request.POST
			offer_dict = {
			"Offer_Modified_Date":str(dt.datetime.now()),
			"Offer_Details":data.get('offer_details'),
			"Offer_Expire_Date":data.get('expire_date'),
			"Offer_Name":data.get('name'),
			"Offer_Code":data.get('offer_code'),
			"Offers_Image_Url":data.get('url') if data.get('url') else offer_details.get('Offers_Image_Url'),
			"Prodct_Id":data.getlist('products'),
			# "Sub_Cat_Id":data.get('subcategory')
			}
			offer_obj.update(offer_dict,token_id)
			for p_id in data.getlist('products'):
				product_obj = db.child('Product').child(p_id)
				product_dict = {
					"Product_Modified_Date":str(dt.datetime.now()),
					"Product_Offer_Id":uid
					}
				product_obj.update(product_dict,token_id)
			return redirect('offerslist')

	elif obj == 'offers2':
		all_subcategories = dict(db.child("ProductSubCategory").get(token_id).val())
		offer_details = dict(db.child("Offers2").child(uid).get(token_id).val())
		all_products = dict(db.child("Product").get(token_id).val())
		template_name = 'admin_panel/offer2_update.html'
		if  request.method == 'POST':
			offer_obj = db.child('Offers2').child(uid)
			data = request.POST
			offer_dict = {
			"WalletPercentageUsed":data.get('WalletPercentageUsed'),
			"TotalMRPForUsingwallet":data.get('TotalMRPForUsingwallet'),
			"MaximumwalletAmountForOrder":data.get('MaximumwalletAmountForOrder'),
			"Offer_Modified_Date":str(dt.datetime.now()),
			"Offer_Details":data.get('offer_details'),
			"Offer_Expire_Date":data.get('expire_date'),
			"Offer_Name":data.get('name'),
			"Offer_Code":data.get('offer_code'),
			"Offers_Image_Url":data.get('url') if data.get('url') else offer_details.get('Offers_Image_Url'),
			"Prodct_Id":data.getlist('products'),
			# "Sub_Cat_Id":data.get('subcategory')
			}
			offer_obj.update(offer_dict,token_id)
			for p_id in data.getlist('products'):
				product_obj = db.child('Product').child(p_id)
				product_dict = {
					"Product_Modified_Date":str(dt.datetime.now()),
					"Product_Offer2_Id":uid
					}
				product_obj.update(product_dict,token_id)
			return redirect('offerslist2')
	return render(request,template_name,locals())


def delete_obj(request,uid,key,url):
	token_id = request.session['uid']
	if key == "user":
		user_obj = db.child('Users').child(uid)
		user_obj.remove(token_id)
	elif key == "category":
		category_obj = db.child('ProductCategory').child(uid)
		category_obj.remove(token_id)
	elif key == "subcategory":
		subcategory_obj = db.child('ProductSubCategory').child(uid)
		subcategory_obj.remove(token_id)
	elif key == "product":
		product_obj = db.child('Product').child(uid)
		product_obj.remove(token_id)
	elif key == "offer":
		offer_obj = db.child('Offers').child(uid)
		offer_obj.remove(token_id)
	elif key == "offer2":
		offer_obj = db.child('Offers2').child(uid)
		offer_obj.remove(token_id)
	elif key == 'location':
		location_obj = db.child('Locations').child(uid)
		location_obj.remove(token_id)
	elif key == 'grandcategory':
		grandcategory_obj = db.child('ProductGrandCategory').child(uid)
		grandcategory_obj.remove(token_id)
	return redirect(url)

"""
from collections import OrderedDict 
return_dict = {}
for i in di_obj.items():
    for j in di_obj[i[0]].items(): 
        return_dict.update({di_obj[i[0]][j[0]]['orderDate']:[di_obj[i[0]],di_obj[i[0]][j[0]]['orderId']]})
        
ordered_products = OrderedDict(sorted(return_dict.items(),reverse=True)) 
print(dict(ordered_products))

"""

def ordered_history(request,deli_type):
	val_type = deli_type
	template_name = 'admin_panel/ordered_details.html'
	token_id = request.session['uid']
	ordered_products = dict(db.child("User-Order-History").get(token_id).val()) 
	if deli_type == 'delivered':
		val_type = deli_type
		# dataval = filter_function(ordered_products,True)
		dataval = ordered_products
	else:
		# dataval = filter_function(ordered_products,False)
		dataval = ordered_products
	return render(request, template_name,locals())


# def odered_products(request,user_uuid,prod_id):
# 	delivered = bool(request.GET.get('delivered',None))
# 	product_lists = []
# 	template_name = 'admin_panel/order_product_details.html'
# 	token_id = request.session['uid']
# 	ordered_products = dict(db.child("User-Order-History").get(token_id).val())
# 	address = ordered_products[str(user_uuid)][str(prod_id)]['userDetails']
# 	name,mobile,addr,email = [address.get('s_NAME'),address.get('s_MOBILE'),address.get('s_ADDRESS'),address.get('s_MAIL')]
# 	for num,prod in enumerate(ordered_products[str(user_uuid)][str(prod_id)]['products']):
# 		product_lists.append({"product":ordered_products[str(user_uuid)][str(prod_id)]['products'][num]['product_Name'],"prod_id":ordered_products[str(user_uuid)][str(prod_id)]['products'][num]['product_Id'],
# 							"prod_mrp":ordered_products[str(user_uuid)][str(prod_id)]['products'][num]['product_MRP'],
# 							"prod_sp":ordered_products[str(user_uuid)][str(prod_id)]['products'][num]['product_SP'],
# 							"prod_image":ordered_products[str(user_uuid)][str(prod_id)]['products'][num]['product_Image_Url']})

# 	return render(request, template_name,locals())


def order_delivered(request,child_key,parent_key):
	token_id = request.session['uid']
	ordered_products = dict(db.child("User-Order-History").child(parent_key).child(child_key).get(token_id).val())
	ordered_products.update({'is_ORDER_DELIVER':True})
	update_product = db.child("User-Order-History").child(parent_key).child(child_key)
	update_product.update(ordered_products,token_id)
	return HttpResponseRedirect('/order/history/')

def order_cancel(request,child_key,parent_key):
	token_id = request.session['uid']
	ordered_products = dict(db.child("User-Order-History").child(parent_key).child(child_key).get(token_id).val())
	ordered_products.update({'Is_Order_Cancelled':True})
	update_product = db.child("User-Order-History").child(parent_key).child(child_key)
	update_product.update(ordered_products,token_id)
	return HttpResponseRedirect('/order/history/')


def location_list(request):
	token_id = request.session['uid']
	template_name = 'admin_panel/list_locations.html'
	try:
		all_location = dict(db.child("Locations").get(token_id).val())
		return render(request, template_name,locals())
	except:
		return render(request, template_name,locals())


def location_add(request):
	template_name = 'admin_panel/add_location.html'
	token_id= request.session['uid']
	if request.method=='POST':
		data = request.POST
		location_dict = {
			"AreaName":data.get('areaname'),
			"District":data.get('district'),
			"State":data.get('state'),
			"Pincode":str(data.get('pincode')),
			"active":True
			}
		add_data_to_table(db,token_id,location_dict,"Locations","Location_Id","Location_Created_Date","Location_Modified_Date")
		return redirect('locations_list')
	return render(request, template_name,locals())


def list_grand_subcategory(request):
	template_name = 'admin_panel/list_grand_subcategory.html'
	token_id = request.session['uid']
	all_subcategories = dict(db.child("ProductGrandCategory").get(token_id).val())
	return render(request, template_name,locals())


def add_grand_subcategory(request):	
	template_name = 'admin_panel/add_grand_subcategory_new.html'
	token_id= request.session['uid']
	all_categories = dict(db.child("ProductSubCategory").get(token_id).val())
	if request.method=='POST':
		name = request.POST.get('name')
		description =request.POST.get('description')
		category_id = request.POST.get('category_id')
		subcategory_dict = {
		"Grand_Cat_Name":name,
		'Grand_Cat_Details':description,
		'SubCat_Id':category_id,
		"Grand_Cat_Image_Url":request.POST.get('url')
		}
		add_data_to_table(db,token_id,subcategory_dict,"ProductGrandCategory","Grand_Cat_Id","Grand_Cat_Created_Date","Grand_Cat_Modified_Date")
		# db.child('ProductSubCategory').push(subcategory_dict,token_id)
		return redirect('grandcategory')
	return render(request, template_name,locals())


def user_details(request,uid):
	token_id= request.session['uid']
	user_details = dict(db.child("Users").child(uid).get(token_id).val())
	template_name = 'admin_panel/user_details.html'
	user_obj = dict(db.child('Users').child(uid).get(token_id).val())
	wal_amount = 0
	wal_id = 0
	user_wallet = dict(db.child("User-Wallet").get(token_id).val()) 
	#return_foreign_key_val(data,column,comp_val,return_column_name)
	all_address = dict(db.child("User_Address").get(token_id).val())
	user_address = all_address.get(uid) 
	wal_amount = wallet_return_foreign_key_val(user_wallet,'userId',uid,'walletTotalBalance')
	wal_id = return_foreign_key_val(user_wallet,'userId',uid,'walletId')
	return_data = {"Name":user_obj.get('userName'),"Email":user_obj.get('userEmail'),
					"userImageUrl":user_obj.get('userImageUrl'),
					"Wallet_amount":wal_amount,"wal_id":wal_id,
					"address":user_address # multiple address are there
					}
	return render(request, template_name,locals())


def odered_products(request,order_id,sub_id):
	delivered = bool(request.GET.get('delivered',None))
	template_name = 'admin_panel/order_product_details.html'
	token_id = request.session['uid']
	ordered_products = db.child("User-Order-History").child(order_id).child(sub_id).get(token_id).val()
	if ordered_products == None:
		ordered_products = dict(db.child("User-Order-History").child(order_id).child(sub_id).get(token_id).val())
	address = json.loads(ordered_products.get('addressModel',{}))
	products = db.child("User-Ordered_Item").child(order_id).child(sub_id).get(token_id).val()
	print(ordered_products)
	try:
		userdetails =user_details = dict(db.child("Users").child(order_id).get(token_id).val())
	except:
		userdetails = {}
	return render(request, template_name,locals())


from django.urls import reverse
def update_order(request,key,key_n,values):
	token_id = request.session['uid']
	values = values.replace('-',' ')
	ordered_products = dict(db.child("User-Order-History").child(key).child(key_n).get(token_id).val())
	if values == "Order Cancelled":
		try:
			user_val_amount = dict(db.child("User-Wallet").child(key).get(token_id).val())
			wallet_key = [i for i in dict(db.child("User-Wallet").child(key).get(token_id).val()).keys()][0]
			essen_dis = ordered_products.get('essentialsDiscount',0)
			wal_up_data = user_val_amount.get(wallet_key)
			wal_amount = wal_up_data.get('walletTotalBalance',0)
			add_wal_amount = wal_amount + essen_dis
			wal_obj = db.child("User-Wallet").child(key).child(wallet_key)
			wal_obj.update({"walletTotalBalance":add_wal_amount},token_id)
		except Exception as e:
			print('Falied at ' + e.message)
			
	if values == "Order Cancelled":
		ordered_products.update({'orderStatus':values,"reasonForCancellation":"Cancelled by admin"})
	else:
		ordered_products.update({'orderStatus':values,"reasonForCancellation":""})
	update_product = db.child("User-Order-History").child(key).child(key_n)
	update_product.update(ordered_products,token_id)
	extra_update_data = dict(db.child("User-Order-Status").child(key).child(key_n).get(token_id).val())
	extra_update_obj = db.child("User-Order-Status").child(key).child(key_n)
	uuid_key = str(uuid.uuid4())
	extra_update_data.update({uuid_key:{"dateTime":str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
											"key":uuid_key,"orderStatus":values}})
	extra_update_obj.update(extra_update_data,token_id)
	# url = reverse('order_detials', kwargs={'order_id': key,'sub_id':key_n})
	url = reverse('orders_history', kwargs={'deli_type':'history'})
	try:
		fcm_token = dict(db.child("User-FCM-Token").child(key).get(token_id).val()).get('fcmToken')

		if str(values) == "Order is Out For Delivery":
			notification_message = {"title":"Order is Out For Delivery",
										"body":"Your order is Out For Delivery."
									}
		elif str(values) == "Order Delivered":
			notification_message = {"title":"Order Delivered",
										"body":"Your Order is successfully delivered. #Happy Shopping... #safe Shopping..."
									}
		elif str(values) == "Order Cancelled":
			notification_message = {"title":"Order Cancelled",
										"body":"Your Order is cancelled as per your request."
									}
		else:
			notification_message = {}

		ntfication_status = send_notification(fcm_token,notification_message)
		print(url,ntfication_status)
	except:
		pass
	return HttpResponseRedirect(url)
	

def list_carts(request):
	token_id = request.session['uid']
	user_id = request.GET.get('user',0)
	if user_id:
		template_name = 'admin_panel/list_user_carts.html'
		all_cart_lists = dict(db.child('User-CartList').child(user_id).get(token_id).val())
	else:
		template_name = 'admin_panel/list_carts.html'
		all_cart_lists = dict(db.child('User-CartList').get(token_id).val())
	return render(request, template_name,locals())


def detais_cart(request,userid,cartid):
	token_id = request.session['uid']
	template_name = 'admin_panel/details_user_carts.html'
	cart_details = dict(db.child('User-CartList').child(userid).child(cartid).get(token_id).val())
	return render(request, template_name,locals())






























def send_notification(fcm_token,message):
	# message = {}
	# fcm_token = "string"
	import requests
	import json
	from grofer import settings
	try:
		serverToken = settings.SERVER_KEY
		deviceToken = fcm_token
		headers = {
				'Content-Type': 'application/json',
				'Authorization': 'key=' + serverToken,
			}
		body = {
				'notification': message,
				'to':deviceToken,
				'priority': 'high',
				}
		response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
		print(response.status_code)
		print(response.json())
		return 1
	except:
		return 0


from django.core.mail import send_mail
from django.http import JsonResponse
def ordermailapicall(request):
	try:
		order  = request.GET.get('order_id')
		mail_data = settings.ORDER_MAIL 
		send_mail( 
					mail_data.get('subject'),
					mail_data.get('message'),
					mail_data.get('from'),
					#'Essentialsordersnotification@gmail.com', 
					[mail_data.get('to')], 
					#['Essentialsordersnotification@gmail.com'], 
					fail_silently=False
				)
		return JsonResponse({'status': 'True'})
	except Exception as e:
		return JsonResponse({'status': 'False'})

