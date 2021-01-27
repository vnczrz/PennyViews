from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError, Error, transaction
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
import yfinance as yf
from yahoo_fin.stock_info import get_stats, get_live_price, get_holders, get_analysts_info
import json
from pprint import pprint
import pandas as pd
from django.views.generic import ListView

from .models import User, Stock, Portfolio, Holding

def format_currency(value):
    return "${:,.2f}".format(value)

def get_price(str):
    p = get_live_price(str)

    return p

def get_balance_sheet(ticker):
    stock = get_stats(f'{ticker}')

    l = []
    balance_sheet = stock.loc['28':, 'Attribute':'Value'].to_dict('records')
    price_his = stock.loc[0:8, 'Attribute':'Value'].to_dict('records')

    l = [balance_sheet, price_his]
    return l

def basicInfo(obj):
    info = {}
    table = ['open',
    'previousClose', 
    'dividendYield', 
    'marketCap', 
    'fiftyTwoWeekHigh', 
    'fiftyTwoWeekLow', 
    'forwardPE', 
    'earningsQuarterlyGrowth', 
    'longBusinessSummary',
    'volume',
    'enterpriseValue',
    'enterpriseToEbitda',
    'sharesOutstanding']
    
    for t in table:
        try:
            d = obj.info[f'{t}']
            if d in ["None", None]:
                x = {f'{t}': 'N/A'}
                info.update(x)
            else:
                x = {f'{t}': f'{d}'}
                info.update(x)
        except KeyError:
            x = {f'{t}': 'N/A'}
            info.update(x)

    return info
    # recs = obj.recommendations
    # time_mask = recs.last('3M')
    # time_sort = time_mask.sort_values(by='Date', ascending=False)
    # rec = time_sort.to_dict('records')
    
    # base.append(info)
    # base.append(rec)

def home(request):
    
    if request.method == 'POST':
        
        ticker = request.POST['ticker']

        res_ = yf.Ticker(f"{ticker}")

        # test = dir(res_)
        
        # pprint(test, indent=2)

        return render(request, 'home.html', {'res_': res_})

    else: 
        return render(request, 'home.html', {'ticker': 'Enter Stock Symbol Above...'})

def search(request):
    if request.method == "POST":
        symbol = request.POST["symbol"]
        symbol = symbol.upper()

    try:
        s = Stock.objects.get(symbol=symbol)
        ticker=s.symbol
        return HttpResponseRedirect(reverse("stock", kwargs={'symbol': ticker}))
        
    except Stock.DoesNotExist:
        return render(request, 'stock.html', {'message': 'Could not find symbol, try again.'})

def stock(request, symbol):
    if request.method == "GET":
        s = Stock.objects.get(symbol=symbol)
        
        stock = yf.Ticker(f'{symbol}')
        # price = get_live_price(f'{symbol}')
        
        stats = get_balance_sheet(f'{symbol}')
        
        basic_info = basicInfo(stock)

        return render(request, 'stock.html', {'stock': s, 'basic_info': basic_info, 'balance': stats[0], 'price_his': stats[1]})
    

class WatchList(ListView):
    model =  Portfolio
    template_name = 'templates/portfolio.html'
    
    def get_queryset(self):
        return Portfolio.objects.filter(user = self.request.user)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            
        
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "register.html")