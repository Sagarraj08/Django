from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("electronic",views.electronic,name="electronic"),
    path("fashion",views.fashion,name="fashion"),
    path("jewellery",views.jewellery,name="jewellery"),
    path("signup",views.signup,name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("change_password",views.change_password,name="change_password"),
    path("Forgot_pswd",views.Forgot_pswd,name="Forgot_pswd"),
    path("otp",views.otp,name="otp"),
    path("new_pswd",views.new_pswd,name="new_pswd"),
    path("sellerindex",views.sellerindex,name="sellerindex"),
    path("addproduct",views.addproduct,name="addproduct"),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('details/<int:pk>',views.details,name='details'),
    path('editproduct/<int:pk>/',views.editproduct,name='editproduct'),
    path("deleteproduct/<int:pk>/",views.deleteproduct,name='deleteproduct'),
    path("allproduct",views.allproduct,name='allproduct'),
    path("buyerdetails/<int:pk>/",views.buyerdetails,name='buyerdetails'),
    path("wishlist",views.wishlist,name='wishlist'),
    path("addtowishlist/<int:pk>/",views.addtowishlist,name='addtowishlist'),
    path('removefromwishlist/<int:pk>/',views.removefromwishlist,name='removefromwishlist'),
    path("cart",views.cart,name='cart'),
    path("addtocart/<int:pk>/",views.addtocart,name='addtocart'),
    path('removefromcart/<int:pk>/',views.removefromcart,name='removefromcart'),
    path('change_qty/<int:pk>/',views.change_qty,name='change_qty'),
    path('category/<int:pk>/',views.category,name='category'),
    path('search',views.search,name='search'),
    path('success',views.success,name='success'),
    path('ajax/Form_Validation/',views.Form_Validation,name='Form_Validation'),



]