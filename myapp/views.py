from django.shortcuts import render,HttpResponse,redirect
from .models import User,Category,Product,Wishlist,Cart
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
import random,razorpay
# Create your views here.
def index(request):
    cat=Category.objects.all()
    product=Product.objects.all()
    # user=User.objects.get(request.session['fname'])
    return render(request,"index.html",{'cat':cat,'product':product})
def electronic(request):
    return render(request,"electronic.html")
def fashion(request):
    return render(request,"fashion.html")
def jewellery(request):
    return render(request,"jewellery.html")
def signup(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email Already Exist"
            return render(request,'signup.html',{'msg',msg})
        
        except:            
            if request.POST['pswd']==request.POST['cpswd']:
                User.objects.create(
                fname=request.POST['fname'],
                email=request.POST['email'],
                password=request.POST['pswd'],
                usertype=request.POST['usertype'],
                )
                return render(request,"login.html") 
            else:
                msg="Password and confirm Password doesn't match!!!!!"
                return render(request,'signup.html',{'msg':msg})
    else:  
        return render(request,"signup.html")

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'],password=request.POST['pswd'])
            wishlists=Wishlist.objects.filter(user=user)
            carts=Cart.objects.filter(user=user)
            if user.usertype=="seller":
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'sellerindex.html')
            else:
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'index.html')
                if user is not None:
                    login(request,user)
                    return render(request,'')
        except:
            msg="Email or password not match"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['cart_count'] 
        return render(request,'index.html')
    except:
        return render(request,'login.html')     
def change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if request.POST['opswd']==user.password:
            if request.POST['newpswd']==request.POST['cnewpswd']:
                user.password=request.POST['newpswd']
                user.save()
                return redirect('login')
            else:
                msg="New password and Confirm Password doesn't match!!!"
                return render(request,'change_password.html',{"msg":msg})
        else:
            msg="Old password is wrong!!!"
            return render(request,'change_password.html',{"msg":msg})
    else:
        return render(request,'change_password.html')

def Forgot_pswd(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = "OTP"
            message = "hello"+user.fname+"Your OTP is : "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'email':user.email,'otp':otp})

        except:
            msg="User doesn't exist!!!"
            return render(request,'Forgot_pswd.html',{"msg":msg})
    else:
        return render(request,"Forgot_pswd.html")
    
def otp(request):
    if request.method=='POST':
        email=request.POST['email']
        otp=request.POST['otp']
        uotp=request.POST['uotp']
        user=User.objects.get(email=email)
        if uotp==otp:
            return render(request,"new_pswd.html",{'email':email})

        else:
            msg="OTP doesn't matched!!!"
            return render(request,'otp.html',{"msg":msg})
    else:
        return render(request,'otp.html')
        
def new_pswd(request):
    if request.method=='POST':
        email=request.POST['email']
        npswd=request.POST['npswd']
        cnpswd=request.POST['cnpswd']

        user=User.objects.get(email=email)
        if npswd==cnpswd:
            user.password=npswd
            user.save()
            return redirect('login')
        else:
            msg="New password and Confirm Password doesn't match!!!"
            return render(request,'new_pswd.html',{"msg":msg})

    else:
        return render(request,'new_pswd.html')
    
def sellerindex(request):
    return render(request,'sellerindex.html')

