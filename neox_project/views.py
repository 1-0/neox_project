import os
import subprocess
from django.shortcuts import render
from django.conf import settings


def home(request, *args, **kwargs):
    """home - show home page"""
    return render(
        request,
        'home.html',
    )


