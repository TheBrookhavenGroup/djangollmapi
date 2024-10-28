from torch.distributed.elastic.multiprocessing.redirects import redirect

from .settings import INDEX_URL
from django.shortcuts import render, redirect


def index(request):
    return redirect(INDEX_URL)
