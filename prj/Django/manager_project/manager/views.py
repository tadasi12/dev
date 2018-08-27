from django.shortcuts import render
from django.views.generic import TemplateView
from manager.models import *
from django.db.models import F, Func


class WorkerListView(TemplateView):
    template_name = "worker_list.html"

    def get(self, request, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        workers = Worker.objects.all().annotate(distance=Func(10 - F('manager_id'), function='ABS')).order_by("distance")
        context['workers'] = workers  # context に入れる

        return render(self.request, self.template_name, context)