def addproduct(request):
    seller=User.objects.get(email=request.session['email'])
    category=Category.objects.all()
    if request.method=='POST':
        Product.objects.create(
            seller=seller,
            category=Category.objects.get(name=request.POST['category']),
            product_name=request.POST['product_name'],
            product_price=request.POST['product_price'],
            product_qty=request.POST['product_qty'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image']
        )
        msg="Product Added Successfully"
        return render(request,'addproduct.html',{'cat':category,'msg':msg})
        
    else:
        return render(request,'addproduct.html',{'cat':category})

def viewproduct(request):
    seller=User.objects.get(email=request.session['email'])
    product=Product.objects.filter(seller=seller)
    return render(request,'viewproduct.html',{'product':product })    

def details(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'details.html',{'product':product})

def editproduct(request,pk): 
    seller=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    category=Category.objects.all()
    if request.method=="POST":
        product.product_name=request.POST['product_name']
        product.product_price=request.POST['product_price']
        product.product_qty=request.POST['product_qty']
        product.product_desc=request.POST['product_desc']
        try:
            product.product_image=request.FILES['product_image']
        except:
            pass    
        product.save()
        return render(request,'editproduct.html',{'product':product,'cat':category})
    else:
        return render(request,'editproduct.html',{'product':product,'cat':category})

def deleteproduct(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('viewproduct')

def allproduct(request):
    cat=Category.objects.all()
    product=Product.objects.all()
    return render(request,'allproduct.html',{'product':product,'cat':cat})

def buyerdetails(request,pk):
    wishlist_obj=False
    cart_obj=False
    product=Product.objects.get(pk=pk)
    cat=Category.objects.all()
    user=User.objects.get(email=request.session['email'])
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_obj=True
        return render(request,'buyerdetails.html',{'product':product,'wishlist_obj':wishlist_obj,'cat':cat})
    except:
        pass
    try:
        Cart.objects.get(user=user,product=product)
        cart_obj=True
        return render(request,'buyerdetails.html',{'product':product,'cart_obj':cart_obj,'cat':cat})
    except:
        pass
    return render(request,'buyerdetails.html',{'product':product,'cat':cat})


def wishlist(request):
    cat=Category.objects.all()
    if user==User.objects.get(email=request.session['email']): 
        wishlists=Wishlist.objects.filter(user=user)
        return render(request,'wishlist.html',{'wishlists':wishlists,'cat':cat})
    else:
        msg="You need to login"
        return render(request,'wishlist.html',{'wishlists':wishlists,'cat':cat,'msg':msg})

def addtowishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk) 
    Wishlist.objects.create(
        user=user,
        product=product,
    )
    return redirect('wishlist') 

def removefromwishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk) 
    wishlists=Wishlist.objects.get(user=user,product=product)
    wishlists.delete()
    return redirect('wishlist')

def cart(request):
    net_price=100
    cat=Category.objects.all()
    User.objects.all()
    try:
        user=User.objects.get(email=request.session['email'])
        # product=Product.objects.get(pk=pk) 
        carts=Cart.objects.filter(user=user,payment=False)
        request.session['cart_count']=len(carts)
        for i in carts:
            net_price+=i.total
        carts.net_price=net_price
        client = razorpay.Client(auth = (settings.KEY_ID, settings.KEY_SECRET))
        payments = client.order.create({'amount':carts.net_price*100,'currency':'INR','payment_capture':1})   
        print("1111111111111111",payments)
        carts.razorpay_order_id=payments['id']
        for i in carts:
            i.save()
        return render(request,'cart.html',{'carts':carts,'payments':payments,'cat':cat})
    except:
        return render(request,'login.html',{'cat':cat})


def success(request):
    order_id=request.GET.get('order_id')
    carts=Cart.objects.filter(razorpay_order_id=order_id)
    for i in carts:
        i.payment=True
        i.save()
    carts.delete()
    return render(request,'callback.html')
def addtocart(request,pk):
    try:     
        user=User.objects.get(email=request.session['email'])
        product=Product.objects.get(pk=pk)
        carts=Cart.objects.get(user=user,product=product)
        return redirect('cart')
    except: 
        Cart.objects.create(
            user=user,
            product=product,
            product_price=product.product_price,
            total=product.product_price,
            product_qty=1
        )
        return redirect('cart') 

def removefromcart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk) 
    carts=Cart.objects.get(user=user,product=product)
    carts.delete()
    return redirect('cart')

def change_qty(request,pk):
    pk=pk
    product_qty=int(request.POST['product_qty'])
    carts=Cart.objects.get(pk=pk)
    carts.total=product_qty*carts.product_price
    carts.product_qty=product_qty
    carts.save()
    return redirect('cart')

def category(request,pk):
    l=Category.objects.all()
    cat=Category.objects.get(pk=pk)
    product=Product.objects.filter(category=cat)
    return render(request,'category.html',{'product':product,'l':l})

def search(request):
    if request.method=='POST':
        if request.POST['name_search'].__contains__('PC'):
            product=Product.objects.get(product_name=request.POST['name_search'])
            return render(request,'buyerdetails.html',{'product':product})
        else:
            return render(request,'allproducts.html')
    else:
        return(request,'index.html')