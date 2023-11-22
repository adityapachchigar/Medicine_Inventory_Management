from django.shortcuts import render
from .forms import PurchaseForm
from .models import Stock
from django.db import connection
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import datetime
# Create your views here.
bill=[]

def home(request):
    return render(request, 'home.html')

def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='order_details.pdf')
    return response
 
def generate_pdf_file():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # prods = Stock.objects.all()
    p.drawString(100, 750, "Order Details")
    # p.drawString(100, 700, f"Username : {prods[0].user}")
 
    y = 700
    # x=20
    sum_total=bill[len(bill)-1]
    # for i in prods:
    #     sum_total+=i.value

    # for i in bill:
    
    # p.drawString(x+50, 700, f"Medicine Name")
    # p.drawString(x+100, 700, f"Medicine Dose Form")
    # p.drawString(x+150, 700, f"Medicine Batch No.")
    # p.drawString(x+200, 700, f"Medicine Expiry Date")
    # p.drawString(x+250, 700, f"Quantity")
    # p.drawString(x+300, 700, f"MRP")
    
    
    p.drawString(100, y-20, f"Medicine Name : {bill[len(bill)-6]}")
    p.drawString(100, y-40, f"Medicine Dose Form : {bill[len(bill)-7]}")
    p.drawString(100, y-60, f"Medicine Batch No. : {bill[len(bill)-3]}")
    p.drawString(100, y-80, f"Medicine Expiry Date : {bill[len(bill)-2]}")
    p.drawString(100, y-100, f"Quantity : {bill[len(bill)-5]}")
    p.drawString(100, y-120, f"MRP : {bill[len(bill)-4]}")
    # bill=[]
    # y -= 60

    p.drawString(100, y-200, f"Bill Total : {sum_total}")
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    # bill=[]
    return buffer



def sales(request):
    if request.method == "POST":
        f = PurchaseForm(request.POST)
        if f.is_valid():
            d = f.cleaned_data
            c1 = d.get("doses")
            c2 = d.get("med_name")
            c2= c2.upper()
            c3 = d.get("quantity")
            c4 = d.get("mrp")
            c5 = d.get("batch_no")
            c6 = d.get("expiry_date")
            c7 = int(c3)*int(c4)
            bill.append(c1);
            bill.append(c2);
            bill.append(c3);
            bill.append(c4);
            bill.append(c5);
            bill.append(c6);
            bill.append(c7);
            # bill.append(t);
            
            with connection.cursor() as cursor:
                sql_query = "SELECT quantity FROM med_stock WHERE doses=%s AND med_name=%s AND batch_no=%s"
                cursor.execute(sql_query,[str(c1),str(c2),str(c5)])
                r1 = cursor.fetchall()
            temp = r1[0][0]
            qty = int(temp)-int(c3)
            
            with connection.cursor() as cursor:
                sql_query = "SELECT amount FROM med_stock WHERE doses=%s AND med_name=%s AND batch_no=%s "
                cursor.execute(sql_query,[str(c1),str(c2),str(c5)])
                r2 = cursor.fetchall()
            temp2 = r2[0][0]
            q2 = int(temp2)-int(c7)
            
            with connection.cursor() as cursor:
                sql_query = "UPDATE med_stock SET quantity=%s,amount=%s WHERE batch_no=%s AND doses=%s AND med_name=%s"
                cursor.execute(sql_query,[str(qty),str(q2),str(c5),str(c1),str(c2)])
            connection.commit()
    
            return render(request,"orderConfirmed.html")
    f1 = PurchaseForm()
    context = {'form':f1}
    return render(request,"sales.html",context)

def stock(request):
    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM med_stock ORDER BY med_name,doses"
        cursor.execute(sql_query)
        results = cursor.fetchall()
    # connection.commit()
    context = {'data': results
            #    ,'date':str(datetime.now())
               }
    return render(request,"stock.html",context)

def purchase(request):
    if request.method == "POST":
        f = PurchaseForm(request.POST)
        if f.is_valid():
            d = f.cleaned_data
            c1 = d.get("doses")
            c2 = d.get("med_name")
            c2= c2.upper()
            c3 = d.get("quantity")
            c4 = d.get("mrp")
            c5 = d.get("batch_no")
            c6 = d.get("expiry_date")
            c7 = int(c3)*int(c4)
            
            with connection.cursor() as cursor:
                sql_query = "SELECT doses,med_name,batch_no FROM med_stock"
                cursor.execute(sql_query)
                r1 = cursor.fetchall()
                
            # print(r1)
            b1=[]
            for i in r1:
                b1.append((i[0],i[1],i[2]))
            
            if (c1,c2,c5) in b1:
                with connection.cursor() as cursor:
                    sql_query = "SELECT quantity FROM med_stock WHERE batch_no=%s"
                    # sql_query = "INSERT INTO med_stock(doses,med_name,quantity,mrp,batch_no,expiry_date) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_query,[str(c5)])
                    res = cursor.fetchall()
                temp = res[0][0]
                qty = int(temp)+int(c3)
                with connection.cursor() as cursor:
                    sql_query = "UPDATE med_stock SET quantity=%s WHERE batch_no=%s"
                    cursor.execute(sql_query,[str(qty),str(c5)])
                connection.commit()
            
            if (c1,c2,c5) not in b1:
                with connection.cursor() as cursor:
                    sql_query = "INSERT INTO med_stock(doses,med_name,quantity,mrp,batch_no,expiry_date,amount) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_query,[str(c1),str(c2),str(c3),str(c4),str(c5),str(c6),str(c7)])
                connection.commit()

            return render(request,"home.html")
    f1 = PurchaseForm()
    context = {'form':f1}
    return render(request,"purchase.html",context)