import razorpay
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate
from ecommerceapp import keys
from math import ceil
from django.conf import settings
MERCHANT_KEY = keys.RAZORPAY_KEY_SECRET

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "index.html", params)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        pnumber = request.POST.get('pnumber')
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "We will get back to you soon.")
        return render(request, 'contact.html')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = int(request.POST.get('amt')) * 100  # Razorpay expects amount in paise
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, amount=amount // 100, email=email, address1=address1,
                       address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        # Razorpay Payment Integration
        client = razorpay.Client(auth=(keys.RAZORPAY_KEY_ID, keys.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order.razorpay_order_id = payment['id']
        order.save()

        return render(request, 'razorpay.html', {'payment': payment, 'order': order})

    return render(request, 'checkout.html')
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        response = request.POST

        params_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature')
        }
        try:
            client = razorpay.Client(auth=(keys.RAZORPAY_KEY_ID, keys.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature(params_dict)

            razorpay_order_id = response.get('razorpay_order_id')
            order = Orders.objects.get(razorpay_order_id=razorpay_order_id)

            razorpay_payment_id = response.get('razorpay_payment_id')
            oid_numeric = int(''.join(filter(str.isdigit, razorpay_payment_id)))

            id = order.order_id

            order.paymentstatus = "PAID"
            order.oid = str(id) + "ShopyCart"
            order.amountpaid = response.get('amount', order.amount)
            order.save()

            return render(request, 'paymentstatus.html', {
                'response': response,
                'status': 'Payment Successful',
                'order_id': order.order_id
            })
        except Orders.DoesNotExist:
            messages.error(request, "Order not found in the database.")
            return render(request, 'paymentstatus.html', {
                'response': response,
                'status': 'Payment Failed'
            })
        except razorpay.errors.SignatureVerificationError as e:
            messages.error(request, "Razorpay signature verification failed.")
            print(e)
            return render(request, 'paymentstatus.html', {
                'response': response,
                'status': 'Payment Failed'
            })
        except Exception as e:
            messages.error(request, "An error occurred during payment processing.")
            print(e)
            return render(request, 'paymentstatus.html', {
                'response': response,
                'status': 'Payment Failed'
            })
    return render(request, 'paymentstatus.html')

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')
    
    currentuser_email = request.user.email
    print(f"Current User Email: {currentuser_email}")
    
    # Check if the email is correctly retrieved
    if not currentuser_email:
        print("No email found for the current user.")
        return render(request, "profile.html", {"items_with_serial": []})

    # Fetch orders for the current user
    items = Orders.objects.filter(email=currentuser_email)
    print(f"Orders found for user ({currentuser_email}): {items}")

    # If no orders found, print a message
    if not items.exists():
        print(f"No orders found for user with email {currentuser_email}")
        return render(request, "profile.html", {"items_with_serial": []})

    items_with_serial = []
    for idx, item in enumerate(items, start=1):
        myid = item.oid
        statuses = []
        if "ShopyCart" in myid:
            rid = myid.replace("ShopyCart", "")
            try:
                rid_int = int(rid)
                statuses = list(OrderUpdate.objects.filter(order_id=rid_int))
                
                # Print order and updates information to the terminal
                print(f"Order ID: {item.order_id}")
                print(f"Order Details: {item}")
                for update in statuses:
                    print(f"Update for Order ID {rid_int}: {update}")

            except ValueError:
                print(f"Invalid order_id extracted: {rid}")

        items_with_serial.append({
            "serial": idx,
            "order_id": item.order_id,
            "name": item.name,
            "items_json": item.items_json,
            "amount": item.amount,
            "paymentstatus": item.paymentstatus,
            "address1": item.address1,
            "phone": item.phone,
            "statuses": statuses
        })

    context = {"items_with_serial": items_with_serial}
    print(f"Final Items with Serial: {items_with_serial}")
    
    return render(request, "profile.html", context)


   